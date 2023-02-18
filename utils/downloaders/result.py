from dataclasses import dataclass
import os


@dataclass
class Result:
    status_code: int
    hash_check: bool
    already_exists: bool
    hash: str | None
    finished: bool

    def __init__(self, status_code: int = 200, hash_check: bool = True,
                 already_exists: bool = False, hash: str | None = None,
                 finished: bool = False, temp_filename: str | None = None):
        self.status_code = status_code
        self.hash_check = hash_check
        self.already_exists = already_exists
        self.hash = hash
        self.finished = finished
        if temp_filename:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                # os.system(f"rm {temp_filename}")
