# FGG Bot - Discord Giveaways Monitor Bot

A Discord bot for automatic notifications about free games on Epic Games and Steam.

## Features

- Automatic notifications about free games
- Supports Epic Games and Steam
- Configure channels via /setup

## Tech Stack

- Python 3.14+
- Mongo DB 8+
- IGDB API
- Steam Web API
- Epic Games Store API
- Docker (optional)

## Project Structure

```bash
project/
│
├── bot/
│   ├── bot_logging.py
│   ├── config.py
│   ├── main.py
│
├── cogs/
│   ├── check_offers.py
│   ├── commands.py
│   └── guild_events.py
│
├── database/
│   ├── crud.py
│
├── services/
│   ├── deals.py
│   ├── igdb_api.py
│   └── ping.py
│
└── utils/
    └── format.py
```

## How It Works

1. The administrator adds the bot to the server
2. The bot sends notifications about free games to the system channel
3. Administrators can configure a channel for notifications and a role for mentions

## Commands

```bash
/setup add - Setup notifications channel (1 per server)
/setup remove - Remove notifications from the server
/setup get - Get current notifications channel
/check - Check current promotions
/ping - Check utils statuses
/help - Show this menu
```

## Installation

### Using Docker Compose (Recommended)

Make sure you have Docker and Docker Compose installed.

- Copy the repoistory

```bash
git clone https://github.com/SoLvkky/fgg-bot
cd fgg-bot
```

- Insert the required environment variables

```bash
#.env
BOT_TOKEN = DISCORD_BOT_TOKEN
TEST_GUILD_ID = YOUR_TEST_GUILD_ID
GUILD_LOGS = LOGS_CHANNEL_ID
TV_ID = TWITCH_CLIENT_ID
TV_SECRET = TWITCH_CLIENT_SECRET
MONGO_LINK = YOUR_MONGO_LINK
```

- Build and start the stack:

```bash
docker compose up -d --build
```

### Using Python

- Copy and initialize the repository

```bash
git clone https://github.com/SoLvkky/fgg-bot
cd fgg-bot
python -m venv .venv
pip install -r requirements.txt
```

- Insert the required environment variables

```bash
#.env
BOT_TOKEN = DISCORD_BOT_TOKEN
TEST_GUILD_ID = YOUR_TEST_GUILD_ID
GUILD_LOGS = LOGS_CHANNEL_ID
TV_ID = TWITCH_CLIENT_ID
TV_SECRET = TWITCH_CLIENT_SECRET
MONGO_LINK = YOUR_MONGO_LINK
```

- Start the bot

```bash
python -m bot.main
```
