# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

import re
from contextlib import suppress
from PIL import Image
from hashlib import md5
from aiofiles.os import remove, path as aiopath, makedirs
import json
from asyncio import (
    create_subprocess_exec,
    gather,
    wait_for,
    sleep,
)
from asyncio.subprocess import PIPE
from os import path as ospath
from re import search as re_search, escape
from time import time
from aioshutil import rmtree
from langcodes import Language

from ... import LOGGER, DOWNLOAD_DIR, threads, cores
from ...core.config_manager import BinConfig
from .bot_utils import cmd_exec, sync_to_async
from .files_utils import get_mime_type, is_archive, is_archive_split
from .status_utils import time_to_seconds

# ... [Keep get_md5_hash, create_thumb, get_media_info, get_document_type, get_streams, take_ss, get_audio_thumbnail, get_video_thumbnail, get_multiple_frames_thumbnail exactly as they are] ...

class FFMpeg:
    def __init__(self, listener):
        self._listener = listener
        self._processed_bytes = 0
        self._last_processed_bytes = 0
        self._processed_time = 0
        self._last_processed_time = 0
        self._speed_raw = 0
        self._progress_raw = 0
        self._total_time = 0
        self._eta_raw = 0
        self._time_rate = 0.1
        self._start_time = 0

    @property
    def processed_bytes(self):
        return self._processed_bytes

    @property
    def speed_raw(self):
        return self._speed_raw

    @property
    def progress_raw(self):
        return self._progress_raw

    @property
    def eta_raw(self):
        return self._eta_raw

    def clear(self):
        self._start_time = time()
        self._processed_bytes = 0
        self._processed_time = 0
        self._speed_raw = 0
        self._progress_raw = 0
        self._eta_raw = 0
        self._time_rate = 0.1
        self._last_processed_time = 0
        self._last_processed_bytes = 0

    async def _ffmpeg_progress(self):
        while not (
            self._listener.subproc.returncode is not None
            or self._listener.is_cancelled
            or self._listener.subproc.stdout.at_eof()
        ):
            try:
                line = await wait_for(self._listener.subproc.stdout.readline(), 60)
            except Exception:
                break
            line = line.decode().strip()
            if not line:
                break
            if "=" in line:
                key, value = line.split("=", 1)
                if value != "N/A":
                    if key == "total_size":
                        self._processed_bytes = int(value) + self._last_processed_bytes
                        self._speed_raw = self._processed_bytes / (
                            time() - self._start_time
                        )
                    elif key == "speed":
                        self._time_rate = max(0.1, float(value.strip("x")))
                    elif key == "out_time":
                        self._processed_time = (
                            time_to_seconds(value) + self._last_processed_time
                        )
                        try:
                            self._progress_raw = (
                                self._processed_time * 100
                            ) / self._total_time
                            if (
                                hasattr(self._listener, "subsize")
                                and self._listener.subsize
                                and self._progress_raw > 0
                            ):
                                self._processed_bytes = int(
                                    self._listener.subsize * (self._progress_raw / 100)
                                )
                            if (time() - self._start_time) > 0:
                                self._speed_raw = self._processed_bytes / (
                                    time() - self._start_time
                                )
                            else:
                                self._speed_raw = 0
                            self._eta_raw = (
                                self._total_time - self._processed_time
                            ) / self._time_rate
                        except ZeroDivisionError:
                            self._progress_raw = 0
                            self._eta_raw = 0
            await sleep(0.05)

    # ==========================================
    # PROFESSOR-X FEATURE: ADD WATERMARK TO VIDEO
    # ==========================================
    async def add_watermark(self, video_file, watermark_text="Professor-X"):
        self.clear()
        self._total_time = (await get_media_info(video_file))[0]
        dir_path, base_name = ospath.split(video_file)
        output_file = f"{dir_path}/WM_{base_name}"
        
        # Hardcodes text onto the video stream at the bottom right corner
        cmd = [
            "taskset", "-c", f"{cores}", BinConfig.FFMPEG_NAME,
            "-hide_banner", "-loglevel", "error", "-progress", "pipe:1",
            "-i", video_file,
            "-vf", f"drawtext=text='{watermark_text}':fontcolor=white@0.7:fontsize=32:x=w-tw-20:y=h-th-20",
            "-c:a", "copy",
            "-threads", f"{threads}", output_file
        ]

        if self._listener.is_cancelled:
            return False
            
        self._listener.subproc = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
        await self._ffmpeg_progress()
        _, stderr = await self._listener.subproc.communicate()
        code = self._listener.subproc.returncode
        
        if self._listener.is_cancelled:
            return False
            
        if code == 0:
            LOGGER.info(f"Watermark applied successfully to {base_name}")
            return output_file
        else:
            if await aiopath.exists(output_file):
                await remove(output_file)
            LOGGER.error(f"Watermark Error: {stderr.decode().strip() if stderr else 'Unknown'}")
            return False

    # ... [Keep ffmpeg_cmds, convert_video, convert_audio, sample_video, split methods exactly as they are] ...
