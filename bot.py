import logging
import datetime
import random

import pytz

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

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


def callback_send_message(context: CallbackContext):
    context.bot.send_message(
        chat_id=context.job.context['chat_id'],
        text=context.job.context['text'],
    )


def sniff_handler(update: Update, context: CallbackContext) -> None:
    context.user_data['spell'] = 'sniff'


def snaff_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data['spell'] == 'sniff':
        context.user_data['spell'] += 'snaff'


def snure_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data['spell'] in ('sniffsnaff', 'sniffsnaffsnure'):
        context.user_data['spell'] += 'snure'


def bazilure_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data['spell'] == 'sniffsnaffsnuresnure':
        context.job_queue.run_once(
            callback_send_message,
            0,
            context={'chat_id': update.effective_chat.id, 'text': "✨"},
        )
        context.job_queue.run_once(
            callback_send_message,
            0.5,
            context={'chat_id': update.effective_chat.id, 'text': "💫"},
        )
        context.job_queue.run_once(
            callback_send_message,
            1,
            context={'chat_id': update.effective_chat.id, 'text': "✨"},
        )
        context.user_data['spell'] = ''


def all_clear(update: Update, context: CallbackContext):
    answer = random.choice((
        'понятно',
        'понятно-понятно',
        'понятно, чего ж тут непонятного',
        'фыр-фыр-фыр',
    ))
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('alakazam', alakazam))
    dispatcher.add_handler(CommandHandler('limerick', limerick_handler))
    dispatcher.add_handler(CommandHandler('do_some_magic', schedule_limericks))
    dispatcher.add_handler(CommandHandler('help', help_handler))

    all_clear_handler = MessageHandler(
        Filters.regex(r'(е|ё|Е|Ё)(ж|Ж).*понятно') & (~Filters.command),
        all_clear,
    )
    dispatcher.add_handler(all_clear_handler)

    # sniff-snaff-snure-snure-bazilure
    dispatcher.add_handler(CommandHandler('sniff', sniff_handler))
    dispatcher.add_handler(CommandHandler('snaff', snaff_handler))
    dispatcher.add_handler(CommandHandler('snure', snure_handler))
    dispatcher.add_handler(CommandHandler('bazilure', bazilure_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
