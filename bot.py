
      import telebot, requests
import os

# --- AAPKI SETTINGS MAINE SET KAR DI HAIN ---
API_TOKEN = "8466199285:AAG5dz2C3mGyTKb4mdJRq0k5ohebgVYqL6I" 
ELEVENLABS_KEY = "sk_91ee4759fdca5fb2dbe6425b840cb4d4a4cd13fe6679e219"
VOICE_ID = "mg9npuuaf8WJphS6E0Rt" 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Sakib Permanent Bot Active hai! Voice ID: mg9npuuaf8WJphS6E0Rt")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
        data = {
            "text": message.text, 
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("reply.mp3", "wb") as f:
                f.write(response.content)
            bot.send_voice(message.chat.id, open("reply.mp3", "rb"))
    except Exception as e:
        print(f"Error: {e}")

bot.polling()
