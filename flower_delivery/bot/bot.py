from handlers import start, order_notification  # Импорт обработчиков
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes




# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Это бот для доставки цветов.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def main():
    TOKEN = "7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo"
    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск приложения
    application.run_polling()


if __name__ == "__main__":
    main()
