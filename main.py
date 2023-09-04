import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from function import add_expense, delete_expense, view_expenses, generate_summary
from credential import AUTH_USERS

# Define handler functions for the commands
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Expense Manager Bot! Type /help to see the list of commands.")

def help(update, context):
    help_text = "Here are the available commands:\n"
    help_text += "/add [Category] [Month] [Expense] - Add expense to a category for a particular month.\n"
    help_text += "/delete [Category] [Month] [Expense] - Delete expense from a category for a particular month.\n"
    help_text += "/view [Month] - View expenses for a particular month.\n"
    help_text += "/summary [Month] - Generate summary for a particular month.\n"
    help_text += "/summary [from date (ddmmyy)] [to date (ddmmyy)] - Generate summary for a date range.\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def add(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    try:
        result = add_expense(text)
        context.bot.send_message(chat_id=chat_id, text=result)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=str(e))

def delete(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    try:
        result = delete_expense(text)
        context.bot.send_message(chat_id=chat_id, text=result)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=str(e))

def view(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    try:
        result = view_expenses(text)
        context.bot.send_message(chat_id=chat_id, text=result, parse_mode='MarkdownV2')
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=str(e))

def summary(update, context):
    text = update.message.text
    chat_id = update.effective_chat.id
    try:
        result = generate_summary(text)
        if result is None:
            context.bot.send_message(chat_id=chat_id, text="No expenses found for the given month/range.")
        else:
            context.bot.send_photo(chat_id=chat_id, photo=open('summary.png', 'rb'))
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=str(e))

def unauthorized_access(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to access this bot.")

if __name__ == '__main__':
    # Set up the bot
    updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers for the commands
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    add_handler = CommandHandler('add', add)
    delete_handler = CommandHandler('delete', delete)
    view_handler = CommandHandler('view', view)
    summary_handler = CommandHandler('summary', summary)

    # Add handlers to the dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(add_handler)
    dispatcher.add_handler(delete_handler)
