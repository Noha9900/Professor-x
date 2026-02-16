# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from aiofiles.os import remove, path as aiopath
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler

from .. import LOGGER, TgClient
from ..helper.ext_utils.bot_utils import new_task
from ..helper.ext_utils.ttv_utils import TTVConverter
from ..helper.telegram_helper.bot_commands import BotCommands
from ..helper.telegram_helper.filters import CustomFilters
from ..helper.telegram_helper.message_utils import send_message, delete_message, send_file

@new_task
async def text_to_video(_, message):
    args = message.text.split(maxsplit=1)
    reply = message.reply_to_message
    
    if len(args) > 1:
        text = args[1]
    elif reply and (reply.text or reply.caption):
        text = reply.text or reply.caption
    else:
        return await send_message(message, "<b>Usage:</b> <code>/ttv [text]</code> or reply to text.")

    status_msg = await send_message(message, "<i>Professor-X Rendering Text-to-Video...</i>")
    out_path = f"ttv_{message.id}.mp4"
    
    try:
        converter = TTVConverter(text, out_path)
        await converter.convert()
        
        if await aiopath.exists(out_path):
            await send_file(message, out_path, caption="<b>Professor-X TTV Engine Result</b>")
            await delete_message(status_msg)
        else:
            await edit_message(status_msg, "❌ Failed to generate video.")
    except Exception as e:
        LOGGER.error(f"TTV Error: {e}")
        await edit_message(status_msg, f"<b>Error:</b> {e}")
    finally:
        if await aiopath.exists(out_path):
            await remove(out_path)

# Registering the handler
TgClient.bot.add_handler(
    MessageHandler(
        text_to_video,
        filters=command("ttv", case_sensitive=True) & CustomFilters.authorized
    )
)
