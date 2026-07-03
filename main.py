import http.server
import socketserver
import threading

def run_fake_server():
    PORT = 10000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()
import random
import telebot
from telebot import types

TOKEN = "8984219272:AAFEoPVU4hfDiLggSL3dYUEswSUztTNA3ic"
bot = telebot.TeleBot(TOKEN)


def generer_analyse_ia(match):
    prob_dom = random.randint(40, 65)
    prob_ext = random.randint(20, 35)
    prob_nul = 100 - (prob_dom + prob_ext)

    texte = f"🤖 *WEASBOY IA PRO*\n🆚 Match : *{match}*\n📊 Victoire : {prob_dom}% | Nul : {prob_nul}% | Défaite : {prob_ext}%\n🎯 *Pronostic conseillé :* Victoire Domicile ou Nul\n⚽ *Score Exact chaud :* 2-1 ou 1-1"
    return texte


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = types.KeyboardButton("🏆 Matchs de la Coupe du Monde")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "🔥 WEASBOY ALL-TIME EN LIGNE !",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "🏆 Matchs de la Coupe du Monde":
        matchs = ["Portugal - Croatie", "Suisse - Algérie"]
        for m in matchs:
            bot.send_message(
                message.chat.id, generer_analyse_ia(m), parse_mode="Markdown"
            )


print("Robot actif...")
bot.infinity_polling()
