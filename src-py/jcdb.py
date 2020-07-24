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
#       See the README for more info
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
DOCS = ""

##########          functions        ##########

ERRORS = {
            "INVALID_DBLOC": "DBLOCATION '{}' does not exist",
            "WRONG_OP":      "command given to wrong operation",
            "INVALID_OP":    "operation '{}' does not exist",
            "MANY_ARGS":     "too many arguments for '{}'",
            "FEW_ARGS":      "too few arguments for '{}'",
            "INVALID_DB":    "database '{}' does not exist",
            "EXISTS_DB":     "database '{}' already exists",
            "INVALID_CLASS": "database '{}': class '{}' does not exist",
            "EXISTS_CLASS":  "database '{}': class '{}' does already exists",
            "INVALID_INST":  "database '{}': class '{}': instance '{}' does not exist",
            "EXISTS_INST":   "database '{}': class '{}': instance '{}' does already exist",
            "JSON_ERR":      "json decoding failed",
            "INVALID_ATTR":  "attribute '{}' does not exist"
    }

def error(err, *args):
    return "Error: " + ERRORS[err].format(*args)

##########         DBOperation       ##########

class DBOperation:
    
    def __init__(self, name, callback, documentation):
        global DOCS
        self.name = name
        self.action = callback
        DOCS += documentation

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
            # Consider "DB" the same input as DB
            if (len(tokens[tokencount]) > 2 and
                tokens[tokencount][0] == "\"" and
                tokens[tokencount][-1] == "\""):
                tokens[tokencount] = eval(tokens[tokencount])
        return tokens                

    def run(self, command):
        name, *args = self.splitToTokens(command)
        if name != self.name:
            return error("WRONG_OP")
        return self.action(*args)

    def __repr__(self):
        return self.name

##########         operations        ##########

doc_op_path = """
'path': show the path to an object within the database
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
        return error("MANY_ARGS", "path")

    #####

doc_op_exists = """
'exists': check if some db, class or instance exists
    exists
    exists <db>
    exists <db> <class>
    exists <db> <class> <instance>
"""

def op_exists(*args):
    if len(args) <= 3:
        return os.path.exists(op_path(*args))
    else:
        return error("MANY_ARGS", "exists")

    #####

doc_op_list = """
'list': show instances in class, classes in db, dbs on sys
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
            if len(args) == 2:
                return error("INVALID_CLASS", args[0], args[1])
            elif len(args) == 1:
                return error("INVALID_DB", args[0])
            else:
                return error("INVALID_DBLOC", DBLOCATION)
    else:
        return error("MANY_ARGS", "list")

    #####

doc_op_get = """
'get': get json instances and their attributes
    get <db> <class> <instance>
    get <db> <class> <instance> <attribute>
"""

def op_get(*args):
    if len(args) < 3:
        return error("FEW_ARGS", "get")
    elif len(args) == 3:
        if not op_exists(args[0]):
            return error("INVALID_DB", args[0])
        if not op_exists(*args[:1]):
            return error("INVALID_CLASS", *args[:1])
        if op_exists(*args):
            f = open(op_path(*args))
            content = f.read()
            f.close()
            return content
        else:
            return error("INVALID_INST", *args)
    elif len(args) == 4:
        content = op_get(*args[:-1])
        if content.split(" ")[0] == "Error:":
            return content

        try:
            jobject = json.loads(content)
        except json.decoder.JSONDecodeError:
            return error("JSON_ERR")
        if args[-1] in list(jobject.keys()):
            return jobject[args[-1]]
        else:
            return error("INVALID_ATTR", args[-1])
    else:
        return error("MANY_ARGS", "get")

    #####

doc_op_set = """
'set': set json instances and their attributes
    set <db> <class> <instance> <jsonstr>
    set <db> <class> <instance> <attribute> <value>
"""

