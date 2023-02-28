# Not named "strings.py" as it'd be confusing

import random
import string

from utils.vars.file import Folder

def random_string(prefix: str = Folder.temp, letter_count: int = 15) -> str:
    return prefix + ''.join(random.choice(string.ascii_lowercase) for _ in range(letter_count))