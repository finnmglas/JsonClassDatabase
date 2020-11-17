import os, json
from cliprint import color

from .object import Object

DEFAULT_OBJECT_STORAGE = os.path.join(os.path.expanduser("~"), ".jcdb")


class JCDB:

    """
    The JSON Class Database.
    """

    @staticmethod
    def makePath(db=None, cls=None, inst=None):
        path = DEFAULT_OBJECT_STORAGE

        if db:
            path = os.path.join(path, db)

        if cls:
            path = os.path.join(path, *cls.split("."))

        if inst:
            path = os.path.join(path, JCDB.innerInstPathToDir(inst)[0])

        return path

    @staticmethod
    def innerInstPathToDir(inst):  # return tuple (filename, attr)
        sp = inst.split(".")
        return (sp[0] + ".json", ".".join(sp[1:]))

    @staticmethod
    def exists(db, cls=None, inst=None):
        return os.path.exists(JCDB.makePath(db, cls, inst))

    @staticmethod
    def list(db=None, cls=None):  # returns tuples (name, isfile)
        dir = JCDB.makePath(db, cls)
        return [
            (d.replace(".json", ""), os.path.isfile(os.path.join(dir, d)))
            for d in os.listdir(dir)
        ]

    @staticmethod
    def get(db, cls, inst):
        dir = JCDB.makePath(db, cls, inst)

        if not JCDB.exists(dir):
            raise ValueError("No JCDB object found at '" + dir + "'")

        with open(dir) as f:
            contents = f.read()

        return contents

    @staticmethod
    def get_json(db, cls, inst):
        dir = JCDB.makePath(db, cls, inst)
        return json.load(open(dir))

    @staticmethod
    def get_object(db, cls, inst):
        from .object import Object

        dir = JCDB.makePath(db, cls, inst)
        o = Object.decodeFile(dir)

        sub = JCDB.innerInstPathToDir(inst)[1]

        if sub:
            try:
                return eval("o." + sub)
            except AttributeError:
                return color.f.red + "undefined" + color.end
        else:
            return o
