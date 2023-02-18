# Note:
# being generous with varchars (version for ex)
# just in case
# it doesn't really matter anyways tbh as debs themselves take much more space

# depiction, sileodepiction, icon, header
# -> saved as hashes (md5s), only saved in file form directly
# (party to avoid the db itself to grow too much w uninteresting things)

class QUERIES:
    @staticmethod
    def get_create_repo_table_query(name: str) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {name} (
                    package VARCHAR(255),
                    name VARCHAR(255),
                    version VARCHAR(255),

                    section VARCHAR(255),
                    architecture VARCHAR(255),
                    tag VARCHAR(2048),

                    depends VARCHAR(2048),
                    provides VARCHAR(2048),
                    predepends VARCHAR(2048),
                    replaces VARCHAR(2048),
                    suggests VARCHAR(2048),
                    breaks VARCHAR(2048),
                    conflicts VARCHAR(2048),

                    support VARCHAR(1024),

                    installed-size INT,
                    size INT,

                    author VARCHAR(1024),
                    maintainer VARCHAR(1024),

                    md5sum VARCHAR(32),
                    sha256 VARCHAR(64),
                    sha512 VARCHAR(128),

                    description TEXT,

                    depiction VARCHAR(32),
                    sileodepiction VARCHAR(32),

                    icon VARCHAR(32),
                    header VARCHAR(32),

                    additionaldata TEXT,
                    
                    PRIMARY KEY (package)
                    );"""
    
    @staticmethod
    def get_insert_query(name: str) -> str:
        return f"""INSERT INTO {name} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""