def op_set(*args):
    if len(args) < 4:
        return error("FEW_ARGS", "set")
    elif len(args) == 4: # inst = json
        if not op_exists(args[0]):
            return error("INVALID_DB", args[0])
        if not op_exists(*args[:-2]):
            return error("INVALID_CLASS", args[0], args[1])
        else: # if json file does not exist, just create
            try:
                jobject = json.loads(args[-1])
            except json.decoder.JSONDecodeError:
                return error("JSON_ERR")
            
            f = open(op_path(*args[:-1]), "w")
            f.write(json.dumps(jobject, indent=4, sort_keys=True))
            f.close()
            return "Successfully written json to '" + args[-2] + "'"

    elif len(args) == 5:
        content = op_get(*args[:-2])
        if content.split(" ")[0] == "Error:":
            return content
        try:
            jobject = json.loads(content)
            index = args[-2]
            value = json.loads(args[-1])
        except json.decoder.JSONDecodeError:
            return error("JSON_ERR")
            
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
        return error("MANY_ARGS", "set")

    #####

doc_op_create = """
'create': create dbs, classes and instances
    create <db>
    create <db> <class>
    create <db> <class> <instance>
"""

def op_create(*args):
    if len(args) == 0:
        return error("FEW_ARGS", "create")
    
    elif len(args) == 1:
        if not op_exists(*args):
            os.makedirs(op_path(*args))
            return "Created Database '" + args[0] + "'"
        else:
            return error("EXISTS_DB", args[0])
    
    elif len(args) == 2:
        if not op_exists(args[0]):
            return error("INVALID_DB", args[0])
        if not op_exists(*args):
            os.makedirs(op_path(*args))
            return "Created Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return error("EXISTS_CLASS", *args)

    elif len(args) == 3:
        if not op_exists(args[0]):
            return error("INVALID_DB", args[0])
        if not op_exists(*args[:1]):
            return error("INVALID_CLASS", args[0], args[1])
        if not op_exists(*args):
            f = open(op_path(*args), "w")
            f.write("{}")
            f.close()
            return "Created Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return error("EXISTS_INST", *args)
    
    else:
        return error("MANY_ARGS", "create")

    #####

doc_op_remove = """
'remove': remove dbs, classes and instances
    remove <db>
    remove <db> <class>
    remove <db> <class> <instance>
"""

def op_remove(*args):
    if len(args) == 0:
        return error("FEW_ARGS", "remove")
    
    elif len(args) == 1:
        if op_exists(*args):
            shutil.rmtree(op_path(*args))
            return "Removed Database '" + args[0] + "'"
        else:
            return error("INVALID_DB", args[0])
    
    elif len(args) == 2:
        if not op_exists(args[0]):
            return error("INVALID_DB", args[0])
        if op_exists(*args):
            shutil.rmtree(op_path(*args))
            return "Removed Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return error("INVALID_CLASS", args[0], args[1])

    elif len(args) == 3:
        if not op_exists(args[0]):
            return error("INVALID_DB", args[0])
        if not op_exists(*args[:1]):
            return error("INVALID_CLASS", args[0], *args[:1])
        if op_exists(*args):
            os.remove(op_path(*args))
            return "Removed Instance '" + args[2] + "' of Class '" + args[1] + "' in Database '" + args[0] + "'"
        else:
            return error("INVALID_INST", *args)
    else:
        return error("MANY_ARGS", "remove")

    #####

doc_op_version = """
'version': print the Json Class DB - Version
    version
"""

def op_version(*args):
    if len(args) == 0:
        return "JSON Class DB " + VERSION
    
    elif len(args) > 1:
        return error("MANY_ARGS", "version")

    #####

doc_op_help = """
'help': print this text
    help
"""

def op_help(*args):
    if len(args) == 0:
        return "\n----- Usage -----\n" + "".join(DOCS)
    else:
        return error("MANY_ARGS", "help")

##########         interpreter       ##########

dbOps = [DBOperation("path",    op_path,    doc_op_path),
         DBOperation("exists",  op_exists,  doc_op_exists),
         DBOperation("list",    op_list,    doc_op_list),
         DBOperation("get",     op_get,     doc_op_get),
         DBOperation("set",     op_set,     doc_op_set),
         DBOperation("create",  op_create,  doc_op_create),
         DBOperation("remove",  op_remove,  doc_op_remove),
         DBOperation("help",    op_help,    doc_op_help),
         DBOperation("version", op_version, doc_op_version)]

def interpret(command):
    result = ""
    for c in dbOps:
        if c.name == command.split(" ")[0]:
            return str(c.run(command)) + "\n"
    return error("INVALID_OP", command.split(" ")[0])

##########            main           ##########

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Type 'jcdb' followed by your command")
    else:
        print(interpret(" ".join(sys.argv[1:])))
