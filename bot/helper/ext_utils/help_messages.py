# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

# ruff: noqa: F403, F405
mirror = """<b>Send link along with command line or </b>

/cmd link

<b>By replying to link/file</b>:

/cmd -n new name -e -up upload destination

<b>NOTE:</b>
1. Commands that start with <b>qb</b> are ONLY for torrents."""

# ... [Keep other strings the same until you reach the specific replacements below] ...

yt_opt = """<b>Options</b>: -opt

/cmd link -opt {"format": "bv*+mergeall[vcodec=none]", "nocheckcertificate": True, "playliststart": 10, "fragment_retries": float("inf"), "matchtitle": "S13", "writesubtitles": True, "live_from_start": True, "postprocessor_args": {"ffmpeg": ["-threads", "4"]}, "wait_for_video": (5, 100), "download_ranges": [{"start_time": 0, "end_time": 10}]}

Check all yt-dlp api options from this <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L184'>FILE</a>."""

# ... [Skip to ffmpeg cmds] ...

ffmpeg_cmds = """<b>FFmpeg Commands</b>: -ff
list of lists of ffmpeg commands. You can set multiple ffmpeg commands for all files before upload. Don't write ffmpeg at beginning, start directly with the arguments.
Notes:
1. Add <code>-del</code> to the list(s) which you want from the bot to delete the original files after command run complete!
3. To execute one of pre-added lists in bot like: ({"subtitle": ["-i professorx.mkv -c copy -c:s srt professorx.mkv"]}), you must use -ff subtitle (list key)
Examples: ["-i professorx.mkv -c copy -c:s srt professorx.mkv", "-i professorx.video -c copy -c:s srt professorx"]
Here I will explain how to use professorx.* which is reference to files you want to work on.
1. First cmd: the input is professorx.mkv so this cmd will work only on mkv videos and the output is professorx.mkv also so all outputs is mkv. -del will delete the original media after complete run of the cmd.
2. Second cmd: the input is professorx.video so this cmd will work on all videos and the output is only professorx so the extenstion is same as input files."""

# ... [Skip to get_bot_commands()] ...

def get_bot_commands():
    from ...core.plugin_manager import get_plugin_manager

    static_commands = {
        "Mirror": "[link/file] Mirror to Upload Destination",
        "QbMirror": "[magnet/torrent] Mirror to Upload Destination using qbit",
        "Ytdl": "[link] Mirror YouTube, m3u8, Social Media and yt-dlp supported urls",
        "UpHoster": "[link/file] Upload to DDL Servers",
        "Leech": "[link/file] Leech files to Upload to Telegram",
        "QbLeech": "[magnet/torrent] Leech files to Upload to Telegram using qbit",
        "YtdlLeech": "[link] Leech YouTube, m3u8, Social Media and yt-dlp supported urls",
        "Clone": "[link] Clone files/folders to GDrive",
        "UserSet": "User personal settings",
        "ForceStart": "[gid/reply] Force start from queued task",
        "Count": "[link] Count no. of files/folders in GDrive",
        "List": "[query] Search any Text which is available in GDrive",
        "Search": "[query] Search torrents via Qbit Plugins",
        "MediaInfo": "[reply/link] Get MediaInfo of the Target Media",
        "Select": "[gid/reply] Select files for NZB, Aria2, Qbit Tasks",
        "Ping": "Ping Bot to test Response Speed",
        "Status": "[id/me] Tasks Status of Bot",
        "Stats": "Bot, OS, Repo & System full Statistics",
        "Rss": "User RSS Management Settings",
        "IMDB": "[query] or ttxxxxxx Get IMDB info",
        "CancelAll": "Cancel all Tasks on the Bot",
        "Help": "Detailed help usage of the Professor-X Bot",
        "BotSet": "[SUDO] Bot Management Settings",
        "Log": "[SUDO] Get Bot Logs for Internal Working",
        "Restart": "[SUDO] Reboot bot",
        "RestartSessions": "[SUDO] Reboot User Sessions",
    }
# ... [Keep the rest of the file identical] ...
