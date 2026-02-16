# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from xml.etree import ElementTree as ET
from aiohttp import ClientSession

from .. import LOGGER
from ..core.config_manager import Config
from ..helper.ext_utils.bot_utils import new_task
from ..helper.ext_utils.status_utils import get_readable_file_size
from ..helper.ext_utils.telegraph_helper import telegraph
from ..helper.telegram_helper.button_build import ButtonMaker
from ..helper.telegram_helper.message_utils import edit_message, send_message

# ... [Keep hydra_search and search_nzbhydra identical] ...

async def create_telegraph_page(query, items):
    content = "<b>Professor-X NZB Search Results:</b><br><br>"
    sorted_items = sorted(
        [
            (
                int(item.find("size").text) if item.find("size") is not None else 0,
                item,
            )
            for item in items[:100]
        ],
        reverse=True,
        key=lambda x: x[0],
    )

    for idx, (size_bytes, item) in enumerate(sorted_items, 1):
        title = (
            item.find("title").text
            if item.find("title") is not None
            else "No Title Available"
        )
        download_url = (
            item.find("link").text
            if item.find("link") is not None
            else "No Link Available"
        )
        size = get_readable_file_size(size_bytes)

        content += (
            f"{idx}. {title}<br>"
            f"<b><a href='{download_url}'>Download URL</a> | <a href='http://t.me/share/url?url={download_url}'>Share Download URL</a></b><br>"
            f"<b>Size:</b> {size}<br>"
            f"━━━━━━━━━━━━━━━━━━━━━━<br><br>"
        )

    response = await telegraph.create_page(
        title=f"Search Results for '{query}'",
        content=content,
    )
    LOGGER.info(f"Telegraph page created for search: {query}")
    return f"https://telegra.ph/{response['path']}"
