from sqlite3 import Row
from chomikuj.data.chomikuj_data import DbVarsChomikuj
from chomikuj.data.chomikuj_file import ChomikujFile
from database.queries import QueriesChomikuj


class ChomikujUtils:
    @staticmethod
    def contains_md5(md5: str) -> Row:
        query = QueriesChomikuj.get_where_contains_md5("chomikuj_packages", md5)
        
        return DbVarsChomikuj.ReadInstance.cursor.execute(query).fetchone()

    # used as md5s aren't in chomikuj, only once the file is downloaded. Hence why we're relying on the bundle id & version for this.
    @staticmethod
    def contains_package(file: ChomikujFile):
        query = QueriesChomikuj.get_where_contains_key("chomikuj_packages", "filename", file.filename)

        # row = DbVarsChomikuj.ReadInstance.cursor.execute(query).fetchone()
        # if not row:
        #     return False
        
        # # Fix bc i forgot to add the date into my sql queries before lmao
        # if row[4] == None:
        #     query2 = f"""UPDATE "chomikuj_packages" SET date = "{file.date_added}" WHERE filename="{file.filename}";"""
        #     DbVarsChomikuj.Queue.add_instuction(query2, None)

        # return row
        return DbVarsChomikuj.ReadInstance.cursor.execute(query).fetchone()