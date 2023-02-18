from objects.files.File import File

#TODO: save Depiction & SileoDepiction & Icon & Header

class Package(File):
    known_keys = [
        "package",
        "name",        
        "version",     
        "section",     
        "architecture",
        "depends",
        "installed-size",
        "author",
        "maintainer",
        "description",
        "depiction",
        "size",
        "md5sum",
        "sha256",
        "sha512",
        "filename",
        "sileodepiction",
        "icon",
        "header",
        "tag",
        "conflicts",
        "replaces",
        "suggests",
        "support",
        "breaks",
        "provides",
        "pre-depends",
    ]

    fix_keys = {
        "conflict": "conflicts"
    }

    hashes: dict

    def __init__(self, file: str):
        self.data = {}
        self.additional_data = {}
        self.hashes = {}
        for line in file.split("\n"):
            # avoid empty lines
            if line == '': continue

            # handle multi-lines keys
            # shouldn't be hashes in there so not handled
            if line[0] == ' ':
                if self.known(self.last_key):
                    self.data[self.last_key] += "\n" + line[1:]
                else:
                    self.additional_data[self.last_key] += "\n" + line[1:]
                continue
            
            # else see if key present in known keys
            key, value = self._get_key_data(line)

            key = self._get_fixed_val(key)

            # Made that way to use capitalization from the known keys table
            if self.known(key):
                self.last_key = key
                if self.is_in(key, self.known_hashes):
                    self.hashes[key] = value
                else:
                    self.data[key] = value
                continue
            
            self.additional_data[key] = value
            print(f"UNKNOWN KEY FOR LINE: {line}")
        