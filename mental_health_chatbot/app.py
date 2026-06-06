from flask import Flask, render_template, request, jsonify, session
from chatbot.response_generator import generate_response
from chatbot.speech_to_text import transcribe_audio
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/")
def index():
    session.pop("chat_history", None)
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    chat_history = session.get("chat_history", [])

    if request.content_type == "application/json":
        # Handle text messages
        data = request.get_json()
        user_message = data.get("message", "").strip()
        relationship = data.get("relationship", "").strip()
        nickname = data.get("nickname", "").strip()

    elif "audio" in request.files:
        # Handle voice messages
        user_message = "(Voice Message)"
        relationship = request.form.get("relationship", "").strip()
        nickname = request.form.get("nickname", "").strip()

        # Save and transcribe the audio file
        audio_file = request.files["audio"]
        audio_path = os.path.join("uploads", "voice_input.wav")
        os.makedirs("uploads", exist_ok=True)
        audio_file.save(audio_path)

        user_message = transcribe_audio(audio_path)  # Convert speech to text

    else:
        return jsonify({"error": "Invalid content type"}), 400

    if not relationship or not nickname:
        return jsonify({"error": "Please provide both relationship and nickname"}), 400

    # Generate AI response
    bot_response = generate_response(user_message, relationship, nickname, chat_history)

    # Store chat history within session (until refresh)
    chat_history.append({"user": user_message, "bot": bot_response})
    session["chat_history"] = chat_history[-10:]  # Keep last 10 messages

    return jsonify({"response": bot_response, "chat_history": chat_history})

if __name__ == "__main__":
    app.run(debug=True)
