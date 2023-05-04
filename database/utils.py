from sqlite3 import Cursor
from typing import Any
from database.queries import Queries
from database.queue import DbQueueInstance
from objects.files.package import Package


class Utils:
    args_order =  ("package", "name", "version", 
                   "section", "architecture", "priority", "tag",
                   "depends", "provides", "predepends", "replaces", "suggests", "breaks", "conflicts",
                   "size", "installedsize",
                   "author", "maintainer", "support", "dev",
                   "homepage", "description",
                   "depiction", "moderndepiction", "icon", "header", # saved as hashes (md5)
                   "additionaldata", "md5sum", "sha256", # saved as hashes (md5)
                   "paid")

    @staticmethod
    def get_args_in_order_from_dict(args_dict: dict):
        # Convert a dict to a list of items in order
        args_order: list[Any] = []
        for key in Utils.args_order:
            args_order.append(args_dict.get(key, None))
        return args_order


    @staticmethod
    def build_args(package: Package, downloadable_elements: dict[str, Any], paid: bool) -> list[Any]:
        # All normal elements from pkg data directly
        final_args_dict: dict[str, Any] = dict(package.data)

        # Add ("depiction", "moderndepiction", "icon", "header")
        for key, value in downloadable_elements.items():
            final_args_dict[key] = value

        # Add additional data
        ad = package.additional_data
        if ad == None or len(ad) == 0:
            final_args_dict["additionaldata"] = None
        else:
            final_args_dict["additionaldata"] = str(ad)
        
        # Add hashes
        for hash, value in package.hashes.items():
            final_args_dict[hash] = value

        # Add paid
        final_args_dict["paid"] = 1 if paid else 0
        
        return Utils.get_args_in_order_from_dict(final_args_dict)


    @staticmethod
    def contains_md5(table: str, md5: str):
        query = Queries.get_where_contains_md5(table, md5)
        
        return DbQueueInstance.cursor.execute(query).fetchone()