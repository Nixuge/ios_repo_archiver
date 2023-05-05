IS_POSIX: bool
try:
    import posix
    IS_POSIX = True
except ImportError:
    IS_POSIX = False


def print_same_line(text: str):
    if IS_POSIX:
        print("\x1b[2K\r", end="\r") #clear line (POSIX only)
    print(f"\r{text}", end="\r")