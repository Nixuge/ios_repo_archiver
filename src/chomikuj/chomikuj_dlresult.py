from dataclasses import dataclass
from chomikuj_file import ChomikujFile

@dataclass
class ChomikujDlResult:
    success: bool
    file: ChomikujFile | None = None