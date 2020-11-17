#! /usr/bin/python3

import argparse, sys, os, json
from cliprint import color

from ..core import *


class JCDBCreate:

    """
    'jcdb create' creates JCDB dbs, classes and objects.
    """

    @staticmethod
    def error(e):
        JCDBCreate.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'jcdb create'.
        """

        JCDBCreate.parser = argparse.ArgumentParser(
            prog="jcdb create",
            description="Create jcdb databases, classes and object.",
        )
        JCDBCreate.parser.add_argument(
            "db",
            help="a jcdb database",
        )
        JCDBCreate.parser.add_argument(
            "cls",
            nargs="?",
            help="a jcdb class",
        )
        JCDBCreate.parser.add_argument(
            "inst",
            nargs="?",
            help="an instance (and the position within it)",
        )

        return JCDBCreate.parser

    @staticmethod
    def main(args=None):

        """
        The main program of 'jcdb create'.
        """

        if args == None:  # parse args using own parser
            JCDBCreate.generateParser()
            args = JCDBCreate.parser.parse_args(sys.argv[1:])

        flag = JCDB.create(args.db, args.cls, args.inst)

        if flag == 0:
            print("Created database.\n")
        elif flag == 1:
            print("Created class.\n")
        elif flag == 2:
            print("Created object.\n")
        elif flag == 3:
            print("Already exists.\n")


if __name__ == "__main__":
    JCDBCreate.main()
