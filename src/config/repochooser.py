#TODO: thing w inputs to choose the repo & config
from objects.repometa import RepoMeta

# to call only if no args specified

class RepoChooser:
    @staticmethod
    def choice(text: str, default_y: bool = True) -> bool:
        if default_y:
            yn = "Y/n"
        else:
            yn = "y/N"

        choice = input(f"{text} [{yn}]").lower()
        return (choice == "y" or choice == "yes")

    @staticmethod
    def full_ask() -> RepoMeta:
        #TODO do this so that:
        # ask repo
        # ask if cares about options or nahs, if yes do them
        return RepoMeta("temp placeholder")