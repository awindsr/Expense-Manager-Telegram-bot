# Expense Manager Telegram Bot

Expense Manager Telegram Bot is a Python-based Telegram bot that allows users to manage their expenses. Users can add, delete, view, and generate summaries of their expenses.

## Features

- **Add Expense:** Users can add expenses to specific categories for a particular month.

- **Delete Expense:** Users can delete expenses from specific categories for a particular month.

- **View Expenses:** Users can view a list of expenses for a particular month.

- **Generate Summary:** Users can generate a summary of expenses for a particular month or within a date range.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- Telegram Bot Token (Get one by talking to [BotFather](https://core.telegram.org/bots#botfather)).
- Authorized users specified in `credential.py`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/expense-manager-telegram-bot.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `credential.py` file with the following content:

   ```python
   AUTH_USERS = ["your_username"]
   ```

   Replace `"your_username"` with your Telegram username.

4. Set up your Telegram bot by talking to [BotFather](https://core.telegram.org/bots#botfather) and obtaining a Bot Token.

5. Set the Bot Token as an environment variable:

   ```bash
   export BOT_TOKEN=your_bot_token
   ```

6. Run the bot:

   ```bash
   python main.py
   ```

## Usage

1. Start the bot by sending `/start` to your bot's username on Telegram.

2. Use the following commands to interact with the bot:

   - `/help`: Get a list of available commands and their usage.
   - `/add [Category] [Month] [Expense]`: Add an expense to a category for a particular month.
   - `/delete [Category] [Month] [Expense]`: Delete an expense from a category for a particular month.
   - `/view [Month]`: View expenses for a particular month.
   - `/summary [Month]`: Generate a summary for a particular month.
   - `/summary [from date (ddmmyy)] [to date (ddmmyy)]`: Generate a summary for a date range.

## Contributors

- Your Name <your.email@example.com>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
