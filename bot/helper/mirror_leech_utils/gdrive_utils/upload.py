# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from logging import getLogger
from os import path as ospath, listdir, remove
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
    RetryError,
)

from ....core.config_manager import Config
from ...ext_utils.bot_utils import async_to_sync, SetInterval
from ...ext_utils.files_utils import get_mime_type
from ...mirror_leech_utils.gdrive_utils.helper import GoogleDriveHelper

LOGGER = getLogger(__name__)

class GoogleDriveUpload(GoogleDriveHelper):
    def __init__(self, listener, path):
        self.listener = listener
        self._updater = None
        self._path = path
        self._is_errored = False
        super().__init__()
        self.is_uploading = True

    def user_setting(self):
        if self.listener.up_dest.startswith("mtp:"):
            self.token_path = f"tokens/{self.listener.user_id}.pickle"
            self.listener.up_dest = self.listener.up_dest.replace("mtp:", "", 1)
            self.use_sa = False
        elif self.listener.up_dest.startswith("tp:"):
            self.listener.up_dest = self.listener.up_dest.replace("tp:", "", 1)
            self.use_sa = False
        elif self.listener.up_dest.startswith("sa:"):
            self.listener.up_dest = self.listener.up_dest.replace("sa:", "", 1)
            self.use_sa = True

    def upload(self):
        self.user_setting()
        self.service = self.authorize()
        LOGGER.info(f"Professor-X Uploading to GDrive: {self._path}")
        self._updater = SetInterval(self.update_interval, self.progress)
        try:
            if ospath.isfile(self._path):
                mime_type = get_mime_type(self._path)
                link = self._upload_file(
                    self._path,
                    self.listener.name,
                    mime_type,
                    self.listener.up_dest,
                    in_dir=False,
                )
                if self.listener.is_cancelled:
                    return
                if link is None:
                    raise ValueError("Upload manually cancelled")
                LOGGER.info(f"Uploaded To G-Drive: {self._path}")
            else:
                mime_type = "Folder"
                dir_id = self.create_directory(
                    ospath.basename(ospath.abspath(self.listener.name)),
                    self.listener.up_dest,
                )
                result = self._upload_dir(self._path, dir_id)
                if result is None:
                    raise ValueError("Upload manually cancelled!")
                link = self.G_DRIVE_DIR_BASE_DOWNLOAD_URL.format(dir_id)
                if self.listener.is_cancelled:
                    return
                LOGGER.info(f"Uploaded To G-Drive: {self.listener.name}")
        except Exception as err:
            if isinstance(err, RetryError):
                err = err.last_attempt.exception()
            err = str(err).replace(">", "").replace("<", "")
            LOGGER.error(err)
            async_to_sync(self.listener.on_upload_error, err)
            self._is_errored = True
        finally:
            self._updater.cancel()
            if self.listener.is_cancelled and not self._is_errored:
                if mime_type == "Folder" and dir_id:
                    LOGGER.info("Deleting cancelled data from Drive...")
                    self.service.files().delete(fileId=dir_id, supportsAllDrives=True).execute()
                return
            elif self._is_errored:
                return
            async_to_sync(
                self.listener.on_upload_complete,
                link,
                self.total_files,
                self.total_folders,
                mime_type,
                dir_id=self.get_id_from_url(link),
            )

    # ... [Keep _upload_dir and _upload_file logic the same as provided earlier] ...
