# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

import os
import asyncio
from shlex import split
from ...core.config_manager import BinConfig
from ..ext_utils.bot_utils import cmd_exec

class TTVConverter:
    def __init__(self, text, output_path, width=1280, height=720, duration=10):
        self.text = text.replace("'", "\\'").replace(":", "\\:")
        self.output = output_path
        self.w = width
        self.h = height
        self.duration = duration

    async def convert(self, bg_color="black", font_color="white", font_size=24):
        """
        Uses FFmpeg filters to generate a video from raw text.
        """
        # Drawing text with word wrap and centering
        drawtext_filter = (
            f"drawtext=text='{self.text}':fontcolor={font_color}:fontsize={font_size}:"
            f"x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor={bg_color}@0.5:boxborderw=5"
        )
        
        cmd = [
            BinConfig.FFMPEG_NAME, "-y", "-f", "lavfi", 
            "-i", f"color=c={bg_color}:s={self.w}x{self.h}:d={self.duration}",
            "-vf", drawtext_filter,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", str(self.duration),
            self.output
        ]
        
        stdout, stderr, code = await cmd_exec(cmd)
        if code != 0:
            raise Exception(f"FFmpeg TTV Error: {stderr}")
        return self.output
