from files.File import File

#TODO: save Depiction & SileoDepiction & Icon & Header

class Package(File):
    known_keys = [
        "Package",
        "Name",        
        "Version",     
        "Section",     
        "Architecture",
        "Depends",
        "Installed-Size",
        "Author",
        "Maintainer",
        "Description",
        "Depiction",
        "Size",
        "MD5sum",
        "SHA256",
        "SHA512",
        "Filename",
        "SileoDepiction",
        "Icon",
        "Header",
        "Tag",
        "Conflicts", "Conflict",
        "Replaces",
        "Suggests",
        "Support",
        "Breaks",
        "Provides",
        "Pre-Depends",
        "dev",
        "XBS-Build-Version" # Purely for Legizmo on Chariz
    ]

    hashes: dict

    def __init__(self, file: str):
        self.data = {}
        self.hashes = {}
        for line in file.split("\n"):
            # avoid empty lines
            if line == '': continue

            # handle multi-lines keys
            # shouldn't be hashes in there so not handled
            if line[0] == ' ':
                self.data[known_key] += "\n" + line[1:]
                continue
            
            # else see if key present in known keys
            key, value = self._get_key_data(line)

            # Made that way to use capitalization from the known keys table
            known_key = self.is_in(key, self.known_keys)
            if known_key:
                self.last_key = key
                if self.is_in(key, self.known_hashes):
                    self.hashes[known_key] = value
                else:
                    self.data[known_key] = value
                continue

            print(f"UNKNOWN KEY FOR LINE: {line}")
        