import telebot
import requests
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = '8466199285:AAG5dz2C3mGyTKb4mdJRq0k5ohebgVYqL6I'
ELEVENLABS_API_KEY = 'sk_536986633d540dde2144d20e0205b890e5b5be37c33ddec5'

bot = telebot.TeleBot(API_TOKEN)

# User ki pasand yaad rakhne ke liye
user_voice_pref = {}

# Voice IDs (Inme se Anjali sabse cute hai)
VOICES = {
    "Zoya (Intro Voice)": "aE6av5ff68FOJqkR7mjG",
    "Anjali (Cute/Young)": "ThT5KcBe7VKqW9ut7Rlb", 
    "Priya (Sweet)": "Lcf7z35Z7pM67S2Ag7uL"
}

def generate_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.content
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    intro_text = "Finally! Aapne Sakib ke sabse Dangerous bot ko jagaya hai. Main Zoya hoon, aur meri speciality hai voice cloning. Main itni perfect hoon ki asli aur nakli ka farq mita sakti hoon. Chaliye, apni audio bhejiye aur mera magic dekhiye."
    
    bot.send_chat_action(message.chat.id, 'upload_voice')
    audio = generate_audio(intro_text, VOICES["Zoya (Intro Voice)"])
    
    if audio:
        bot.send_voice(message.chat.id, audio, caption="🎙️ Zoya Mode On!")
    
    # Buttons for selection
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [types.KeyboardButton(name) for name in VOICES.keys()]
    markup.add(*btns)
    
    bot.send_message(message.chat.id, "Niche buttons se voice select karein aur phir kuch bhi likhen, main audio bana kar dungi:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in VOICES.keys())
def set_voice(message):
    user_voice_pref[message.chat.id] = VOICES[message.text]
    bot.send_message(message.chat.id, f"✅ Done! Ab main {message.text} ki awaaz mein bolungi. Kuch bhi likh kar bhejiye!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Agar user ne command ya button nahi dabaya, toh ye text to speech karega
    if message.text in VOICES.keys():
        return

    v_id = user_voice_pref.get(message.chat.id, VOICES["Zoya (Intro Voice)"])
    
    bot.send_chat_action(message.chat.id, 'upload_voice')
    audio = generate_audio(message.text, v_id)
    
    if audio:
        bot.send_voice(message.chat.id, audio)
    else:
        bot.send_message(message.chat.id, "❌ Error: Audio generate nahi ho saki. API limit check karein.")

bot.polling()



