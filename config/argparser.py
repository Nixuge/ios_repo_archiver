from argparse import ArgumentParser, Namespace
from config.config import Config
from config.jsonparser import ConfigLoader

from objects.repometa import RepoMeta


class ArgsParser:
    parser: ArgumentParser
    args: Namespace

    def __init__(self) -> None:
        parser = ArgumentParser(prog='IOS Repo Downloader')
        # Priority in order
        parser.add_argument('-dc', '--default-config')
        parser.add_argument('-rl', '--repo-list') # is list using default config, if dict using specified config
        parser.add_argument('-r', '--repo')
        # 4 below may be overwritten by "default_config"
        parser.add_argument('-p', '--print', action='store_true', help="none, all, additional_fails, deb_fails, paid_packages, progress") #TODO: implement custom choice instead of bool like rn
        parser.add_argument('-s', '--save-additional-data', action='store_true')
        parser.add_argument('-i', '--ignore-errors', action='store_true')
        parser.add_argument('-rc', '--recheck-paid-packages', action='store_true')
        self.parser = parser
        self.args = parser.parse_args()
    
    def _gen_config(self) -> Config:
        args = self.args
        conf = Config()
        if args.print:
            # see line 18
            conf.print_additional_fails = args.print
            conf.print_deb_fails = args.print
            conf.print_paid_packages = args.print
            conf.print_progress = args.print
        
        if args.save_additional_data:
            conf.save_additional_data = args.save_additional_data
        
        if args.ignore_errors:
            conf.ignore_errors = args.ignore_errors
        
        if args.recheck_paid_packages:
            conf.recheck_paid_packages = args.recheck_paid_packages
        
        return conf

    def get_repos(self) -> list[RepoMeta] | None:
        args = self.args
        config: Config = self._gen_config()

        if args.default_config:
            config = ConfigLoader().from_file(args.default_config).parse()
        
        if args.repo_list:
            #TODO: Load config multiple times for every file
            # if list apply default config, else apply whathever specified in dict
            return #return the loaded thingys here
            
        if args.repo:
            return [RepoMeta(args.repo, config)]

        return None
