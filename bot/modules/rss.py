# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from httpx import AsyncClient
from apscheduler.triggers.interval import IntervalTrigger
from asyncio import Lock, sleep
from datetime import datetime, timedelta
from feedparser import parse as feed_parse
from functools import partial
from io import BytesIO
from pyrogram.filters import create
from pyrogram.handlers import MessageHandler
from time import time
from re import compile, I

from .. import scheduler, rss_dict, LOGGER
from ..core.config_manager import Config
from ..helper.ext_utils.bot_utils import new_task, arg_parser, get_size_bytes
from ..helper.ext_utils.status_utils import get_readable_file_size
from ..helper.ext_utils.db_handler import database
from ..helper.ext_utils.exceptions import RssShutdownException
from ..helper.ext_utils.help_messages import RSS_HELP_MESSAGE
from ..helper.telegram_helper.button_build import ButtonMaker
from ..helper.telegram_helper.filters import CustomFilters
from ..helper.telegram_helper.message_utils import (
    send_message,
    edit_message,
    send_rss,
    send_file,
    delete_message,
)

rss_dict_lock = Lock()
handler_dict = {}
size_regex = compile(r"(\d+(\.\d+)?\s?(GB|MB|KB|GiB|MiB|KiB))", I)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

async def rss_menu(event):
    user_id = event.from_user.id
    buttons = ButtonMaker()
    buttons.data_button("Subscribe", f"rss sub {user_id}")
    buttons.data_button("Subscriptions", f"rss list {user_id} 0")
    buttons.data_button("Get Items", f"rss get {user_id}")
    buttons.data_button("Edit", f"rss edit {user_id}")
    buttons.data_button("Pause", f"rss pause {user_id}")
    buttons.data_button("Resume", f"rss resume {user_id}")
    buttons.data_button("Unsubscribe", f"rss unsubscribe {user_id}")
    if await CustomFilters.sudo("", event):
        buttons.data_button("All Subscriptions", f"rss listall {user_id} 0")
        buttons.data_button("Pause All", f"rss allpause {user_id}")
        buttons.data_button("Resume All", f"rss allresume {user_id}")
        buttons.data_button("Unsubscribe All", f"rss allunsub {user_id}")
        buttons.data_button("Delete User", f"rss deluser {user_id}")
        if scheduler.running:
            buttons.data_button("Shutdown Rss", f"rss shutdown {user_id}")
        else:
            buttons.data_button("Start Rss", f"rss start {user_id}")
    buttons.data_button("Close", f"rss close {user_id}")
    button = buttons.build_menu(2)
    msg = f"Professor-X RSS Menu | Users: {len(rss_dict)} | Running: {scheduler.running}"
    return msg, button

# ... [Keep the rest of the massive RSS file the same as you provided originally] ...
