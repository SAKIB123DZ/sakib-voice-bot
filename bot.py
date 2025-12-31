
import telebot
import requests
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = '8466199285:AAG5dz2C3mGyTKb4mdJRq0k5ohebgVYqL6I'
ELEVENLABS_API_KEY = 'sk_536986633d540dde2144d20e0205b890e5b5be37c33ddec5'

bot = telebot.TeleBot(API_TOKEN)
user_voice_pref = {}

# Aapki chaaro Voice IDs yahan set hain
VOICES = {
    "Zoya (Intro/Cute)": "aE6av5ff68FOJqkR7mjG",
    "Voice 2 (Deep)": "fG9s0SXJb213f4UxVHyG",
    "Voice 3 (Young)": "mg9npuuaf8WJphS6E0Rt",
    "Voice 4 (Clear)": "jUjRbhZWoMK4aDciW36V"
}

def generate_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content
    except:
        pass
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Option 3 Introduction
    intro_text = "Finally! Aapne Sakib ke sabse Dangerous bot ko jagaya hai. Main Zoya hoon, aur meri speciality hai voice cloning. Main itni perfect hoon ki asli aur nakli ka farq mita sakti hoon. Chaliye, apni audio bhejiye aur mera magic dekhiye."
    
    bot.send_chat_action(message.chat.id, 'upload_voice')
    # Intro humesha Zoya ki voice mein jayega
    audio = generate_audio(intro_text, VOICES["Zoya (Intro/Cute)"])
    
    if audio:
        bot.send_voice(message.chat.id, audio, caption="🎙️ Zoya Mode On!")

    # Reply Markup with 4 Buttons
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [types.KeyboardButton(name) for name in VOICES.keys()]
    markup.add(*btns)
    
    bot.send_message(message.chat.id, "Niche buttons se voice select karein aur phir kuch bhi likhen, main audio bana kar dungi:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in VOICES.keys())
def set_voice(m):
    user_voice_pref[m.chat.id] = VOICES[m.text]
    bot.send_message(m.chat.id, f"✅ Done! Ab main {m.text} ki awaaz mein bolungi. Kuch bhi likh kar bhejiye!")

@bot.message_handler(func=lambda m: True)
def handle_all_messages(m):
    # Handle text to speech
    v_id = user_voice_pref.get(m.chat.id, VOICES["Zoya (Intro/Cute)"])
    bot.send_chat_action(m.chat.id, 'upload_voice')
    audio = generate_audio(m.text, v_id)
    if audio:
        bot.send_voice(m.chat.id, audio)
    else:
        bot.send_message(m.chat.id, "❌ Error: Audio nahi ban saki. Voice ID check karein.")

bot.polling()



