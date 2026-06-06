import ollama

def generate_response(user_input, relationship, nickname, chat_history):
    # Format previous messages properly
    formatted_history = "\n".join(
        [f"{nickname}: {msg['user']}\n{relationship}: {msg['bot']}" for msg in chat_history]
    )

    prompt = (
        f"You are {relationship} to {nickname}. Always call them '{nickname}', and never use any other name like 'sweetheart' or 'dear'. "
        f"Your response should feel exactly like how a real {relationship} would talk. "
        f"You already know their name, so do not act surprised or ask for their name again. "
        f"Be warm, caring, and realistic, just like a real {relationship}. Do NOT sound like a chatbot. "
        f"Always use appropriate emojis to enhance emotional depth. "
        f"Avoid using markdown formatting like *italics* or **bold**. "
        
        f"\nHere is the conversation history so far:\n{formatted_history}\n\n"
        f"{nickname}: {user_input}\n"
        f"{relationship}:"
    )

    try:
        response = ollama.chat(model="gemma2:2b", messages=[{"role": "user", "content": prompt}])
        ai_response = response["message"]["content"].strip()

        # 🛠 **Extra Fix:** Forcefully replace any unexpected names
        ai_response = ai_response.replace("sweetie", nickname).replace("darling", nickname).replace("honey", nickname)
        
        return ai_response
    except Exception as e:
        print(f"❌ Ollama (Gemma-2B) failed: {e}")
        return f"Sorry, {nickname}, I am having trouble responding right now."
