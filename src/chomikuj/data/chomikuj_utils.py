from sqlite3 import Row
from chomikuj.data.chomikuj_data import DbVarsChomikuj
from chomikuj.data.chomikuj_file import ChomikujFile
from database.queries import QueriesChomikuj


class ChomikujUtils:
    # unneeded
    @staticmethod
    def contains_md5(md5: str) -> Row:
        query = QueriesChomikuj.get_where_contains_md5("chomikuj_packages", md5)
        
        return DbVarsChomikuj.ReadInstance.cursor.execute(query).fetchone()

    # used as md5s aren't in chomikuj, only once the file is downloaded. Hence why we're relying on the bundle id & version for this.
    @staticmethod
    def contains_package(file: ChomikujFile):
        query = QueriesChomikuj.get_where_contains_key("chomikuj_packages", "bundle_id", file.bundle_id)

        packages = DbVarsChomikuj.ReadInstance.cursor.execute(query).fetchall()
        print(len(packages))