#! /usr/bin/python3

import argparse, sys, os

from ..core.object import *
from .tool_path import *


class JCDBExists:

    """
    'jcdb exists' checks if a JCDB object exists.
    """

    @staticmethod
    def error(e):
        JCDBExists.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'jcdb exists'.
        """

        JCDBExists.parser = argparse.ArgumentParser(
            prog="jcdb exists",
            description="Check if a JCDB object exists",
        )
        JCDBExists.parser.add_argument(
            "db",
            nargs="?",
            help="a jcdb database",
        )
        JCDBExists.parser.add_argument(
            "cls",
            nargs="?",
            help="a jcdb class",
        )
        JCDBExists.parser.add_argument(
            "inst",
            nargs="?",
            help="an instance (and the position within it)",
        )

        return JCDBExists.parser

    @staticmethod
    def exists(db, cls, inst):
        return os.path.exists(JCDBPath.makePath(db, cls, inst))

    @staticmethod
    def main(args=None):

        """
        The main program of 'jcdb exists'.
        """

        if args == None:  # parse args using own parser
            JCDBExists.generateParser()
            args = JCDBExists.parser.parse_args(sys.argv[1:])

        print(JCDBExists.exists(args.db, args.cls, args.inst))


if __name__ == "__main__":
    LedgerMan.main()
