#at
# import os
from openai import OpenAI
#at

import os
import json
from io import BytesIO
from itertools import groupby
from elevenlabs import ElevenLabs

# # Set your ElevenLabs API key
# os.environ["ELEVENLABS_API_KEY"] = ELEVENLABS_API_KEY




# Path to the API key file
api_keys_file = "D:\\call\\elevenlabs.txt"

def rotate_and_get_api_key(file_path):
    with open(file_path, 'r+') as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise ValueError("API key file is empty!")

        # Get the first key
        current_api_key = lines[0]

        # Rotate the list: move first to last
        rotated_keys = lines[1:] + [current_api_key]

        # Move cursor to beginning and overwrite file
        f.seek(0)
        f.truncate()
        f.write('\n'.join(rotated_keys) + '\n')  # Ensure newline at end

        return current_api_key

# Get and set the rotated API key
ELEVENLABS_API_KEY = rotate_and_get_api_key(api_keys_file)
os.environ["ELEVENLABS_API_KEY"] = ELEVENLABS_API_KEY




# Paths (fixed to match your automation)
INPUT_AUDIO_PATH = r"D:\call\autocall\audio_temp\rec.wav"
FORMATTED_OUTPUT_PATH = r"D:\call\autocall\transcripts\call_transcript.txt"
RAW_OUTPUT_PATH = r"D:\call\autocall\transcripts\raw_transcription.json"

def transcribe_audio(file_path):
    """
    Transcribes an audio file using ElevenLabs API.
    """
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    with open(file_path, "rb") as f:
        audio_data = BytesIO(f.read())

    transcription = client.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1",
        tag_audio_events=True,
        diarize=True,
        # language_code="eng"
    )

    return transcription

# def format_transcription_by_speaker(transcription):
#     """
#     Formats transcription by speaker using speaker diarization.
#     """
#     words = transcription.words
#     segments = []

#     for speaker_id, group in groupby(words, key=lambda x: x.speaker_id):
#         speaker_words = [w.text for w in group if w.type in ("word", "audio_event")]
#         speaker_text = " ".join(speaker_words).strip()
#         if speaker_text:
#             segments.append(f"{speaker_id.capitalize()}: {speaker_text}")

#     return "\n\n".join(segments)









def format_transcription_by_speaker(transcription):
    """
    Formats transcription by speaker using speaker diarization.
    Adds time ranges and audio event durations in a single set of parentheses.
    """
    words = transcription.words
    segments = []

    for speaker_id, group in groupby(words, key=lambda x: x.speaker_id):
        group_list = list(group)
        start_time = group_list[0].start
        end_time = group_list[-1].end

        speaker_parts = []
        for w in group_list:
            if w.type == "audio_event" and w.text.strip():
                duration = round(w.end - w.start, 2)
                speaker_parts.append(f"({w.text} for {duration} seconds)")
            elif w.type == "word":
                speaker_parts.append(w.text)

        speaker_text = " ".join(speaker_parts).strip()
        if speaker_text:
            time_str = f"({format_time(start_time)}-{format_time(end_time)})"
            segments.append(f"{speaker_id.capitalize()}: {speaker_text} {time_str}")

    return "\n\n".join(segments)


def format_time(seconds):
    """Formats seconds into M:SS format."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"
















def save_transcription(transcription):
    """
    Saves the formatted and raw transcription results to disk.
    """
    formatted = format_transcription_by_speaker(transcription)

    # Save formatted text
    with open(FORMATTED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(formatted)

    # Save raw transcription data
    with open(RAW_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(transcription.model_dump(), f, indent=2)

    print("Transcription saved:")
    print(f"- Formatted: {FORMATTED_OUTPUT_PATH}")
    print(f"- Raw JSON: {RAW_OUTPUT_PATH}")
    return formatted








#analyze transcript

# # API key (keep it hardcoded as you requested)

openrouter_file = "D:\\call\\deepseek.txt"
OPENROUTER_API_KEY = rotate_and_get_api_key(openrouter_file)
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY



# Setup OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)




def analyze_transcript(transcript_text, rules_path="rules_and_options.txt", instructions_path="instructions.txt"):
    # Load rules and instructions from local files
    with open(rules_path, "r", encoding="utf-8") as file:
        RULES = file.read()

    with open(instructions_path, "r", encoding="utf-8") as file:
        INSTRUCTIONS = file.read()

    # Prepare messages for API
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert call reviewer for humanatic.com. Use the provided rules and instructions "
                "to analyze customer service calls and select the correct multiple-choice response out of options provided at end of Rules."
            )
        },
        {
            "role": "user",
            "content": (
                f"These are the rules + options:\n{RULES}\n\n"
                f"Here is the transcription of the call:\n\n{transcript_text}\n\n"
                f"These are instructions you have to follow:\n{INSTRUCTIONS}\n\n"
                f"Read them carefully and use 100% of your intelligence to give the correct answer."
            )
        }
    ]

    # Send request to OpenRouter
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=messages
    )

    reply = response.choices[0].message.content
    return reply



# Run automatically
if __name__ == "__main__":

    # Clear existing files in transcripts folder
    for f in os.listdir(os.path.dirname(FORMATTED_OUTPUT_PATH)):
        if f != "log.txt":  # Skip log file
            os.remove(os.path.join(os.path.dirname(FORMATTED_OUTPUT_PATH), f))

    print("Transcribing from:", INPUT_AUDIO_PATH)
    transcription = transcribe_audio(INPUT_AUDIO_PATH)
    print("Saving output...")
    formatted = save_transcription(transcription)
    print("\n--- Transcription Complete ---\n")
    print(formatted)

    # Analyze transcript
    print("Analyzing call transcript...")
    result = analyze_transcript(formatted)
    print("\n--- AI Response ---\n")

    try:
        print(result)
        with open(r"D:\call\autocall\transcripts\ai_response.txt", "w", encoding="utf-8") as f:
            f.write(result)
        with open(r"D:\call\autocall\transcripts\log.txt", "a", encoding="utf-8") as log:
            log.write("AI response saved successfully.\n")
    except Exception as e:
        with open(r"D:\call\autocall\transcripts\log.txt", "a", encoding="utf-8") as log:
            log.write(f"Error while saving AI response: {e}\n")




#analyze transcript