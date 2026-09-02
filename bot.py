import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN غير موجود!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"مرحباً {user.mention_html()}! 👋\n"
        f"أنا بوت Daoud الذكي! 🤖\n"
        f"اكتب /help لرؤية الأوامر",
        parse_mode="HTML"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🔧 **الأوامر المتاحة:**

/start - ابدأ هنا
/help - المساعدة
/info - معلومات البوت
/test - اختبر البوت
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = """
ℹ️ **معلومات البوت:**

📌 الاسم: Daoud Bot
🔧 الإصدار: 1.0.0
⚡ الحالة: يعمل بكفاءة
"""
    await update.message.reply_text(info_text, parse_mode="Markdown")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل بشكل طبيعي!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logger.info(f"رسالة من {update.effective_user.username}: {user_text}")
    
    await update.message.reply_text(
        f"📨 استقبلت رسالتك: `{user_text}`",
        parse_mode="Markdown"
    )

async def error_handler(update, context):
    logger.error(f"خطأ: {context.error}")

def main():
    logger.info("🤖 بدء تشغيل البوت...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("test", test_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.add_error_handler(error_handler)
    
    logger.info("✅ البوت جاهز!")
    app.run_polling()

if __name__ == '__main__':
    main()