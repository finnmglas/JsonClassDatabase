#! /usr/bin/python3

import argparse, sys

from ..core import *

from .tool_path import JCDBPath
from .tool_exists import JCDBExists
from .tool_list import JCDBList


class JCDBCLI:

    """
    The 'jcdb' commandline tool based on the JCDB python module.
    It allows you to store data in the JSON Class Database.
    """

    tools = {
        "path": JCDBPath,
        "exists": JCDBExists,
        "list": JCDBList,
    }

    @staticmethod
    def error(e):
        JCDBCLI.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'jcdb'.
        """

        JCDBCLI.parser = argparse.ArgumentParser(
            description="Interact with the JSON Class Database.",
            epilog="More details at https://github.com/finnmglas/jcdb.",
        )
        JCDBCLI.parser.add_argument(
            "-v",
            "--version",
            dest="show_version",
            action="store_true",
            help="show the current version and exit",
        )

        subparsers = JCDBCLI.parser.add_subparsers(dest="tool", help="JCDB tools")

        for name in JCDBCLI.tools:
            tool = JCDBCLI.tools[name]
            # Import Parser --- jcdb [name]
            toolParser = subparsers.add_parser(name)
            toolParser.__dict__ = tool.generateParser().__dict__

        return JCDBCLI.parser

    @staticmethod
    def main():

        # generate parser
        JCDBCLI.generateParser()
        # parse args
        args = JCDBCLI.parser.parse_args(sys.argv[1:])

        # show version
        if args.show_version:
            import pkg_resources

            print("v" + pkg_resources.require("jcdb")[0].version)
            return

        if args.tool == None:
            print("No tool supplied. Run 'jcdb -h' for a list of tools.\n")
            exit()

        # forward args to a tool
        JCDBCLI.tools[args.tool].main(args)


if __name__ == "__main__":
    JCDBCLI.main()
