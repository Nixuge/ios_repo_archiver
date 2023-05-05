from dataclasses import dataclass
import os


@dataclass
class Result:
    status_code: int
    hash_check: bool
    already_exists: bool
    hash: str | None
    finished: bool
    valid_url: bool

    def __init__(self, status_code: int = 200, hash_check: bool = True,
                 already_exists: bool = False, hash: str | None = None,
                 finished: bool = False, valid_url: bool = True,
                 temp_filename: str | None = None):
        self.status_code = status_code
        self.hash_check = hash_check
        self.already_exists = already_exists
        self.hash = hash
        self.finished = finished
        self.valid_url = valid_url
        if temp_filename:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                # os.system(f"rm {temp_filename}")
