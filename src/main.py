import os
import logging
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
from canvasapi import Canvas
from datetime import datetime, timezone

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CANVAS_URL = os.getenv('CANVAS_URL')
CANVAS_TOKEN = os.getenv('CANVAS_API')
canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)

def get_current_term_id():
    """
    Fetches all terms from Canvas and returns the ID of the term
    that includes today's date (i.e., the current semester).
    """
    try:
        terms = canvas.get_account(1).get_terms()
        now = datetime.now(timezone.utc)
        for term in terms['enrollment_terms']:
            start = datetime.fromisoformat(term['start_at'].replace('Z', '+00:00')) if term['start_at'] else None
            end = datetime.fromisoformat(term['end_at'].replace('Z', '+00:00')) if term['end_at'] else None
            if start and end and start <= now <= end:
                return term['id']
    except Exception as e:
        logger.error(f"Error fetching terms: {e}")
    return None

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("⚠️ An unexpected error occurred. Please try again later.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome_message = f"""
Hi {user.first_name} Welcome to your Telegram Bot!

To see the list of commands that are available, please use the /help command.
    """

    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = """
These are the list of commands you can use:
/start - Welcome message
/help - Show the help message
/info - Show the bot information
/course - Show the list of currently enrolled courses
    """

    await update.message.reply_text(help_message)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    info_message = f"""
**BOT INFORMATION**
• Framework: python-telegram-bot
• Version: 20.7
• Status: ✅ Active

**CHAT DETAILS**
• Chat Type: {chat.type}
• Chat ID: {chat.id}

**USER DETAILS**
• User ID: {user.id}
• Username: {user.username}
• First Name: {user.first_name}
• Last Name: {user.last_name}
• Is Bot: {user.is_bot}
    """

    await update.message.reply_text(info_message)

async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def course_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        courses = canvas.get_courses(enrollment_state="active")
        course_list = [course for course in courses if hasattr(course, "name") and course.name]

        if not course_list:
            message = "You are not currently enrolled in any courses for this semester."
        else:
            message = f"**Courses you are currently enrolled in, {user.first_name}**\n"
            for course in course_list:
                message += f"• {course.name}\n"

        await update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in /course: {e}")
        await update.message.reply_text("⚠️ Could not fetch your courses. Please try again later.")

    except Exception as e:
        logger.error(f"Error fetching courses: {e}")
        await update.message.reply_text("An error occurred while fetching your courses. Please try again later.")

def main():
    application = Application.builder().token(os.getenv('TELEGRAM_KEY')).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("course", course_command))
    application.add_handler(CommandHandler("remind", remind_command))

    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()