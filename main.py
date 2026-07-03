import http.server
import socketserver
import threading
import random
import telebot
from telebot import types
import google.generativeai as genai

# 1. FAUX SERVEUR POUR RENDER
def run_fake_server():
    PORT = 10000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# 2. CONFIGURATION DES CLÉS
TOKEN = "8984219272:AAFEoPVU4hfDiLggSL3dYUEswSUztTNA3ic"
GEMINI_API_KEY = "AQ.Ab8RN6KEosy9rItekKaxlPQNlYyTOLyF5Llm68Gmu38L1u-rzQ"

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. FONCTION DE PRÉDICTION FOOTBALL
def generer_analyse_ia(match):
    prob_dom = random.randint(40, 65)
    prob_ext = random.randint(20, 35)
    prob_nul = 100 - (prob_dom + prob_ext)
    
    texte = f"🤖 *WEASBOY IA PRO*\nMatch : *{match}*\n📊 Victoire Dom: {prob_dom}% | Nul: {prob_nul}% | Victoire Ext: {prob_ext}%"
    return texte

# 4. COMMANDES DU BOT
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = types.KeyboardButton("🏆 Matchs de la Coupe du Monde")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "🔥 WEASBOY ALL-TIME EN LIGNE !\nPose-moi n'importe quelle question ou clique sur le bouton en bas.",
        reply_markup=markup,
    )

# 5. GESTION DES MESSAGES
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "🏆 Matchs de la Coupe du Monde":
        matchs = ["Portugal - Croatie", "Suisse - Algérie"]
        for m in matchs:
            analyse = generer_analyse_ia(m)
            bot.send_message(message.chat.id, analyse, parse_mode="Markdown")
    else:
        try:
            response = model.generate_content(message.text)
            bot.send_message(message.chat.id, response.text)
        except Exception as e:
            bot.send_message(message.chat.id, "Désolé, j'ai un petit problème pour réfléchir... 🤖")

# LANCEMENT DU BOT
bot.polling(none_stop=True)
