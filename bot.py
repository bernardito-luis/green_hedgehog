import logging
import datetime
import pytz

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

from limerick import compose_limerick
from settings import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log',
)
log = logging.getLogger()


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me ^_^"
             " I know some tricks (:"
             " Use /help to discover them",
    )


def limerick_handler(update: Update, context: CallbackContext) -> None:
    limerick = compose_limerick()
    context.bot.send_message(chat_id=update.effective_chat.id, text=limerick)


def callback_limerick(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context['chat_id'], text=compose_limerick())


def alakazam(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="✨")


def schedule_limericks(update: Update, context: CallbackContext) -> None:
    target_chat_id = update.effective_chat.id
    for job in context.job_queue.jobs():
        if job.context.get('chat_id') == target_chat_id:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Too much magic can cast charm-overflow!",
            )
            return

    context.bot.send_message(chat_id=update.effective_chat.id, text="✨")
    context.job_queue.run_daily(
        callback_limerick,
        days=(0, 2, 4),
        time=datetime.time(hour=18, minute=00, tzinfo=pytz.timezone('Europe/Moscow')),
        context={'chat_id': target_chat_id}
    )


def help_handler(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Commands available\n"
             "/start - Initial message with little info\n"
             "/alakazam - Casts some simple old spell, they say it brings fortune\n"
             "/limerick - Composes limerick\n"
             "/do_some_magic - ✨✨✨\n"
             "/help - This text\n"
    )


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('alakazam', alakazam))
    dispatcher.add_handler(CommandHandler('limerick', limerick_handler))
    dispatcher.add_handler(CommandHandler('do_some_magic', schedule_limericks))
    dispatcher.add_handler(CommandHandler('help', help_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
