#! /usr/bin/python3

import argparse, sys

from cliprint import print_table, color

from ..core import *


class JCDBList:

    """
    'jcdb list' returns the location of a JCDB object.
    """

    @staticmethod
    def error(e):
        JCDBList.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'jcdb list'.
        """

        JCDBList.parser = argparse.ArgumentParser(
            prog="jcdb list",
            description="Calculate the location of a JCDB object.",
        )
        JCDBList.parser.add_argument(
            "db",
            nargs="?",
            help="a jcdb database",
        )
        JCDBList.parser.add_argument(
            "cls",
            nargs="?",
            help="a jcdb class",
        )

        return JCDBList.parser

    @staticmethod
    def main(args=None):

        """
        The main program of 'jcdb list'.
        """

        if args == None:  # parse args using own parser
            JCDBList.generateParser()
            args = JCDBList.parser.parse_args(sys.argv[1:])

        if args.db == None:
            print("The following databases were was found:\n")
            print_table(
                [8, 32],
                [
                    [
                        "DB",
                        e[0],
                    ]
                    for e in JCDB.list(args.db, args.cls)
                ],
            )
        else:
            print("The following elements were found:\n")
            print_table(
                [8, 32],
                [
                    [
                        {True: "OBJECT", False: "CLASS"}[e[1]],
                        e[0],
                    ]
                    for e in JCDB.list(args.db, args.cls)
                ],
            )


if __name__ == "__main__":
    JCDBList.main()
