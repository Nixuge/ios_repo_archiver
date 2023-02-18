# I'll admit it, the 2 classes inheriting this one
# are far from the fanciest
# They're made to be as easy to access as possible from the outside
# for this use case

class File:
    known_keys: list
    last_key: str
    data: dict
    additional_data: dict
    fix_keys = {}

    known_hashes = [
        "md5sum",
        "sha512",
        "sha256"
    ]

    def __init__(self, file: str):
        pass
    
    def _get_fixed_val(self, val: str) -> str:
        if val.lower() in self.fix_keys:
            return self.fix_keys[val]
        return val.lower()

    @staticmethod
    def _get_key_data(line: str) -> tuple[str, str]:
        data = line.split(':')
        key = data[0]
        value = ''.join(data[1:])
        # cant split by ": " bc of hashes, need this
        if value != '' and value[0] == ' ':
            value = value[1:]
        
        return key, value

    # remainings from an old system
    @staticmethod
    def is_in(key: str, values: list[str]) -> bool:
        key = key.lower()
        return key.lower() in values
        
    def known(self, key: str) -> bool:
        return self.is_in(key, self.known_keys)