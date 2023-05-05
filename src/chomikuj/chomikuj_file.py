from dataclasses import dataclass


@dataclass
class ChomikujFile:
    filename: str
    filepath: str
    # id: int #TODO (maybe?)
    filesize: str # from the website, not the actual file
    date_added: str