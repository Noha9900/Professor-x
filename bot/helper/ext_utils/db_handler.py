# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from importlib import import_module
from aiofiles import open as aiopen
from aiofiles.os import path as aiopath
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

from ... import LOGGER, qbit_options, rss_dict, user_data
from ...core.config_manager import Config
from ...core.tg_client import TgClient

class DbManager:
    def __init__(self):
        self._return = True
        self._conn = None
        self.db = None

    async def connect(self):
        try:
            if self._conn is not None:
                await self._conn.close()
            self._conn = AsyncIOMotorClient(
                Config.DATABASE_URL, server_api=ServerApi("1")
            )
            # PROFESSOR-X: Using dedicated database namespace
            self.db = self._conn.professorx 
            self._return = False
            LOGGER.info("Professor-X Database Connected Successfully!")
        except PyMongoError as e:
            LOGGER.error(f"Database Connection Error: {e}")
            self.db = None
            self._return = True
            self._conn = None

    # ... [Keep update_deploy_config, update_config, update_aria2, update_user_data etc. with rebranded log info] ...
    
    async def update_deploy_config(self):
        if self._return:
            return
        settings = import_module("config")
        config_file = {
            key: value.strip() if isinstance(value, str) else value
            for key, value in vars(settings).items()
            if not key.startswith("__")
        }
        await self.db.settings.deployConfig.replace_one(
            {"_id": TgClient.ID}, config_file, upsert=True
        )
        LOGGER.info("Professor-X: Deploy Config Synced to Cloud.")

database = DbManager()
