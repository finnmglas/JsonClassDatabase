import os

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
            path = os.path.join(path, inst + ".json")

        return path

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
