#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

class Config(object):
    # Mandatory environment variables
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")

    # Validate required variables
    if not BOT_TOKEN:
        sys.exit("ERROR: BOT_TOKEN environment variable not set.")
    if not API_ID:
        sys.exit("ERROR: API_ID environment variable not set.")
    if not API_HASH:
        sys.exit("ERROR: API_HASH environment variable not set.")

    # Convert API_ID to int (required by pyrogram)
    try:
        API_ID = int(API_ID)
    except ValueError:
        sys.exit("ERROR: API_ID must be an integer.")

    # AUTH_USERS: comma-separated list of user IDs (optional)
    AUTH_USERS_STR = os.environ.get("AUTH_USERS", "")
    if AUTH_USERS_STR:
        AUTH_USERS = [int(uid.strip()) for uid in AUTH_USERS_STR.split(",") if uid.strip()]
    else:
        AUTH_USERS = []

    # You can add other optional configs here
    # For example: WORKERS, SLEEP_THRESHOLD, etc.
