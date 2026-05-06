#  MIT License
#
#  Copyright (c) 2019-present Dan <https://github.com/delivrance>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE

import os
import sys
import asyncio
import logging
from logging.handlers import RotatingFileHandler

from config import Config
from pyrogram import Client, idle
from pyromod import listen

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# ---------- DEBUG: Print masked token to verify it's loaded ----------
token = Config.BOT_TOKEN
if token:
    masked = token[:6] + "..." + token[-4:] if len(token) > 10 else "***"
    LOGGER.info(f"Loaded BOT_TOKEN: {masked}")
else:
    LOGGER.error("BOT_TOKEN is empty! Set it in Render environment variables.")
    sys.exit(1)

# ---------- Auth Users ----------
if isinstance(Config.AUTH_USERS, list):
    AUTH_USERS = Config.AUTH_USERS
else:
    # If it's a comma-separated string (old style)
    AUTH_USERS = [int(uid.strip()) for uid in Config.AUTH_USERS.split(",") if uid.strip()]

LOGGER.info(f"Authorized users: {AUTH_USERS}")

# Prefixes
prefixes = ["/", "~", "?", "!"]

plugins = dict(root="plugins")

if __name__ == "__main__":
    bot = Client(
        "StarkBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=20,
        plugins=plugins,
        workers=50
    )
    
    async def main():
        try:
            await bot.start()
            bot_info = await bot.get_me()
            LOGGER.info(f"<--- @{bot_info.username} Started (c) STARKBOT --->")
            await idle()
        except Exception as e:
            LOGGER.error(f"Failed to start bot: {e}")
            raise

    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped by user")
    except Exception as e:
        LOGGER.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        LOGGER.info("<--- Bot Stopped --->")
