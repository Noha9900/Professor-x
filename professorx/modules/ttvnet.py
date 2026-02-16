# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from aiofiles.os import remove, path as aiopath
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from time import time

from .. import LOGGER, TgClient, task_dict, task_dict_lock
from ..helper.ext_utils.bot_utils import new_task, sync_to_async
from ..helper.ext_utils.ttv_utils import TTVConverter
from ..helper.listeners.task_listener import TaskListener
from ..helper.mirror_leech_utils.status_utils.ffmpeg_status import FFmpegStatus
from ..helper.telegram_helper.bot_commands import BotCommands
from ..helper.telegram_helper.filters import CustomFilters
from ..helper.telegram_helper.message_utils import send_message, delete_message

class TTVTask(TaskListener):
    def __init__(self, client, message, is_leech=True):
        super().__init__()
        self.client = client
        self.message = message
        self.is_leech = is_leech
        self.name = f"TTV_{int(time())}.mp4"
        self.subproc = None

    async def start(self, text):
        out_path = f"downloads/{self.mid}/{self.name}"
        import os
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # 1. Create Status Entry
        # We use FFmpegStatus to track the rendering progress
        from ..helper.ext_utils.media_utils import FFMpeg
        ffmpeg_obj = FFMpeg(self)
        async with task_dict_lock:
            task_dict[self.mid] = FFmpegStatus(self, ffmpeg_obj, self.mid, "TTV Render")

        try:
            # 2. Render Process
            converter = TTVConverter(text, out_path)
            await converter.convert()
            
            # 3. Handle the Upload
            # This triggers the Mirror/Leech listener to send to TG or Cloud
            if await aiopath.exists(out_path):
                self.size = (await aiopath.stat(out_path)).st_size
                # If mirroring to cloud was requested, it would go here. 
                # For now, we default to Leech (Telegram Upload).
                await self.on_download_complete()
            else:
                await self.on_download_error("Render failed: Output file not found.")
        except Exception as e:
            LOGGER.error(f"Professor-X TTV Engine Error: {e}")
            await self.on_download_error(str(e))

@new_task
async def text_to_video_handler(_, message):
    args = message.text.split(maxsplit=1)
    reply = message.reply_to_message
    
    if len(args) > 1:
        text = args[1]
    elif reply and (reply.text or reply.caption):
        text = reply.text or reply.caption
    else:
        return await send_message(message, "<b>Usage:</b> <code>/ttv [text]</code> or reply to text.")

    # Initialize Professor-X TTV Task
    task = TTVTask(TgClient.bot, message)
    await task.start(text)

# Registering the new handler
TgClient.bot.add_handler(
    MessageHandler(
        text_to_video_handler,
        filters=command(BotCommands.TTVCommand, case_sensitive=True) & CustomFilters.authorized
    )
)
