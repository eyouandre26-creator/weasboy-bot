import os
import random
import threading
import flask
from flask import Flask
import telebot
from telebot import types
import google.generativeai as genai

# 1. CONFIGURATION DU SERVEUR WEB POUR RENDER
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 2. CONFIGURATION DES CLES
JETON = "8984219272:AAEo7H0UFgw2I3ZejSqn2eBef8-wDu2N1_Y"
Cle_API_GEMINI = "AQ.Ab8RN6KEosy9rItekKaxlPQNlYyTOLyF5Llm68Gmu38L1u-rzQ"

bot = telebot.TeleBot(JETON)
genai.configure(api_key=Cle_API_GEMINI)

# CONFIGURATION DE L'IA POUR QU'ELLE RECONNAISSE SON CRÉATEUR
instructions_ia = (
    "Tu es WEASBOY IA PRO, une intelligence artificielle puissante et un expert en pronostics football. "
    "Tu as été créé par le grand créateur, artiste et producteur EYOU André (connu sous le nom de WEASBOY). "
    "Si on te demande qui t'a créé, tu dois répondre avec enthousiasme et respect que ton créateur est EYOU André / WEASBOY. "
    "Sois toujours pro, dynamique, amical et utilise des émojis."
)
modele = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instructions_ia)

# 3. FONCTION DE PREDICTION FOOTBALL
def analyse_generique_ia(correspondre):
    prob_dom = random.randint(40, 65)
    prob_ext = random.randint(20, 35)
    prob_nul = 100 - (prob_dom + prob_ext)
    
    texte = f"🤖 *WEASBOY IA PRO*\n\nMatch : *{correspondre}*\n📊 Victoire Domicile : {prob_dom}%\n📊 Victoire Extérieur : {prob_ext}%\n📊 Match Nul : {prob_nul}%"
    return texte

# 4. COMMANDES ET MENU DU BOT
@bot.message_handler(commands=["commencer", "start"])
def envoyer_bienvenue(message):
    # Création du menu avec plusieurs fonctionnalités à disposition
    marge = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    bouton_prono = types.KeyboardButton("📊 Analyses & Pronos")
    bouton_ia = types.KeyboardButton("🧠 Discuter avec l'IA")
    bouton_createur = types.KeyboardButton("🔥 Zone WEASBOY")
    
    marge.add(bouton_prono, bouton_ia, bouton_createur)
    
    bot.send_message(
        message.chat.id,
        "🔥 *WEASBOY ALL TIME EN LIGNE !*\n\nBienvenue sur ton espace de contrôle. Choisis une fonctionnalité ci-dessous ou pose-moi une question directement !",
        reply_markup=marge,
        parse_mode="Markdown"
    )

# 5. GESTION DES MESSAGES ET DES BOUTONS
@bot.message_handler(func=lambda message: True)
def gerer_messages(message):
    if message.text == "📊 Analyses & Pronos":
        matchs = ["Portugal - Croatie", "Suisse - Algérie"]
        bot.send_message(message.chat.id, "⚽ *Génération des analyses en cours...*", parse_mode="Markdown")
        for m in matchs:
            analyser = analyse_generique_ia(m)
            bot.send_message(message.chat.id, analyser, parse_mode="Markdown")
            
    elif message.text == "🧠 Discuter avec l'IA":
        bot.send_message(
            message.chat.id, 
            "🧠 *Mode IA activé !* Pose-moi n'importe quelle question sur le foot, la musique, ou ce que tu veux, et je te répondrai."
        )
        
    elif message.text == "🔥 Zone WEASBOY":
        texte_createur = (
            "👑 *MON CRÉATEUR* 👑\n\n"
            "Ce robot a été entièrement conçu et développé par **EYOU André** (alias **WEASBOY**).\n\n"
            "Restez connectés, du très lourd arrive pour la marque et la production de contenus ! 🚀"
        )
        bot.send_message(message.chat.id, texte_createur, parse_mode="Markdown")
        
    else:
        # L'utilisateur discute directement avec l'IA
        try:
            reponse = modele.generate_content(message.text)
            bot.send_message(message.chat.id, reponse.text)
        except Exception as e:
            bot.send_message(message.chat.id, "Désolé, j'ai rencontré une erreur.")

# Lancement du bot Telegram dans un thread séparé pour laisser Gunicorn gérer Flask
def run_bot():
    bot.polling(none_stop=True)

threading.Thread(target=run_bot, daemon=True).start()

# Requis pour que Gunicorn puisse trouver l'application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
