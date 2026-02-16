# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from io import BufferedReader
from json import loads as json_loads
from logging import getLogger
from os import path as ospath
from os import walk as oswalk
from pathlib import Path

from aiofiles.os import path as aiopath
from aiofiles.os import rename as aiorename
from aiohttp import ClientSession
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from bot.core.config_manager import Config
from bot.helper.ext_utils.bot_utils import SetInterval, sync_to_async

LOGGER = getLogger(__name__)


class ProgressFileReader(BufferedReader):
    def __init__(self, filename, read_callback=None):
        super().__init__(open(filename, "rb"))
        self.__read_callback = read_callback
        self.length = Path(filename).stat().st_size

    def read(self, size=None):
        size = size or (self.length - self.tell())
        if self.__read_callback:
            self.__read_callback(self.tell())
        return super().read(size)

    def __len__(self):
        return self.length


class BuzzHeavierUpload:
    def __init__(self, listener, path):
        self.listener = listener
        self._updater = None
        self._path = path
        self._is_errored = False
        self.api_url = "https://buzzheavier.com/api/"
        self.upload_url = "https://w.buzzheavier.com/"
        self.__processed_bytes = 0
        self.last_uploaded = 0
        self.total_time = 0
        self.total_files = 0
        self.total_folders = 0
        self.is_uploading = True
        self.update_interval = 3

        from bot import user_data

        user_dict = user_data.get(self.listener.user_id, {})
        self.token = user_dict.get("BUZZHEAVIER_TOKEN") or Config.BUZZHEAVIER_API
        self.folder_id = user_dict.get("BUZZHEAVIER_FOLDER_ID") or ""
        
        LOGGER.info(f"Professor-X BuzzHeavier Engine Initialized.")

    @property
    def speed(self):
        try:
            return self.__processed_bytes / self.total_time
        except Exception:
            return 0

    @property
    def processed_bytes(self):
        return self.__processed_bytes

    def __progress_callback(self, current):
        chunk_size = current - self.last_uploaded
        self.last_uploaded = current
        self.__processed_bytes += chunk_size

    async def progress(self):
        self.total_time += self.update_interval

    @staticmethod
    async def is_buzzapi(token):
        if not token:
            return False
        async with (
            ClientSession() as session,
            session.get(
                "https://buzzheavier.com/api/account",
                headers={"Authorization": f"Bearer {token}"},
            ) as resp,
        ):
            return resp.status == 200

    async def __resp_handler(self, response):
        try:
            if isinstance(response, dict):
                if "id" in response:
                    return response["id"]
                if (
                    "data" in response
                    and isinstance(response["data"], dict)
                    and "id" in response["data"]
                ):
                    return response["data"]["id"]
            elif isinstance(response, str):
                try:
                    json_resp = json_loads(response)
                    if isinstance(json_resp, dict):
                        if "id" in json_resp:
                            return json_resp["id"]
                        if (
                            "data" in json_resp
                            and isinstance(json_resp["data"], dict)
                            and "id" in json_resp["data"]
                        ):
                            return json_resp["data"]["id"]
                except Exception:
                    pass
                return response.strip().strip('"')
        except Exception as e:
            LOGGER.error(f"Professor-X: Response handling error: {e}")
        return response

    async def __get_root_id(self):
        if self.token is None:
            raise Exception("Professor-X: BuzzHeavier API token missing!")

        async with ClientSession() as session:
            async with session.get(
                f"{self.api_url}account",
                headers={"Authorization": f"Bearer {self.token}"},
            ) as resp:
                if resp.status == 200:
                    try:
                        res = await resp.json()
                        if "rootDirectoryId" in res:
                            return res["rootDirectoryId"]
                        if (
                            "data" in res
                            and isinstance(res["data"], dict)
                            and "rootDirectoryId" in res["data"]
                        ):
                            return res["data"]["rootDirectoryId"]
                    except Exception:
                        pass
            async with session.get(
                f"{self.api_url}fs", headers={"Authorization": f"Bearer {self.token}"}
            ) as resp:
                if resp.status == 200:
                    try:
                        res = await resp.json()
                        if "id" in res:
                            return res["id"]
                        if (
                            "data" in res
                            and isinstance(res["data"], dict)
                            and "id" in res["data"]
                        ):
                            return res["data"]["id"]
                    except Exception:
                        pass
        return None

    @retry(
        wait=wait_exponential(multiplier=2, min=4, max=8),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception),
    )
    async def upload_aiohttp(self, url, file_path):
        headers = {"Authorization": f"Bearer {self.token}"}
        with ProgressFileReader(
            filename=file_path, read_callback=self.__progress_callback
        ) as file:
            async with ClientSession() as session:
                async with session.put(url, data=file, headers=headers) as resp:
                    if resp.status in [200, 201]:
                        return await self.__resp_handler(await resp.text())
                    else:
                        raise Exception(f"HTTP {resp.status}: {await resp.text()}")
        return None

    # ... [Keep create_folder, upload_file, _upload_dir, upload, _upload_process, cancel_task as analyzed] ...
