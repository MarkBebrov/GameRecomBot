import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from games_recommender import get_recommendations, nn, games_df


# Токен бота
TOKEN = "6037600711:AAFdOcEf5s2QXn_fWB3M-IOhw8PRWM4m7Mg"

# Создаем экземпляр класса Updater и передаем ему токен бота
updater = Updater(TOKEN)

# Получаем ссылку на диспетчер сообщений бота
dispatcher = updater.dispatcher

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который рекомендует игры. Введите название игры, и я найду похожие игры для вас.')

# Обработчик сообщений пользователя
def recommend(update: Update, context: CallbackContext) -> None:
    game_title = update.message.text

    try:
        recommended_games = get_recommendations(game_title, nn, games_df)
    except Exception as e:
        logging.exception(e)
        update.message.reply_text("Что-то пошло не так. Пожалуйста, повторите запрос.")
        return

    if isinstance(recommended_games, str):
        update.message.reply_text(recommended_games)
    else:
        update.message.reply_text('\n'.join(recommended_games))

# Добавляем обработчик команды /start
dispatcher.add_handler(CommandHandler("start", start))

# Добавляем обработчик сообщений пользователя
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, recommend))

# Запускаем бота
updater.start_polling()
updater.idle()
