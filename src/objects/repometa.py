from config.config import Config

NUMS = "0123456789"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
VALID_CHARS = NUMS + ALPHABET + '_'

class RepoMeta:
    url: str
    sql_name: str
    config: Config
    
    def __init__(self, url: str, config: Config | None = None) -> None:
        self.url = url
        self.sql_name = self._get_sql_name_from_url(url)
        if config == None:
            config = Config()
        self.config = config

    @staticmethod
    def _get_sql_name_from_url(url: str) -> str:
        sql_name = url.replace("https://", "").replace("http://", "")

        # remove last char if is a /
        if sql_name[-1] == '/':
            sql_name = sql_name[:-1]

        # .=_, /=__
        sql_name = sql_name.replace('.', '_').replace('/', '__')

        # if starting w number add _
        if sql_name[0] in NUMS:
            sql_name = '_' + sql_name
        
        # final checks just in case
        for char in sql_name:
            if char not in VALID_CHARS:
                raise RuntimeError(f"Invalid characters in final sql table name: \"{sql_name}\"")
        
        return sql_name
