# Json Class Database

A simple, yet effective key-value database. Data is sorted into different classes, that contain instances stored in JSON files.
The database serves the purpose of facilitating the storage of shared data, while giving the user an easy way to manipulate,
search or add the stored data.

## Usage

By running `python3 jcdb.py` in your terminal, you start the **dbshell**.

The following commands can be used:

```
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

'show': print a instance of a class in a specific db
    show <db> <class> <instance>

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
    quit
```

