from random import randint


def public_vars(obj):
    return {key: getattr(obj, key)
            for key in dir(obj)
            if not key.startswith("_") and not callable(getattr(obj, key))}


class DBItem(object):
    ID_PROPERTY = ''
    CONTAINS_ITEMS = []

    def __init__(self):
        self._id = randint(0, 100000)

    @property
    def id(self):
        if self.ID_PROPERTY == '':
            return self._id
        return getattr(self, self.ID_PROPERTY)

    @id.setter
    def id(self, value):
        pass

    def encode(self):
        encoded = public_vars(self)
        if self.ID_PROPERTY == '':
            encoded['id'] = self.id

        return self.id, encoded

    @staticmethod
    def decode(s):
        raise NotImplementedError('To be overridden!')


class TestObject(DBItem):
    @staticmethod
    def decode(s):
        pass

    def __init__(self, name, age):
        super(TestObject, self).__init__()
        self.name = name
        self.age = age
