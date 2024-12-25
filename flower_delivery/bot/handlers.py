from telegram import Update
from telegram.ext import ContextTypes

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Этот бот поможет вам с доставкой цветов.")

# Уведомление о новом заказе
async def order_notification(order_id):
    # Замените YOUR_CHAT_ID на ID чата, куда нужно отправлять уведомления
    YOUR_CHAT_ID = "551378516"
    bot = context.bot
    await bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text=f"Новый заказ: #{order_id}"
    )

