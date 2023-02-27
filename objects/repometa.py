from dataclasses import dataclass


@dataclass
class RepoMeta:
    full_name: str #TODO: get that using the Release file directly (if possible)
    url: str
    sql_name: str #TODO: generate this automatically from URL (.=_, /=__, if starting w number add _)

