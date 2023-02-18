# Note:
# being generous with varchars (version for ex)
# just in case
# it doesn't really matter anyways tbh as debs themselves take much more space

# depiction, moderndepiction, icon, header
# -> saved as hashes (md5s), only saved in file form directly
# (party to avoid the db itself to grow too much w uninteresting things)

class Queries:
    @staticmethod
    def get_create_repo_table_query(name: str) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {name} (
                    package VARCHAR(255) NOT NULL,
                    name VARCHAR(255),
                    version VARCHAR(255),

                    section VARCHAR(255),
                    architecture VARCHAR(255),
                    priority VARCHAR(255),
                    tag VARCHAR(2048),

                    depends VARCHAR(2048),
                    provides VARCHAR(2048),
                    predepends VARCHAR(2048),
                    replaces VARCHAR(2048),
                    suggests VARCHAR(2048),
                    breaks VARCHAR(2048),
                    conflicts VARCHAR(2048),

                    size INT,
                    installedsize INT,

                    author VARCHAR(1024),
                    maintainer VARCHAR(1024),
                    support VARCHAR(1024),
                    dev VARCHAR(1024),

                    homepage VARCHAR(1024),
                    description TEXT,

                    depiction VARCHAR(32),
                    moderndepiction VARCHAR(32),

                    icon VARCHAR(32),
                    header VARCHAR(32),

                    additionaldata TEXT,
                    
                    md5sum VARCHAR(32) NOT NULL,
                    sha256 VARCHAR(64),

                    PRIMARY KEY (md5sum)
                    );"""
    
    @staticmethod
    def get_insert_query(table: str) -> str:
        return f"""INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    
    @staticmethod
    def get_where_contains_key(table: str, column: str, value: str):
        return f"""SELECT * FROM {table} WHERE {column}=\"{value}\""""
    
    @staticmethod
    def get_where_contains_md5(table: str, hash: str):
        return Queries.get_where_contains_key(table, "md5sum", hash)