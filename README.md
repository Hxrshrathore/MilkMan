# Telegram Milk Consumption Tracker Bot

This Telegram bot allows you to track your daily milk consumption and calculate the monthly expense based on the rate per liter. The bot interacts with the user through commands and messages, providing a convenient way to record and manage milk consumption data.

## Setup

To set up the Telegram Milk Consumption Tracker Bot, follow the steps below:

1. Install the required dependencies by running the following command:

```
pip install python-telegram-bot pandas
```

2. Obtain a Telegram Bot token by creating a new bot on the Telegram platform. You can create a bot and obtain the token by following the official documentation: [Telegram Bot API](https://core.telegram.org/bots/api)

3. Replace the `BOT_TOKEN` variable in the code with your own Telegram Bot token.

4. Run the script using the following command:

```
python milk_consumption_bot.py
```

5. Start the bot by sending the `/start` command to your Telegram Bot.

## Bot Commands

The Telegram Milk Consumption Tracker Bot supports the following commands:

- `/start`: Start the bot and display the menu.
- `/totalbill`: Calculate and share the total monthly expense.
- `/breakdown`: Show the breakdown of monthly expenses.
- `/setrate`: Set the rate per liter for the calculation.
- `/cleardata`: Clear all recorded data.

## Usage

1. Start the bot by sending the `/start` command to your Telegram Bot.

2. Set the rate per liter by sending the `/setrate` command. The bot will prompt you to enter the rate per liter.

3. To record your daily milk consumption, the bot will ask you to enter the consumption in liters for the current day. Respond to the bot's prompts with the corresponding values.

4. You can view the total monthly expense by sending the `/totalbill` command.

5. To view the breakdown of monthly expenses, use the `/breakdown` command.

6. If you want to clear all recorded data, send the `/cleardata` command.

Note: The bot will create an Excel file with the expense breakdown and share it with you when you use the `/totalbill` or `/breakdown` commands. The file will be available for download for one hour.

## Contributing

Contributions to this project are welcome! If you have any improvements, bug fixes, or new features to add, feel free to fork the repository, make your changes, and open a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code within the terms of this license.
