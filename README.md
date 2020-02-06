# Json Class Database

A simple, yet effective key-value database. Data is sorted into different classes, that contain instances stored in JSON files.
The database serves the purpose of facilitating the storage of shared data, while giving the user an easy way to manipulate,
search or add the stored data.

## Installation

To install, clone this repository and run './install.sh' from your console

## Usage

By running `jcdb` in your terminal, you can access the database.

The following commands can be used:

```
'path': show the path to an object within the database
    path <db>
    path <db> <class>
    path <db> <class> <instance>

'exists': check if some db, class or instance exists
    exists
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

'help': print this text
    help

'version': print the Json Class DB - Version
    version
```

## Example usage

Creating a examle database and modifying it:

```
jcdb create DB1
jcdb create DB1 Class1
jcdb set DB1 Class1 Inst1 "attribute" '{"subattribute:"value"}'
jcdb set DB1 Class1 Inst1 "attribute2" 42
jcdb get DB1 Class1 Inst1
```

