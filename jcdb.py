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
VERSION = "v1.0"

##########          DBCommand        ##########

class DBCommand:
    
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
                #print(char)
                tokens[tokencount] += char
             # "DB" is the same input as DB
            if (len(tokens[tokencount]) > 2 and
                tokens[tokencount][0] == "\"" and
                tokens[tokencount][-1] == "\""):
                tokens[tokencount] = eval(tokens[tokencount])
        return tokens                

    def run(self, command):
        name, *args = self.splitToTokens(command)
        if name != self.name:
            return "ERROR: command given to wrong operation"
        return self.action(*args)

    def __repr__(self):
        return self.name

##########         operations        ##########

"""
    path <db>
    path <db> <class>
    path <db> <class> <instance>
"""
def op_path(*args):
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
def op_exists(*args):
    if len(args) <= 3:
        return os.path.exists(op_path(*args))
    else:
        return "Error: too many arguments for 'exists'"

"""
    list
    list <db>
    list <db> <class>
"""
def op_list(*args):
    if len(args) <= 2:
        if op_exists(*args):
            r = os.listdir(op_path(*args))
            if len(args) == 2:
                r = [i.replace(".json", "") for i in r]
            return r
        else:
            return "Error: directory to list does not exist"
    else:
        return "Error: too many arguments for 'exists'"

"""
    get <db> <class> <instance>
    get <db> <class> <instance> <attribute>
"""
def op_get(*args):
    if len(args) < 3:
        return "Error: too few arguments for 'get'"
    elif len(args) == 3:
        if not op_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not op_exists(*args[:1]):
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"
        if op_exists(*args):
            f = open(op_path(*args))
            content = f.read()
            f.close()
            return content
        else:
            return "Error: Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"
    elif len(args) == 4:
        content = op_get(*args[:-1])
        if content.split(" ")[0] != "Error:":
            try:
                jobject = json.loads(content)
            except json.decoder.JSONDecodeError:
                return "Error: Json decoding failed"
            if args[-1] in list(jobject.keys()):
                return jobject[args[-1]]
            else:
                return "Error: Attribute does not exist"
        else:
            return "Error: 'get': " + content
    else:
        return "Error: too many arguments for 'get'"

"""
    set <db> <class> <instance> <jsonstr>
    set <db> <class> <instance> <attribute> <value>
"""
def op_set(*args):
    if len(args) < 4:
        return "Error: too few arguments for 'set'"
    elif len(args) == 4: # inst = json
        if not op_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not op_exists(*args[:-2]):
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"
        else: # if json file does not exist, just create
            try:
                jobject = json.loads(args[-1])
            except json.decoder.JSONDecodeError:
                return "Error: Json decoding failed"
            
            f = open(op_path(*args[:-1]), "w")
            f.write(json.dumps(jobject, indent=4, sort_keys=True))
            f.close()
            return "Successfully written json to '" + args[-2] + "'"

    elif len(args) == 5: # inst[attr] = json
        content = op_get(*args[:-2])
        if content.split(" ")[0] != "Error:":
            try:
                jobject = json.loads(content)
                index = args[-2]
                value = json.loads(args[-1])
            except json.decoder.JSONDecodeError:
                return "Error: Json decoding failed"
            
            if type(jobject) == type(dict()):
                jobject[index] = value
            else:
                jobject = {}
                jobject[index] = value

            f = open(op_path(*args[:-2]), "w")
            f.write(json.dumps(jobject, indent=4, sort_keys=True))
            f.close()
            
            return "Successfully written attribute to '" + args[-3] + "'"
        else:
            return "Error: 'get': " + content
    else:
        return "Error: too many arguments for 'set'"

"""
    create <db>
    create <db> <class>
    create <db> <class> <instance>
"""
def op_create(*args):
    if len(args) == 0:
        return "Error: too few arguments for 'create'"
    
    elif len(args) == 1: # create <dbname>
        if not op_exists(*args):
            os.makedirs(op_path(*args))
            return "Created Database '" + args[0] + "'"
        else:
            return "Error: Database '" + args[0] + "' already exists"
    
    elif len(args) == 2: # create <dbname> <classname>
        if not op_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not op_exists(*args):
            os.makedirs(op_path(*args))
            return "Created Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' already exists"

    elif len(args) == 3: # create <dbname> <classname> <instance>
        if not op_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not op_exists(*args[:1]):
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' already exists"
        if not op_exists(*args):
            f = open(op_path(*args), "w")
            f.write("{}")
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
def op_remove(*args):
    if len(args) == 0:
        return "Error: too few arguments for 'remove'"
    
    elif len(args) == 1: # remove <dbname>
        if op_exists(*args):
            shutil.rmtree(op_path(*args))
            return "Removed Database '" + args[0] + "'"
        else:
            return "Error: Database '" + args[0] + "' does not exist"
    
    elif len(args) == 2: # remove <dbname> <classname>
        if not op_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if op_exists(*args):
            shutil.rmtree(op_path(*args))
            return "Removed Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"

    elif len(args) == 3: # remove <dbname> <classname> <instance>
        if not op_exists(args[0]):
            return "Error: Database '" + args[0] + "' does not exist"
        if not op_exists(*args[:1]):
            return "Error: Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"
        if op_exists(*args):
            os.remove(op_path(*args))
            return "Removed Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return "Error: Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "' does not exist"
    
    else:
        return "Error: too many arguments for 'remove'"

"""
    version
"""
def op_version(*args):
    if len(args) == 0: # version
        return "JSON Class DB " + VERSION
    
    elif len(args) > 1:
        return "Error: too many arguments for 'version'"

"""
    help
"""
def op_help(*args):
    if len(args) == 0:
        return """
----- Usage -----

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

'get': get json instances and their attributes
    get <db> <class> <instance>
    get <db> <class> <instance> <attribute>

'set': set json instances and their attributes
    set <db> <class> <instance> <jsonstr>
    set <db> <class> <instance> <attribute> <value>

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
def op_quit(*args):
    if len(args) == 0:
        sys.exit()
    else:
        return "Error: too many arguments for 'quit'"

##########         interpreter       ##########

dbOps = [DBCommand("path", op_path),
           DBCommand("exists", op_exists),
           DBCommand("list", op_list),
           DBCommand("get", op_get),
           DBCommand("set", op_set),
           DBCommand("create", op_create),
           DBCommand("remove", op_remove),
           DBCommand("help", op_help),
           DBCommand("version", op_version),
           DBCommand("quit", op_quit)]

def interpret(command):
    result = ""
    for c in dbOps:
        if c.name == command.split(" ")[0]:
            return str(c.run(command)) + "\n"
    return "Error: command '" + command + "' does not exist\n"

##########            main           ##########

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Type 'jcdb' followed by your command")
    else:
        print(interpret(" ".join(sys.argv[1:])))
