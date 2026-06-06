from models.emotion_detector import detect_emotion
from chatbot.response_generator import generate_response
from chatbot.speech_to_text import record_audio, transcribe_audio

# Main Chatbot Code with Relationship Handling
def chatbot():
    print("Mental Health Chatbot: Type 'exit' to end the chat.\n")

    # Ask the user for the relationship and preferred nickname
    relationship = input("Who would you like me to respond as? (e.g., Mom, Dad, Cousin, Friend): ").strip().lower()
    nickname = input(f"How would you like {relationship} to address you? (e.g., sweetie, buddy, your name): ").strip()

    while True:
        user_input = input("You (or type 'voice' to talk): ")
        
        if user_input.lower() == "exit":
            print(f"{relationship.title()}: Take care, {nickname}! 💙")
            break
        
        # If user wants to talk instead of typing
        if user_input.lower() == "voice":
            audio_path = record_audio(duration=5)
            user_input = transcribe_audio(audio_path)

        print("🔍 Detecting emotion...")
        try:
            emotion = detect_emotion(user_input)
            print(f"✅ Detected emotion: {emotion}")
        except Exception as e:
            print(f"❌ Emotion detection failed: {e}")
            continue

        print("📝 Generating response...")
        try:
            response = generate_response(user_input, emotion, relationship, nickname)
            print(f"🤖 {relationship.title()} ({emotion} detected): {response}")
        except Exception as e:
            print(f"❌ Response generation failed: {e}")
            continue

if __name__ == "__main__":
    chatbot()
