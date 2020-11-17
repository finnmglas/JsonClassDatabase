#! /usr/bin/python3

import argparse, sys, os, json
from cliprint import color

from ..core import *


class JCDBGet:

    """
    'jcdb get' displays JCDB objects.
    """

    @staticmethod
    def error(e):
        JCDBGet.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'jcdb get'.
        """

        JCDBGet.parser = argparse.ArgumentParser(
            prog="jcdb get",
            description="Display a jcdb object.",
        )
        JCDBGet.parser.add_argument(
            "db",
            help="a jcdb database",
        )
        JCDBGet.parser.add_argument(
            "cls",
            help="a jcdb class",
        )
        JCDBGet.parser.add_argument(
            "inst",
            help="an instance (and the position within it)",
        )

        return JCDBGet.parser

    @staticmethod
    def main(args=None):

        """
        The main program of 'jcdb get'.
        """

        if args == None:  # parse args using own parser
            JCDBGet.generateParser()
            args = JCDBGet.parser.parse_args(sys.argv[1:])

        if not JCDB.exists(args.db, args.cls, args.inst):
            print(color.f.bold + "Object does not exist.\n" + color.end)
            exit()

        try:
            o = JCDB.get_object(args.db, args.cls, args.inst)
        except ValueError:
            print(color.f.bold + "Cannot decode JSON.\n" + color.end)
            exit()

        print()
        if isinstance(o, Object):
            print(o.encode(indent=2) + "\n")
        else:
            print(str(o) + "\n")


if __name__ == "__main__":
    JCDBGet.main()
