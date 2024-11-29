from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен вашего бота
TOKEN = "8112472204:AAHVScXlre8vd01LC2gwHTtx8DbeYXsvFbI"

# Ваш Telegram ID
ADMIN_ID = 5240125096

# Словарь для хранения отзывов
feedbacks = []

# Функция стартового сообщения
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать! Вот, что я умею:\n"
        "1️⃣ Оставить анонимный отзыв: просто отправьте сообщение.\n"
        "2️⃣ Пройти опрос: отправьте команду /poll."
    )

# Обработка анонимных отзывов
async def anonymous_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global feedbacks
    feedback = update.message.text
    feedbacks.append(feedback)  # Сохраняем отзыв
    await update.message.reply_text("Ваш отзыв отправлен анонимно. Спасибо!")

    # Отправляем отзыв вам в личные сообщения
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"Новый анонимный отзыв: {feedback}")

# Функция для создания опроса
async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = ["Как вы оцениваете наш сервис?", "Хотите ли вы воспользоваться снова?"]
    options = [["Отлично", "Хорошо", "Удовлетворительно", "Плохо"], ["Да", "Нет"]]

    for i, question in enumerate(questions):
        await update.message.reply_poll(question, options[i])

# Основная функция
def main():
    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("poll", poll))

    # Обработка текстовых сообщений (анонимные отзывы)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anonymous_feedback))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
