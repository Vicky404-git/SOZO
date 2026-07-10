import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sozo.core.services import log_natural_event, show_today
from sozo.cli.utils import format_today_events  # Reuse your clean text formatters!

# Load token from your existing environment setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_USER_ID", 0)) # Secure it so only YOU can log to your PC

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    await update.message.reply_text("🌌 Sōzō Bridge active. Send me anything to log it via AI.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    
    raw_text = update.message.text
    await update.message.reply_chat_action("typing")
    
    try:
        # Pass directly into your existing AI parser logic!
        category, value, final_tags = log_natural_event(raw_text)
        tag_str = " ".join([f"#{t}" for t in final_tags])
        
        reply = f"✔ **Saved to Timeline:**\n📁 {category.upper()} → {value}\n🏷 {tag_str}"
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"✖ Error parsing log: {e}")

async def handle_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    # Reuse your existing database service & presentation layer formatting!
    events = show_today()
    clean_output = format_today_events(events)
    await update.message.reply_text(f"📅 **Today's Actions:**\n\n{clean_output}")

def start_bridge():
    if not TELEGRAM_BOT_TOKEN:
        print("[red]Missing TELEGRAM_BOT_TOKEN in .env[/red]")
        return
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", handle_today))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("📲 Sōzō Telegram Bridge listening via long polling...")
    app.run_polling()
