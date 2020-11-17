#! /usr/bin/python3

import argparse, sys, os

from ..core import *


class JCDBPath:

    """
    'jcdb path' returns the location of a JCDB object.
    """

    @staticmethod
    def error(e):
        JCDBPath.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'jcdb path'.
        """

        JCDBPath.parser = argparse.ArgumentParser(
            prog="jcdb path",
            description="Calculate the location of a JCDB object.",
        )
        JCDBPath.parser.add_argument(
            "db",
            nargs="?",
            help="a jcdb database",
        )
        JCDBPath.parser.add_argument(
            "cls",
            nargs="?",
            help="a jcdb class",
        )
        JCDBPath.parser.add_argument(
            "inst",
            nargs="?",
            help="an instance (and the position within it)",
        )

        return JCDBPath.parser

    @staticmethod
    def main(args=None):

        """
        The main program of 'jcdb path'.
        """

        if args == None:  # parse args using own parser
            JCDBPath.generateParser()
            args = JCDBPath.parser.parse_args(sys.argv[1:])

        print(JCDB.makePath(args.db, args.cls, args.inst), "\n")


if __name__ == "__main__":
    JCDBPath.main()
