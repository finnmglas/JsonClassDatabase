#! /bin/python3

##########          jcdb.py         ###########
#
#       This script manages a JSON database.
#       Data is stored in classes, in .json
#       files.
#
#       This was recreated on the 28.01.2020,
#       based on an old idea (04.01.2019)
#       by Finn M. Glas
#
#       You are free to use this for your own,
#       private, non-commercial purposes.
#
#       Feel free to contact me at:
#               finnmglas@gmail.com
#
###############################################

##########         imports           ##########

import os
import shutil
import json
import sys

##########           globals         ##########

DBLOCATION = "/var/jcdb"

##########          verb class       ##########

class DBVerb:
    
    def __init__(self, name, callback):
        self.name = name
        self.action = callback

    def splitToTokens(self, command):
        tokens = [""]
        recursionLevel = 0
        inString = False
        tokencount = 0
                
        for char in command:
            if char == "\"":
                inString = not inString
            elif char in ("{", "[") and not inString:
                recursionLevel += 1
            elif char in ("}", "]") and not inString:
                recursionLevel -= 1
            if char == " " and recursionLevel == 0 and not inString:
                tokencount += 1
                tokens.append("")
            else:
                tokens[tokencount] += char
        return tokens                

    def run(self, command):
        args = self.splitToTokens(command)
        if args[0] != self.name:
            return "ERROR: command given to wrong verb"
        return self.action(*args[1:])

    def __repr__(self):
        return self.name

##########            verbs          ##########

"""
    path <db>
    path <db> <class>
    path <db> <class> <instance>
"""
def verb_path(*args):
    if len(args) <= 3:
        p = DBLOCATION + "/" + "/".join(args)
        if len(args) == 3:
            p += ".json"
        return p
    else:
        return "Error: too many arguments for 'path'"

"""
    exists
    exists <db>
    exists <db> <class>
    exists <db> <class> <instance>
"""
def verb_exists(*args):
    if len(args) <= 3:
        return os.path.exists(verb_path(*args))
    else:
        return "Error: too many arguments for 'exists'"

"""
    list
    list <db>
    list <db> <class>
"""
def verb_list(*args):
    if len(args) <= 2:
        if verb_exists(*args):
            r = os.listdir(verb_path(*args))
            if len(args) == 2:
                r = [i.replace(".json", "") for i in r]
            return r
        else:
            return "Error: directory to list does not exist"
    else:
        return "Error: too many arguments for 'exists'"

"""
    create <db>
    create <db> <class>
    create <db> <class> <instance>
"""
def verb_create(*args):
    if len(args) == 0:
        return "Error: too few arguments for 'create'"
    
    elif len(args) == 1: # create <dbname>
        if not verb_exists(*args):
            os.makedirs(verb_path(*args))
            return "Created Database '" + args[0] + "'"
        else:
            return "Error: Database '" + args[0] + "' already exists"
    
    elif len(args) == 2: # create <dbname> <classname>
        if not verb_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not verb_exists(*args):
            os.makedirs(verb_path(*args))
            return "Created Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' already exists"

    elif len(args) == 3: # create <dbname> <classname> <instance>
        if not verb_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not verb_exists(*args[:1]):
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' already exists"
        if not verb_exists(*args):
            f = open(verb_path(*args), "w")
            f.close()
            return "Created Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return "Error: Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "' already exists"
    
    else:
        return "Error: too many arguments for 'create'"

"""
    remove <db>
    remove <db> <class>
    remove <db> <class> <instance>
"""
def verb_remove(*args):
    if len(args) == 0:
        return "Error: too few arguments for 'remove'"
    
    elif len(args) == 1: # remove <dbname>
        if verb_exists(*args):
            shutil.rmtree(verb_path(*args))
            return "Removed Database '" + args[0] + "'"
        else:
            return "Error: Database '" + args[0] + "' does not exist"
    
    elif len(args) == 2: # remove <dbname> <classname>
        if not verb_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if verb_exists(*args):
            shutil.rmtree(verb_path(*args))
            return "Removed Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"

    elif len(args) == 3: # remove <dbname> <classname> <instance>
        if not verb_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not verb_exists(*args[:1]):
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"
        if verb_exists(*args):
            os.remove(verb_path(*args))
            return "Removed Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return "Error: Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"
    
    else:
        return "Error: too many arguments for 'remove'"

"""
    version
"""
def verb_version(*args):
    if len(args) < 1:
        return "Error: too few arguments for 'version'"
    
    elif len(args) == 1: # version
        return "JSON Class DB v0b4"
    
    elif len(args) > 1:
        return "Error: too many arguments for 'version'"

"""
    help
"""
def verb_help(*args):
    if len(args) == 0:
        return """
'path': show the path to an object within the database
    path <db>
    path <db> <class>
    path <db> <class> <instance>

'exists': check if some db, class or instance exists
    exists <db>
    exists <db> <class>
    exists <db> <class> <instance>

'list': show instances in class, classes in db, dbs on sys
    list
    list <db>
    list <db> <class>

'create': create dbs, classes and instances
    create <db>
    create <db> <class>
    create <db> <class> <instance>

'remove': remove dbs, classes and instances
    remove <db>
    remove <db> <class>
    remove <db> <class> <instance>

'version': print the Json Class DB - Version
    version

'help': print this text
    help

'quit': leave the dbshell
    quit"""
    
    else:
        return "Error: too many arguments for 'help'"

"""
    quit
"""
def verb_quit(*args):
    if len(args) == 0:
        sys.exit()
    else:
        return "Error: too many arguments for 'quit'"

##########         interpreter       ##########

dbVerbs = [DBVerb("path", verb_path),
           DBVerb("exists", verb_exists),
           DBVerb("list", verb_list),
           DBVerb("create", verb_create),
           DBVerb("remove", verb_remove),
           DBVerb("help", verb_help),
           DBVerb("version", verb_version),
           DBVerb("quit", verb_quit)]

def interpret(command):
    result = ""
    for c in dbVerbs:
        if c.name == command.split(" ")[0]:
            return str(c.run(command)) + "\n"
    return "Error: command '" + command + "' does not exist\n"
    
def interpret_loop():
    try:
        while True:
            print(interpret(input("dbshell#\t")))
    except KeyboardInterrupt:
        verb_quit()

##########            main           ##########

if __name__ == "__main__":
    interpret_loop()
