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

DBLOCATION = "./DB"

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
        return self.action(args)

    def __repr__(self):
        return self.name

##########            util           ##########

def listFiles(path):
    return [f for f in os.listdir(DBLOCATION + path)
            if os.path.isfile(os.path.join(DBLOCATION + path, f))]

##########            verbs          ##########

def verb_create(args):
    if len(args) < 2:
        return "Error: too few arguments for 'create'"
    
    elif len(args) == 2: # create <classname>
        classname = args[1]
        if not os.path.exists(DBLOCATION + "/" + classname):
            os.makedirs(DBLOCATION + "/" + classname)
            return "Created class '" + classname + "'"
        else:
            return "Error: Class '" + classname + "' already exists"
    
    elif len(args) == 3: # create <classname> <instance>
        classname = args[1]
        instancename = args[2]
        if not os.path.exists(DBLOCATION + "/" + classname):
            return "Error: Class '" + classname + "' does not exist"
        if not os.path.exists(DBLOCATION + "/" + classname + "/" + instancename + ".json"):
            f = open(DBLOCATION + "/" + classname + "/" + instancename + ".json", "w")
            f.close()
            return "Created Instance '" + instancename + "' of class '" + classname + "'"
        else:
            return "Error: Instance '" + instancename + "' of class '" + classname + "' already exists"
    
    elif len(args) > 2:
        return "Error: too many arguments for 'create'"

def verb_remove(args):
    if len(args) < 2:
        return "Error: too few arguments for 'remove'"
    
    elif len(args) == 2: # remove <classname>
        classname = args[1]
        if os.path.exists(DBLOCATION + "/" + classname):
            shutil.rmtree(DBLOCATION + "/" + classname)
            return "Removed class '" + classname + "'"
        else:
            return "Error: Class '" + classname + "' does not exist"

    elif len(args) == 3: # remove <classname> <instance>
        classname = args[1]
        instancename = args[2]
        if not os.path.exists(DBLOCATION + "/" + classname):
            return "Error: Class '" + classname + "' does not exist"
        if os.path.exists(DBLOCATION + "/" + classname + "/" + instancename + ".json"):
            os.remove(DBLOCATION + "/" + classname + "/" + instancename + ".json")
            return "Removed Instance '" + instancename + "' of class '" + classname + "'"
        else:
            return "Error: Instance '" + instancename + "' of class '" + classname + "' does not exist"
    
    elif len(args) > 2:
        return "Error: too many arguments for 'remove'"
    

def verb_version(args):
    if len(args) < 1:
        return "Error: too few arguments for 'version'"
    
    elif len(args) == 1: # version
        return "JSON Class DB v0"
    
    elif len(args) > 1:
        return "Error: too many arguments for 'version'"

def verb_quit(args):
    if len(args) < 1:
        return "Error: too few arguments for 'quit'"
    
    elif len(args) == 1: # quit
        sys.exit()
    
    elif len(args) > 1:
        return "Error: too many arguments for 'quit'"

def verb_help(args):
    if len(args) < 1:
        return "Error: too few arguments for 'help'"
    
    elif len(args) == 1: # help
        return "\t" + "\n\n\t".join([str(v) for v in dbVerbs])
    
    elif len(args) > 1:
        return "Error: too many arguments for 'help'"

##########         interpreter       ##########

dbVerbs = [DBVerb("create", verb_create),
           DBVerb("remove", verb_remove),
           DBVerb("help", verb_help),
           DBVerb("version", verb_version),
           DBVerb("quit", verb_quit)]

def interpret(command):
    result = ""
    for c in dbVerbs:
        if c.name == command.split(" ")[0]:
            return c.run(command) + "\n"
    return "command not found\n"
    
def interpret_loop():
    shouldRun = True
    try:
        while shouldRun:
            i = input("dbshell#\t")
            print(interpret(i))
            if i == "quit":
                shouldRun = False
    except KeyboardInterrupt:
        print(interpret("quit"))

##########            main           ##########

if __name__ == "__main__":
    interpret_loop()
