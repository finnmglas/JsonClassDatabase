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
    def main(args=None):

        """
        The main program of 'jcdb exists'.
        """

        if args == None:  # parse args using own parser
            JCDBExists.generateParser()
            args = JCDBExists.parser.parse_args(sys.argv[1:])

        print(JCDB.exists(args.db, args.cls, args.inst), "\n")


if __name__ == "__main__":
    JCDBExists.main()
