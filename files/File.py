# I'll admit it, the 2 classes inheriting this one
# are far from the fanciest lol

class File:
    last_key: str
    data: dict

    known_hashes = [
        "MD5Sum",
        "SHA512",
        "SHA256"
    ]

    def __init__(file: str):
        pass

    @staticmethod
    def _get_key_data(line: str) -> tuple[str, str]:
        data = line.split(':')
        key = data[0]
        value = ''.join(data[1:])
        # cant split by ": " bc of hashes, need this
        if value != '' and value[0] == ' ':
            value = value[1:]
        
        return key, value

    @staticmethod
    def is_in(key: str, values: list[str]) -> str | None:
        key = key.lower()
        for value in values:
            if value.lower() == key:
                return value