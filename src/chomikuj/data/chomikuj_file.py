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
        self.bundle_id, self.version = tempIdVer.split("_v")

    # Not really needed but mmmm Java
    def set_size(self, size: int) -> None:
        self.size = size