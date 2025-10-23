from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    transcript_path = r"autocall/transcripts/call_transcript.txt"
    ai_result_path = r"autocall/transcripts/ai_response.txt"

    transcript = ""
    ai_result = ""

    if os.path.exists(transcript_path):
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()

    if os.path.exists(ai_result_path):
        with open(ai_result_path, "r", encoding="utf-8") as f:
            ai_result = f.read()

    return render_template("index.html", transcript=transcript, ai_result=ai_result)


if __name__ == "__main__":
    app.run(debug=True)
