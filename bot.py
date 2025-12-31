import telebot
import requests
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = '8466199285:AAG5dz2C3mGyTKb4mdJRq0k5ohebgVYqL6I'
ELEVENLABS_API_KEY = 'sk_536986633d540dde2144d20e0205b890e5b5be37c33ddec5' # Nayi Key

bot = telebot.TeleBot(API_TOKEN)

# User ki pasand yaad rakhne ke liye dictionary
user_voice_pref = {}

# Voice IDs
VOICES = {
    "Zoya (Cute/Intro)": "aE6av5ff68FOJqkR7mjG",
    "Ananya (Deep/Calm)": "fG9s0SXJb213f4UxVHyG",
    "Priya (Young/Sweet)": "Lcf7z35Z7pM67S2Ag7uL" # Ek aur extra cute voice add ki hai
}

def generate_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=data, headers=headers)
    return response.content if response.status_code == 200 else None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Option 3 Intro Script
    intro_text = "Finally! Aapne Sakib ke sabse Dangerous bot ko jagaya hai. Main Zoya hoon, aur meri speciality hai voice cloning. Main itni perfect hoon ki asli aur nakli ka farq mita sakti hoon. Chaliye, apni audio bhejiye aur mera magic dekhiye."
    
    bot.send_chat_action(message.chat.id, 'upload_voice')
    audio = generate_audio(intro_text, VOICES["Zoya (Cute/Intro)"])
    
    if audio:
        bot.send_voice(message.chat.id, audio, caption="🎙️ Zoya Mode On!")
    
    # Buttons dikhana taaki user voice select kare
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [types.KeyboardButton(name) for name in VOICES.keys()]
    markup.add(*btns)
    
    bot.send_message(message.chat.id, "Niche diye gaye buttons se voice select karein aur phir kuch bhi likhen ya audio bhejen:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in VOICES.keys())
def set_voice(message):
    user_voice_pref[message.chat.id] = VOICES[message.text]
    bot.reply_to(message, f"✅ Ab main {message.text} ki awaaz mein bolungi!")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Agar user ne voice select nahi ki, toh Zoya default rahegi
    v_id = user_voice_pref.get(message.chat.id, VOICES["Zoya (Cute/Intro)"])
    
    bot.send_chat_action(message.chat.id, 'upload_voice')
    audio = generate_audio(message.text, v_id)
    if audio:
        bot.send_voice(message.chat.id, audio)

bot.polling()


