from sqlite3 import Cursor
from database.queries import Queries
from objects.files.package import Package


class Utils:
    @staticmethod
    def get_dict_args_order() -> tuple:
        return ("package", "name", "version", 
                "section", "architecture", "priority", "tag",
                "depends", "provides", "predepends", "replaces", "suggests", "breaks", "conflicts",
                "size", "installedsize",
                "author", "maintainer", "support", "dev",
                "homepage", "description") 

        # + ("depiction", "moderndepiction", "icon", "header")
        # saved as hashes (md5) after

        # + ("additionaldata", "md5sum", "sha256", "sha512")
        # not here as processed differently

    @staticmethod
    def build_args(package: Package, downloadable_elements: list[str | None]) -> list[str | None]:
        final_args: list[str | None] = []
        # All normal elements
        for arg in Utils.get_dict_args_order():
            final_args.append(package.data.get(arg, None))
        
        # Add ("depiction", "moderndepiction", "icon", "header")
        for element in downloadable_elements:
            final_args.append(element)
        
        # Add additional data
        if package.additional_data == None or len(package.additional_data) == 0:
            final_args.append(None)
        else:
            final_args.append(str(package.additional_data))
        
        # Add hashes
        for elem in ("md5sum", "sha256"):
            final_args.append(package.hashes.get(elem, None))
        
        return final_args


    @staticmethod
    def contains_md5(table: str, md5: str, cursor: Cursor):
        query = Queries.get_where_contains_md5(table, md5)

        return cursor.execute(query).fetchone()