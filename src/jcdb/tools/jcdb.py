#! /usr/bin/python3

import argparse, sys

from ..core.object import *


class JCDB:

    """
    The 'jcdb' commandline tool based on the JCDB python module.
    It allows you to store data in the JSON Class Database.
    """

    tools = {}

    @staticmethod
    def error(e):
        JCDB.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'jcdb'.
        """

        JCDB.parser = argparse.ArgumentParser(
            description="Interact with the JSON Class Database.",
            epilog="More details at https://github.com/finnmglas/jcdb.",
        )
        JCDB.parser.add_argument(
            "-v",
            "--version",
            dest="show_version",
            action="store_true",
            help="show the current version and exit",
        )

        subparsers = JCDB.parser.add_subparsers(dest="tool", help="JCDB tools")

        for name in JCDB.tools:
            tool = JCDB.tools[name]
            # Import Parser --- jcdb [name]
            toolParser = subparsers.add_parser(name)
            toolParser.__dict__ = tool.generateParser().__dict__

        return JCDB.parser

    @staticmethod
    def main():

        # generate parser
        JCDB.generateParser()
        # parse args
        args = JCDB.parser.parse_args(sys.argv[1:])

        # show version
        if args.show_version:
            import pkg_resources

            print("v" + pkg_resources.require("jcdb")[0].version)
            return

        if args.tool == None:
            print("No arguments supplied.")
            exit()

        # forward args to a tool
        JCDB.tools[args.tool].main(args)


if __name__ == "__main__":
    JCDB.main()
