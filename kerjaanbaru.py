import logging
import time
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= CONFIG FROM ENV =================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BROADCAST_CHAT_ID = os.getenv("BROADCAST_CHAT_ID")

# Pastikan variabel wajib ada
if not TOKEN:
    raise ValueError("Error: TELEGRAM_BOT_TOKEN belum di-set di Railway!")

if not BROADCAST_CHAT_ID:
    raise ValueError("Error: BROADCAST_CHAT_ID belum di-set di Railway!")

BROADCAST_CHAT_ID = int(BROADCAST_CHAT_ID)

LOGIN_LINK = "https://shortq.info/bolapelangi2"
TOURNAMENT_LINK = "https://shortq.info/event-bolapelangi2"
ADMIN_LINK = "https://bopel2.link/wa"

# ==========================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ========= BUTTON MENU /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🔗 LOGIN", url=LOGIN_LINK)],
        [InlineKeyboardButton("🏆 Info Tournament", url=TOURNAMENT_LINK)],
        [InlineKeyboardButton("📞 Hubungi Admin", url=ADMIN_LINK)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Selamat datang di *BOLAPELANGI2 Bot* 🎉\n\nSilakan pilih menu:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


# ============= AUTO BROADCAST PER JAM ==============
async def auto_broadcast(application: Application):

    try:
        await application.bot.send_message(
            chat_id=BROADCAST_CHAT_ID,
            text=(
                "⏰ *Informasi Berkala*\n"
                "Jangan lupa cek tournament & prediksi harian!\n\n"
                f"🔗 Login: {LOGIN_LINK}\n"
                f"🏆 Event: {TOURNAMENT_LINK}"
            ),
            parse_mode="Markdown"
        )
        logger.info("Broadcast 1 jam terkirim.")
    except Exception as e:
        logger.error(f"Broadcast gagal: {e}")


# ============= BOT LOOP FOREVER =============
async def main_loop():
    application = Application.builder().token(TOKEN).build()

    # COMMAND HANDLERS
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    # Start bot polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # LOOP BROADCAST SETIAP 1 JAM
    while True:
        await auto_broadcast(application)
        time.sleep(3600)  # 1 jam


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_loop())
