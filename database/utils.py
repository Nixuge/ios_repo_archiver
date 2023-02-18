from sqlite3 import Cursor
from database.queries import Queries
from objects.files.Package import Package


class Utils:
    @staticmethod
    def get_args_order() -> tuple:
        return ("package", "name", "version", 
                "section", "architecture", "tag",
                "depends", "provides", "predepends", "replaces", "suggests", "breaks", "conflicts",
                "size", "installedsize",
                "author", "maintainer", "support",
                "description",
                "depiction", "sileodepiction", # saved as hashes (md5)
                "icon", "header") # saved as hashes (md5)

        #TODO: 
        #remove depiction, sileodepiction,
        #icon, header
        #& download them & save MD5

        # ("additionaldata", "md5sum", "sha256", "sha512")
        # not here as processed differently

    @staticmethod
    def build_args(package: Package) -> list[str]:
        final_args: list[str] = []
        # All normal elements
        for arg in Utils.get_args_order():
            final_args.append(package.data.get(arg, None))
        
        # Add additional data
        if package.additional_data == None or len(package.additional_data) == 0:
            final_args.append(None) # type: ignore 
        else:
            final_args.append(str(package.additional_data))
        
        # Add hashes
        for elem in ("md5sum", "sha256"):
            final_args.append(package.hashes.get(elem, None))
        
        return final_args


    @staticmethod
    def contains_md5(table: str, md5: str, cursor: Cursor):
        query = Queries.get_where_contains_md5(table, md5)

        result = cursor.execute(query)
        return result.fetchone()