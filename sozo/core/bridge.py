import os
import asyncio
from sozo.core.runtime import VAULT_PATH
import html
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import your core Sōzō services
from sozo.core.services import log_natural_event, show_today, list_events, get_stats, search_events
from sozo.cli.utils import extract_date 

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_USER_ID", 0))

def start_bridge():
    if not TELEGRAM_BOT_TOKEN:
        print("[red]Missing TELEGRAM_BOT_TOKEN in .env[/red]")
        return
    
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .build()
    )
    

# --- COMMAND HANDLERS ---

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    await update.message.reply_text("🌌 Sōzō Bridge active. Type /help to see commands.")

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    help_text = """
🌌 *Sōzō Bot Commands*
/today - View today's events
/logs - View your 15 most recent logs
/stats - View activity statistics
/search <query> - Search your timeline
/help - Show this menu

*Natural Language Logging:*
Just type a sentence to log an event via AI.
_Example: Just spent 2 hours debugging Python #programming_
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def handle_read(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a note name to read. \nUsage: /read projects")
        return
        
    from sozo.core.runtime import VAULT_PATH
    found = list(VAULT_PATH.rglob(f"*{query}*.md"))
    
    if not found:
        await update.message.reply_text(f"✖ Could not find any note matching '{query}'.")
        return
        
    filepath = found[0]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        reply_header = f"📄 Reading: {filepath.name}\n{'-'*30}\n"
        full_text = reply_header + content
        
        # Telegram limit is 4096. We slice at 4000 to be perfectly safe.
        chunk_size = 4000
        chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
        
        # Send each chunk as a separate message
        for i, chunk in enumerate(chunks):
            await update.message.reply_text(chunk)
            
            # If there's more than one chunk, pause for half a second to prevent rate-limiting
            if i < len(chunks) - 1:
                await asyncio.sleep(0.5) 
                
    except Exception as e:
        await update.message.reply_text(f"✖ Error reading note: {e}")

async def handle_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    events = show_today()
    if not events:
        await update.message.reply_text("No events logged today.")
        return
    
    reply = "📅 <b>Today's Actions:</b>\n\n"
    for e in events:
        # html.escape prevents crash if your log contains < or >
        safe_value = html.escape(e[3])
        reply += f"• <b>{e[2].capitalize()}</b> → {safe_value}\n"
    await update.message.reply_text(reply, parse_mode="HTML")

async def handle_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    events = list_events()[-15:] 
    if not events:
        await update.message.reply_text("No events found in the timeline.")
        return
    
    reply = "🕒 <b>Recent Logs:</b>\n\n"
    for e in events:
        date_str = extract_date(e[1])
        safe_value = html.escape(e[3])
        reply += f"• <code>{date_str}</code>: <b>{e[2].capitalize()}</b> → {safe_value}\n"
    await update.message.reply_text(reply, parse_mode="HTML")

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a search term. \nUsage: /search python")
        return
    
    events = search_events(query)[:10]
    if not events:
        await update.message.reply_text(f"No results found for '{query}'.")
        return
        
    safe_query = html.escape(query)
    reply = f"🔍 <b>Search Results for '{safe_query}':</b>\n\n"
    for e in events:
        date_str = extract_date(e[1])
        safe_value = html.escape(e[3])
        reply += f"• <code>{date_str}</code>: <b>{e[2].capitalize()}</b> → {safe_value}\n"
        
    await update.message.reply_text(reply, parse_mode="HTML")

async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    stats = get_stats()
    if not stats:
        await update.message.reply_text("No stats available yet.")
        return
    
    reply = "📊 *Activity Stats:*\n\n"
    for cat, count in stats:
        reply += f"• *{cat.capitalize()}*: {count} events\n"
    await update.message.reply_text(reply, parse_mode="Markdown")

# --- AI PARSER HANDLER ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID: return
    
    raw_text = update.message.text
    await update.message.reply_chat_action("typing")
    
    try:
        category, value, final_tags = log_natural_event(raw_text)
        tag_str = " ".join([f"#{t}" for t in final_tags]) if final_tags else ""
        
        reply = f"✔ *Saved to Timeline:*\n📁 {category.upper()} → {value}\n🏷 {tag_str}"
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"✖ Error parsing log: {e}")

# --- BOT LAUNCHER ---

def start_bridge():
    if not TELEGRAM_BOT_TOKEN:
        print("[red]Missing TELEGRAM_BOT_TOKEN in .env[/red]")
        return
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register the commands!
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("today", handle_today))
    app.add_handler(CommandHandler("logs", handle_logs))
    app.add_handler(CommandHandler("stats", handle_stats))
    app.add_handler(CommandHandler("search", handle_search))
    app.add_handler(CommandHandler("read", handle_read))
    
    # Keep this last: It catches normal text to run through the AI log
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("📲 Sōzō Telegram Bridge listening via long polling...")
    app.run_polling()
