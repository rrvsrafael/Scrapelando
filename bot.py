from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from src.pelando_crawler import scrape_pelando
from src.utils import validate_search_term, validate_min_score
from dotenv import load_dotenv
import os


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send a message with the format:\n`search_term min_score`\nExample: `bike 50`"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Parse user message
        user_input = update.message.text.rsplit(None, 1)
        search_term = validate_search_term(user_input[0])
        min_score = (
            validate_min_score(int(user_input[1])) if len(user_input) == 2 else 100
        )

        results = scrape_pelando(search_term, min_score)

        # Send results
        if results:
            await update.message.reply_text("\n\n".join(results))
        else:
            await update.message.reply_text("No deals found matching your criteria.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


def main():
    load_dotenv()
    BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
    if BOT_API_TOKEN is None:
        raise ValueError("BOT_API_TOKEN not found in environment variables")

    app = ApplicationBuilder().token(BOT_API_TOKEN).build()

    # Define commands and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
    print("Bot is running...")


if __name__ == "__main__":
    main()
