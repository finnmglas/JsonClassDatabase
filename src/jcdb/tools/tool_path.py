#! /usr/bin/python3

import argparse, sys, os

from ..core.object import *


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
    def makePath(db, cls, inst):
        path = DEFAULT_OBJECT_STORAGE

        if db:
            path = os.path.join(path, db)

        if cls:
            path = os.path.join(path, *cls.split("."))

        if inst:
            path = os.path.join(path, inst + ".json")

        return path

    @staticmethod
    def main(args=None):

        """
        The main program of 'jcdb path'.
        """

        if args == None:  # parse args using own parser
            JCDBPath.generateParser()
            args = JCDBPath.parser.parse_args(sys.argv[1:])

        print(JCDBPath.makePath(args.db, args.cls, args.inst))


if __name__ == "__main__":
    LedgerMan.main()
