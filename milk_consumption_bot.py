import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd
import datetime
import os
import time

# Telegram bot token
BOT_TOKEN = 'BOT_TOKEN'

# Function to get the current date
def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

# Function to collect daily milk consumption
def collect_daily_consumption(context):
    message = "Enter the milk consumption in liters for today: "
    context.bot.send_message(chat_id=context.job.context.job_queue.chat_id, text=message)

# Function to handle user input
def handle_user_input(update, context):
    try:
        if 'rate_per_liter' not in context.user_data:
            context.user_data['rate_per_liter'] = float(update.message.text)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Rate per liter recorded.")
        else:
            consumption = float(update.message.text)
            context.user_data.setdefault('daily_consumption', []).append(consumption)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Daily milk consumption recorded.")
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid input. Please enter a numeric value.")

# Function to calculate monthly expense
def calculate_monthly_expense(daily_consumption, rate_per_liter):
    total_liters = sum(daily_consumption)
    expense = total_liters * rate_per_liter
    return expense

# Function to create an Excel sheet with expense breakdown
def create_expense_sheet(update, context, daily_consumption, rate_per_liter, expense):
    current_month = datetime.datetime.now().strftime("%B")
    filename = f"MILK_Expense_{current_month}.xlsx"

    data = {
        'Date': [get_current_date() for _ in range(len(daily_consumption))],
        'Consumption (liters)': daily_consumption,
        'Rate per Liter (INR)': [rate_per_liter for _ in range(len(daily_consumption))],
        'Expense (INR)': [rate_per_liter * consumption for consumption in daily_consumption]
    }

    # Add row for total expense and total consumption
    data['Date'].append("Total")
    data['Consumption (liters)'].append(sum(daily_consumption))
    data['Rate per Liter (INR)'].append('')
    data['Expense (INR)'].append(expense)

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

    # Send the file
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))

    # Delete the file after 1 hour
    time.sleep(3600)  # Wait for 1 hour
    os.remove(filename)

# Function to handle /start command
def start(update, context):
    menu_message = "Welcome! This bot will help you track your daily milk consumption.\n\n" \
                   "Available commands:\n" \
                   "/start - Start the bot and show this menu\n" \
                   "/totalbill - Calculate and share the total monthly expense\n" \
                   "/breakdown - Show the breakdown of monthly expense\n" \
                   "/setrate - Set the rate per liter for the calculation\n" \
                   "/cleardata - Clear all recorded data\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=menu_message)

# Function to handle /totalbill command
def total_bill(update, context):
    daily_consumption = context.user_data.get('daily_consumption', [])
    rate_per_liter = context.user_data.get('rate_per_liter')
    expense = calculate_monthly_expense(daily_consumption, rate_per_liter)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Total monthly expense: {} INR".format(expense))
    create_expense_sheet(update, context, daily_consumption, rate_per_liter, expense)

# Function to handle /breakdown command
def breakdown(update, context):
    if 'rate_per_liter' in context.user_data:
        daily_consumption = context.user_data.get('daily_consumption', [])
        rate_per_liter = context.user_data.get('rate_per_liter')
        expense = calculate_monthly_expense(daily_consumption, rate_per_liter)

        breakdown_message = "Breakdown of monthly expense:\n"
        for i in range(len(daily_consumption)):
            breakdown_message += "Date: {}\n".format(get_current_date())
            breakdown_message += "Consumption: {} liters\n".format(daily_consumption[i])
            breakdown_message += "Rate per Liter: {} INR\n".format(rate_per_liter)
            breakdown_message += "Expense: {} INR\n\n".format(rate_per_liter * daily_consumption[i])

        breakdown_message += "Total monthly expense: {} INR".format(expense)

        context.bot.send_message(chat_id=update.effective_chat.id, text=breakdown_message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Rate per liter is not set. Please set the rate using /setrate command.")

# Function to handle /setrate command
def set_rate(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the rate per liter for the calculation:")

# Function to handle /cleardata command
def clear_data(update, context):
    context.user_data.clear()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Data cleared.")

# Function to handle unknown commands
def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understand that command.")

# Function to handle errors
def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("totalbill", total_bill))
    dispatcher.add_handler(CommandHandler("breakdown", breakdown))
    dispatcher.add_handler(CommandHandler("setrate", set_rate))
    dispatcher.add_handler(CommandHandler("cleardata", clear_data))

    # Message handler
    dispatcher.add_handler(MessageHandler(Filters.text, handle_user_input))

    # Unknown command handler
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

    # Error handler
    dispatcher.add_error_handler(error)

    # Run the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
