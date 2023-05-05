from dataclasses import dataclass

class ChomikujFile:
    filename: str
    filepath: str
    filesize: str # from the website, not the actual file
    date_added: str
    id: str
    bundle_id: str
    version: str
    size: int | None

    def __init__(self, filename: str, filepath: str, filesize: str, date_added: str) -> None:
        self.filename = filename
        self.filepath = filepath
        self.filesize = filesize
        self.date_added = date_added
        self.id = filepath.split(",")[-1].split(".")[0]
        tempIdVer = filename.replace("_iphoneos-arm64", "").replace("_iphoneos-arm", "")
        if "_v" in tempIdVer:
            self.bundle_id, self.version = tempIdVer.split("_v")
        elif "_ v" in tempIdVer:
            self.bundle_id, self.version = tempIdVer.split("_ v")
        else:
            print(f"\n\nCOULDN'T GET PROPRE BUNDLE ID/VERSION! FILENAME: \"{filename}\"\n")
            self.bundle_id = tempIdVer
            self.version = ""
        
        self.bundle_id = self.bundle_id.strip()
        self.version = self.version.strip()

    # Not really needed but mmmm Java
    def set_size(self, size: int) -> None:
        self.size = size