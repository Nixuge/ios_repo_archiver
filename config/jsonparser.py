from abc import abstractmethod
import jstyleson
from config.config import Config

from objects.repometa import RepoMeta

class BaseLoader:
    content: list | dict
    
    def from_file(self, file_path: str):
        with open(file_path, 'r') as openFile:
            self.content = jstyleson.load(openFile)
        return self #make it chainable

    def from_data(self, data: dict | list):
        self.content = data
        return self #make it chainable


class ConfigLoader(BaseLoader):
    def parse(self) -> Config: # type: ignore
        #TODO: LOAD CONFIG HERE
        pass


class RepoListLoader(BaseLoader):
    conf: Config
    def __init__(self, default_conf: Config) -> None:
        self.conf = default_conf

    def _load_list(self) -> list[RepoMeta]:
        repos = []
        for elem in self.content:
            repos.append(RepoMeta(elem, self.conf))
        return repos

    def _load_dict(self) -> list[RepoMeta]:
        repos = []
        for repo_url, repo_conf in self.content.items(): # type: ignore (always dict if here)
            repos.append(RepoMeta(
                repo_url,
                ConfigLoader().from_data(repo_conf).parse()
            ))
        return repos
         


    def parse_all(self, ) -> list[RepoMeta]:
        if isinstance(self.content, list):
            return self._load_list()
    
        return self._load_dict()

    


# class ConfigLoader:
#     def __init__(self) -> None:
#         pass

#     @staticmethod
#     def load_config_dict():
#         pass

    