from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from flask import Flask
import asyncio
import schedule
import time
from threading import Thread
from datetime import datetime, timedelta

BOT_TOKEN = "8062761924:AAGcLjqxM2WL48N-pVw8tynhlCuH1D4_snY"
CHAT_ID = "-1002877323438"

# Mensaje bienvenida a nuevos integrantes
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for miembro in update.message.new_chat_members:
        nombre = miembro.first_name
        mensaje = (
            f"👋 *¡Bienvenido/a, {nombre}, a la comunidad P.1🦁!*\n\n"
            "Recuerda revisar los mensajes anclados donde encontrarás:\n"
            "- Las reglas del grupo\n"
            "- El significado de P.1🦁\n"
            "- Un mensaje prediseñado que puedes usar para invitar a otros\n\n"
            "*Unidos somos más, y más fuertes* 💪🔥"
        )
        botones = InlineKeyboardMarkup([
            [InlineKeyboardButton("📜 Ver reglas", url="https://t.me/c/2877323438/73")],
            [InlineKeyboardButton("🦁 ¿Qué es P.1?", url="https://t.me/c/2877323438/75")],
            [InlineKeyboardButton("📅 Agendar batalla", url="https://forms.gle/KFMDU69wxav9KvBb6")]
        ])
        await context.bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown", reply_markup=botones)

# Mensaje diario de buenos días
async def buenos_dias(context: ContextTypes.DEFAULT_TYPE):
    fecha = datetime.utcnow() - timedelta(hours=5)
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    mensaje = (
        f"🌞 *¡Muy buenos días, familia P.1🦁!*\n\n"
        f"🗓️ Hoy es *{dias[fecha.weekday()]} {fecha.day} de {meses[fecha.month - 1]} de {fecha.year}*.\n\n"
        "Iniciamos un nuevo día con la energía y el compromiso de seguir creciendo juntos 💫.\n"
        "Recuerda que aquí estamos para *apoyarnos, impulsarnos y lograr cada meta que nos propongamos* 💪🚀.\n\n"
        "📣 *¡Invita a más personas a unirse!* Cuantos más seamos, más fuerte será nuestra comunidad 🔥🙌.\n\n"
        "🎯 *¿Tienes una batalla, live o evento planificado?* Compártelo con anticipación para agregarlo a los recordatorios automáticos ⏰.\n"
        "📝 Puedes usar este formulario para agendarlo fácilmente:\n"
        "👉 https://forms.gle/KFMDU69wxav9KvBb6\n\n"
        "*¡Estamos aquí para respaldarte!*\n\n"
        "💥✨ *¡A darlo todo hoy!*"
    )
    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Ver reglas", url="https://t.me/c/2877323438/73"),
         InlineKeyboardButton("🦁 ¿Qué es P.1?", url="https://t.me/c/2877323438/75"),
         InlineKeyboardButton("📅 Agendar batalla", url="https://forms.gle/KFMDU69wxav9KvBb6")]
    ])
    await context.bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown", reply_markup=botones)

# Flask app para mantener vivo el bot
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot activo ✅"

Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# Main del bot
async def main():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))

    def job():
        app_bot.create_task(buenos_dias(app_bot.bot))

    schedule.every().day.at("12:00").do(job)

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(10)

    Thread(target=run_schedule, daemon=True).start()
    await app_bot.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
