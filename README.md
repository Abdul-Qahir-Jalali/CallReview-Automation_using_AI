# CallReview-Automation_Using_AI 🎧🤖

This project automates the **Humanatic call review** process using **AI-powered transcription and decision-making**.

When a call recording is taken from Humanatic:
1. The audio is sent to **ElevenLabs** via API for high-quality transcription.
2. The resulting text is sent to **DeepSeek AI**, which uses predefined rules and instructions to review the call.
3. The Flask web app displays:
   - the **call transcript**
   - the **AI-generated review result**
   - a short **explanation / justification**

---

## 🧠 Features
- 🎙️ Automatically records audio from Humanatic (AHK automation)
- 🪄 Transcribes calls using ElevenLabs API
- 🤖 Analyses and reviews calls using DeepSeek API (rule-based logic)
- 🌐 Displays results in a local Flask web app
- 🔁 Rotates multiple API keys automatically
- 🧩 Organized folder structure (audio, transcripts, templates, etc.)

---

## 🗂️ Project Structure

CallReview-Automation_Using_AI/
│
├─ autocall/
│ ├─ automation.ahk # AutoHotkey script to start/stop recording
│ ├─ audio_temp/ # Temporary audio files (ignored)
│
├─ transcripts/ # Generated transcripts and AI responses
│
├─ rules_and_instructions/
│ ├─ rules_and_options.txt
│ ├─ instructions.txt
│
├─ templates/
│ └─ index.html # Flask HTML template
│
├─ flask_app.py # Web interface to display results
├─ transcribe.py # Handles ElevenLabs + DeepSeek API calls
├─ .gitignore
└─ README.md



---

## ⚙️ How It Works (Quick Summary)

1. Open **Humanatic** and start a call review.  
2. Press **Ctrl + Q** → the AutoHotkey script begins recording.  
3. Press **Ctrl + W** → recording stops and the audio file is saved in `autocall/audio_temp/`.  
4. `transcribe.py` automatically:
   - Sends the audio to **ElevenLabs** for transcription.  
   - Passes the transcript to **DeepSeek AI**, which reviews it based on the predefined **rules and options**.  
   - Saves both transcript and AI-generated review in the `/transcripts` folder.  
5. The **Flask web app** displays:
   - the call transcript  
   - the review decision  
   - a short justification for why that option was selected.  

---

## 🚀 Setup Instructions

1. **Clone or download** this repository.  
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3.Add your own API keys for ElevenLabs and DeepSeek inside the scripts where indicated (fake keys are placeholders).

Run the Flask app

python flask_app.py
http://127.0.0.1:5000/


🛡️ Notes

🔒 No real API keys are included — only placeholder (fake) keys for demonstration.

🎧 Audio recordings and transcripts are ignored via .gitignore to keep the repository clean.

🧠 This project is intended for educational and portfolio purposes.

🪄 You can customize rules and logic inside the rules_and_instructions/ folder to change how DeepSeek evaluates calls.
