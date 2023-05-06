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
    
    polish_month_dict = {
        "sty": "01", #styczeń, january
        "lut": "02", #luty, february
        "mar": "03", #marzec, march
        "kwi": "04", #kwiecień, april
        "maj": "05", #maj, may
        "cze": "06", #czerwiec, june
        "lip": "07", #lipiec, july
        "sie": "08", #sierpień, august
        "wrz": "09", #wrzesień, september
        "paź": "10", #październik, october
        "lis": "11", #listopad, november
        "gru": "12"  #grudzień, december
    }

    def _parse_datetime(self, date: str):
        splitted_date = date.split(' ')
        if len(splitted_date) != 4:
            raise Exception(f"DATE DOESN'T HAVE 4 PARTS! ERROR! ({date})")

        # Date
        final_date_str = "20" + splitted_date[2]# YYYY
        final_date_str += "-"

        final_date_str += self.polish_month_dict[splitted_date[1]] # MM
        final_date_str += "-"

        day = splitted_date[0]
        if len(day) != 2: day = "0" + day # add "0" in front if not in "DD" format
        final_date_str += day

        # Time
        final_date_str += " "
        time = splitted_date[3]
        if len(time) != 5: time = "0" + time # add "0" in front if not in "HH:MM" format (H:MM instead)
        final_date_str += time

        self.date_added = final_date_str
        # print(final_date_str)

    def __init__(self, filename: str, filepath: str, filesize: str, date_added: str) -> None:
        self.filename = filename.replace(' ', '')
        self.filepath = filepath
        self.filesize = filesize.replace(',', '.') # saved in EU format (using , for decimals)
        self._parse_datetime(date_added)
        self.id = filepath.split(",")[-1].split(".")[0]
        tempIdVer = self.filename.replace("_iphoneos-arm64", "").replace("_iphoneos-arm", "")
        if "_v" in tempIdVer:
            self.bundle_id, self.version = tempIdVer.split("_v")
        elif "_ v" in tempIdVer:
            self.bundle_id, self.version = tempIdVer.split("_ v")
        else:
            print(f"\nCOULDN'T GET PROPRE BUNDLE ID/VERSION! FILENAME: \"{filename}\"")
            self.bundle_id = tempIdVer
            self.version = ""
        
        self.bundle_id = self.bundle_id.strip()
        self.version = self.version.strip()

    # Not really needed but mmmm Java
    def set_size(self, size: int) -> None:
        self.size = size