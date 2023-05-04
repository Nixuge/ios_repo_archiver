import hashlib
import os
from utils.downloaders.result import Result
from utils.downloaders.simple._simple_base import _SimpleDownloaderBase
from utils.vars.file import get_create_path


class SimpleDownloaderAsync(_SimpleDownloaderBase):
