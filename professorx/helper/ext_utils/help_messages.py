# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from ..telegram_helper.bot_commands import BotCommands

# Main Help String
help_string = f"""⌬ <b>Professor-X Engine Help Menu</b>
│
┟ <code>/{BotCommands.MirrorCommand[0]}</code>: Mirror links/files to Cloud.
┠ <code>/{BotCommands.LeechCommand[0]}</code>: Leech links/files to Telegram.
┠ <code>/{BotCommands.YtdlCommand[0]}</code>: Mirror YouTube/Audio-Video links.
┠ <code>/{BotCommands.CloneCommand}</code>: Copy GDrive/Rclone items.
┠ <code>/{BotCommands.TTVCommand}</code>: Convert Text to Video (TTV).
┖ <code>/{BotCommands.StatusCommand[0]}</code>: Check current task status.

<b>Arguments & Advanced Usage:</b>
Use buttons below to see specific arguments for each command.
"""

# Mirror & Leech Arguments
MIRROR_HELP_DICT = {
    "main": f"""➲ <b>Mirror/Leech Arguments:</b>
<code>/{BotCommands.MirrorCommand[0]} [link] -n [name] -up [remote]</code>
│
┟ <b>-n</b>: Rename the file/folder.
┠ <b>-up</b>: Custom Rclone/GDrive path.
┠ <b>-z</b>: Compress into a Zip file.
┠ <b>-s</b>: Select specific files from Torrent/NZB.
┠ <b>-p</b>: Protect Zip with a password.
┖ <b>-m</b>: Define a subfolder in destination.""",
}

# YT-DLP Arguments
YT_HELP_DICT = {
    "main": f"""➲ <b>YT-DLP Arguments:</b>
<code>/{BotCommands.YtdlCommand[0]} [link] -opt [options]</code>
│
┟ <b>-opt</b>: Pass raw YT-DLP options.
┠ <b>-s</b>: Manual quality selection menu.
┠ <b>-ca</b>: Convert Audio to (mp3/m4a/opus/etc).
┖ <b>-cv</b>: Convert Video to (mp4/mkv/etc).""",
}

# Clone Arguments
CLONE_HELP_DICT = {
    "main": f"""➲ <b>Clone Arguments:</b>
<code>/{BotCommands.CloneCommand} [link] -up [remote]</code>
│
┟ <b>-sync</b>: Sync source to destination.
┖ <b>-rcf</b>: Custom Rclone flags.""",
}

# TTV Engine Help (Professor-X Exclusive)
TTV_HELP_DICT = {
    "main": f"""➲ <b>TTV Engine (Text-to-Video):</b>
<code>/{BotCommands.TTVCommand} [text]</code>
│
┟ <b>Reply:</b> Reply to any text message with <code>/{BotCommands.TTVCommand}</code>.
┠ <b>Render:</b> The bot generates an MP4 video with the text.
┖ <b>Customization:</b> Coming soon in Professor-X v2.0!""",
}

# Mapping for the button logic
COMMAND_USAGE = {
    "mirror": ["Mirror/Leech Usage", MIRROR_HELP_DICT["main"]],
    "yt": ["YT-DLP Usage", YT_HELP_DICT["main"]],
    "clone": ["Clone Usage", CLONE_HELP_DICT["main"]],
    "ttv": ["TTV Usage", TTV_HELP_DICT["main"]],
}
