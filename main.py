import os
import random
import threading
from flask import Flask
import telebot
from telebot import types
import google.generativeai as genai

# 1. CONFIGURATION DU SERVEUR WEB POUR RENDER
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Lancement du serveur en arrière-plan
threading.Thread(target=run_server, daemon=True).start()

# 2. CONFIGURATION DES CLES
JETON = "8984219272:AAFEoPVU4hfDiLggSL3dYUEsWSuztTNA3ic"
Cle_API_GEMINI = "AQ.Ab8RN6KEosy9rItekKax1PQNlyYToLYF5llm68Gmu38L1u-rzQ"

bot = telebot.TeleBot(JETON)
genai.configure(api_key=Cle_API_GEMINI)
modele = genai.GenerativeModel('gemini-1.5-flash')

# 3. FONCTION DE PREDICTION FOOTBALL
def analyse_generique_ia(correspondre):
    prob_dom = random.randint(40, 65)
    prob_ext = random.randint(20, 35)
    prob_nul = 100 - (prob_dom + prob_ext)
    
    texte = f"🤖 *WEASBOY IA PRO*\n\nMatch : *{correspondre}*\n📊 Victoire Domicile : {prob_dom}%\n📊 Victoire Extérieur : {prob_ext}%\n📊 Match Nul : {prob_nul}%"
    return texte

# 4. COMMANDES DU BOT
@bot.message_handler(commands=["commencer"])
def envoyer_bienvenue(message):
    marge = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bouton = types.KeyboardButton("🏆 Matchs de la Coupe du Monde")
    marge.add(bouton)
    bot.send_message(
        message.chat.id,
        "🔥 WEASBOY ALL TIME EN LIGNE !\nPose-moi n'importe quelle question.",
        reply_markup=marge
    )

# 5. GESTION DES MESSAGES
@bot.message_handler(func=lambda message: True)
def gerer_messages(message):
    if message.text == "🏆 Matchs de la Coupe du Monde":
        matchs = ["Portugal - Croatie", "Suisse - Algérie"]
        for m in matchs:
            analyser = analyse_generique_ia(m)
            bot.send_message(message.chat.id, analyser, parse_mode="Markdown")
    else:
        try:
            reponse = modele.generate_content(message.text)
            bot.send_message(message.chat.id, reponse.text)
        except Exception as e:
            bot.send_message(message.chat.id, "Désolé, j'ai rencontré une erreur.")

# LANCEMENT DU BOT TELEGRAM
if __name__ == "__main__":
    bot.polling(none_stop=True)
