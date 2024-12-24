# Scrapelando

A Telegram bot that scrapes Pelando (Brazilian deals website) and notifies users about deals matching their search criteria and minimum score requirements.

## Features

- Search for deals on Pelando using custom search terms
- Filter deals by minimum score
- Receive deal notifications through Telegram
- Headless browser automation for efficient scraping

## Prerequisites

- Python 3.x
- Chrome browser installed
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Scrapelando
```

2. Install required packages:
```
pip install -r requirements.txt
````

3. Create a .env file in the project root and add your Telegram Bot token:
````
BOT_API_TOKEN=your_telegram_bot_token_here
````
