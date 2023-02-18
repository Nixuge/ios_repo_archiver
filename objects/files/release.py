from objects.files.file import File

class Release(File):
    known_keys = [
        "origin",
        "label",
        "suite",
        "version",
        "codename",
        "architectures",
        "components",
        "description",
        "date",
        "md5sum",
        "sha512",
        "sha256"
    ]

    files: dict

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
        self.additional_data = {}
        self.files = {}

        for line in file.split("\n"):
            # avoid empty lines
            if line == '': 
                continue

            # Handle multi line values (& hashes)
            if line[0] == ' ':
                if self.is_in(self.last_key, self.known_hashes):
                    self._add_hash(line)
                elif self.known(self.last_key):
                    self.data[self.last_key] += line[1:]
                else:
                    self.additional_data[self.last_key] += line[1:]
                continue
            
            key, value = self._get_key_data(line)

            key = self._get_fixed_val(key)

            # Save key to dict (if key is a known key)
            if self.known(key):
                self.last_key = key
                if not self.is_in(key, self.known_hashes):
                    self.data[key] = value
                continue

            self.additional_data[key] = value
            print(f"UNKNOWN KEY FOR LINE: {line}")
