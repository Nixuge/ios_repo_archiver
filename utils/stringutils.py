# Not named "strings.py" as it'd be confusing

import random
import string

from utils.vars import DLF

def random_string(prefix: str = DLF.temp, letter_count: int = 15) -> str:
    return prefix + ''.join(random.choice(string.ascii_lowercase) for _ in range(letter_count))