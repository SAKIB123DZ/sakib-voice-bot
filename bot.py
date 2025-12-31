
import telebot
import requests

# --- CONFIGURATION ---
API_TOKEN = '8466199285:AAG5dz2C3mGyTKb4mdJRq0k5ohebgVYqL6I' # Aapka Token
ELEVENLABS_API_KEY = 'R8_Ti12QajRr7a1hJgaVXpM6v4lkQFbBT23Buf8D' # Aapki Key

bot = telebot.TeleBot(API_TOKEN)

# Voice IDs
INTRO_VOICE_ID = "aE6av5ff68FOJqkR7mjG" # Zoya (Option 3)
CLONE_VOICE_ID = "fG9s0SXJb213f4UxVHyG" # Secondary Voice

def generate_audio(text, voice_id):
    """ElevenLabs se text-to-speech generate karne ke liye"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"Error: {e}")
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Option 3 Introduction Script (Zoya)
    intro_text = "Finally! Aapne Sakib ke sabse Dangerous bot ko jagaya hai. Main Zoya hoon, aur meri speciality hai voice cloning. Main itni perfect hoon ki asli aur nakli ka farq mita sakti hoon. Chaliye, apni audio bhejiye aur mera magic dekhiye."
    
    bot.send_chat_action(message.chat.id, 'upload_voice')
    audio_content = generate_audio(intro_text, INTRO_VOICE_ID)
    
    if audio_content:
        # Zoya ki voice mein intro bhejna
        bot.send_voice(message.chat.id, audio_content, caption="🎙️ **Zoya Mode Activated!**")
    
    bot.send_message(message.chat.id, "Main online hoon! Ab aap koi bhi text likhiye ya audio bhejkar mera magic dekhiye. 🔥")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Text ko Voice ID 2 mein badalne ke liye"""
    bot.send_chat_action(message.chat.id, 'upload_voice')
    audio = generate_audio(message.text, CLONE_VOICE_ID)
    if audio:
        bot.send_voice(message.chat.id, audio)

bot.polling()

