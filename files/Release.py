from files.File import File

class Release(File):
    known_keys = [
        "Origin",
        "Label",
        "Suite",
        "Version",
        "Codename",
        "Architectures",
        "Components",
        "Description",
        "Date",
        "MD5Sum",
        "SHA512",
        "SHA256"
    ]

    files = {}

    def _add_hash(self, line: str) -> None:
        keys = line.split(' '); keys.pop(0)
        # [hash, size, name]
        hash = keys[0]
        size = keys[1]
        filename = keys[2]
        if not filename in self.files:
            self.files[filename] = {}
            self.files[filename]["hashes"] = {}
            self.files[filename]["size"] = size
        self.files[filename]["hashes"][self.last_key] = hash
    
    def __init__(self, file: str):
        self.data = {}
        for line in file.split("\n"):
            # avoid empty lines
            if line == '': 
                continue

            # Handle multi line values (& hashes)
            if line[0] == ' ':
                if self.is_in(self.last_key, self.known_hashes):
                    self._add_hash(line)
                else:
                    self.data[known_key] += line[1:]
                continue
            
            key, value = self._get_key_data(line)

            # Save key to dict (if key is a known key)
            known_key = self.is_in(key, self.known_keys)
            if known_key:
                self.last_key = known_key
                if not self.is_in(key, self.known_hashes):
                    self.data[known_key] = value
                continue

            
            print(f"UNKNOWN KEY FOR LINE: {line}")
