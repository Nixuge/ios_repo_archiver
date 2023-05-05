# Not named "strings.py" as it'd be confusing

import os
import random
import string

from utils.vars.file import Folder

def random_string(prefix: str = Folder.temp, letter_count: int = 15) -> str:
    path = prefix + ''.join(random.choice(string.ascii_lowercase) for _ in range(letter_count))
    while os.path.exists(path):
        print("Path already exists (random_string)")
        path = prefix + ''.join(random.choice(string.ascii_lowercase) for _ in range(letter_count))
    return path