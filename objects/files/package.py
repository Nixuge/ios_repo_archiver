from objects.files.file import File


class Package(File):
    known_keys = File.known_hashes + [
        "package",
        "name",        
        "version",     
        "section",     
        "architecture",
        "depends",
        "installedsize",
        "author",
        "maintainer",
        "description",
        "depiction",
        "size",
        "filename",
        "moderndepiction",
        "icon",
        "header",
        "tag",
        "conflicts",
        "replaces",
        "suggests",
        "support",
        "breaks",
        "provides",
        "predepends",
        "homepage",
        "dev",
        "priority"
    ]

    # Keys known but not worth having a whole column for
    # Eg. here, Sponsor
    # this is only to avoid printing when encountering smth from
    # additional data that's already known
    known_but_additional = (
        "sponsor",
    )

    fix_keys = {
        "recommended": "suggests",
        "recommends": "suggests",
        "sileodepiction": "moderndepiction",
        "tags": "tag",
        "conflict": "conflicts",
        "pre-depends": "predepends",
        "installed-size": "installedsize"
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
            if key in self.known_keys:
                self.last_key = key
                if key in self.known_hashes:
                    self.hashes[key] = value
                else:
                    self.data[key] = value
                continue
            
            self.additional_data[key] = value
            if not key in self.known_but_additional:
                print(f"UNKNOWN KEY FOR LINE: {line}")
        