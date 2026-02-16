# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from uvloop import install
install()

from subprocess import run as srun
from os import getcwd
from asyncio import Lock, new_event_loop, set_event_loop
from logging import (
    ERROR, INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger,
)
from os import cpu_count
from time import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Import from the new package name
from .core.config_manager import BinConfig
from sabnzbdapi import SabnzbdClient

# Setup Global Logging with the Professor-X Tag
basicConfig(
    format="[%(asctime)s] [PROF-X] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[FileHandler("log.txt"), StreamHandler()],
    level=INFO,
)

LOGGER = getLogger("Professor-X")
bot_start_time = time()
bot_loop = new_event_loop()
set_event_loop(bot_loop)

# Performance Tuning
cpu_no = cpu_count()
threads = max(1, cpu_no // 2)

# Professor-X Global Cache & States
intervals = {"status": {}, "qb": "", "jd": "", "nzb": "", "stopAll": False}
user_data = {}
task_dict = {}
status_dict = {}
task_dict_lock = Lock()
queue_dict_lock = Lock()

sabnzbd_client = SabnzbdClient(
    host="http://localhost",
    api_key="admin",
    port="8070",
)

# Initialize Professor-X qBit Daemon
srun([BinConfig.QBIT_NAME, "-d", f"--profile={getcwd()}"], check=False)
scheduler = AsyncIOScheduler(event_loop=bot_loop)
