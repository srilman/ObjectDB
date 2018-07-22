from .table import DBObject
from .proxy import JSONProxy
from .utils import LRUCache, itervalues


class ObjectDB(object):
    def __init__(self, path, cache_size=5, proxy=None):
        """
        :param path: Path to the folder where table class files will be stored
        :param cache_size: Size of cache for storing responses for intended requests
        :param proxy: Item of Proxy class for reading and writing file
        """
        self._proxy = proxy
        if self._proxy is None:
            self._proxy = JSONProxy(path)

        self._query_cache = LRUCache(capacity=cache_size)
        self._opened = True
        self._tables = self._proxy.read()

    def _write(self):
        encoded_data = {key: self._data[key].encode() for key in self._data}
        self._query_cache.clear()
        self._proxy.write(encoded_data)

    def save(self):
        self._write()

    # --------- Modified Set Functions ----------
    def _set(self, new_val):
        self._data = new_val
        self._write()

    def _set_index(self, key, new_val):
        if key in self._data:
            raise ValueError("Key Already Exists")
        self._data[key] = new_val
        if self._write_on_save:
            self._write()

    def _merge(self, new_val):
        for key in new_val:
            if key in self._data:
                raise ValueError("Key Already Exists")
            self._data[key] = new_val[key]
        if self._write_on_save:
            self._write()

    # --------- End Modified Set Functions ----------

    def _clear_cache(self):
        self._query_cache.clear()

    def close(self):
        self._opened = False
        self._proxy.close()

    def all(self):
        return self._data.values()

    def contains(self, cond):
        pass

    def count(self, cond):
        pass

    def get(self, cond):
        pass

    def purge(self):
        self._set({})

    # ------- CRUD Commands --------
    def insert(self, elem):
        if not isinstance(elem, self._table_class):
            raise ValueError("Document is not Specified Database Object")

        self._set_index(elem.get_id(), elem)
        return elem.get_id()

    def insert_multiple(self, elems):
        merge_dict = {}
        for elem in elems:
            if not isinstance(elem, self._table_class):
                raise ValueError("Document is not Specified Database Object")
            elif elem.get_id() in merge_dict:
                raise ValueError("Repeated ID in the arrays")
            merge_dict[elem.get_id()] = elem

        self._merge(merge_dict)

    def remove(self):
        pass

    # ----------- Internal Functions -------------
    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._opened:
            self.close()

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for value in itervalues(self._data):
            yield value

    def search(self, cond, val):
        docs = [doc for doc in self._data if doc[cond] == val]
        return docs[:]

    def hard_search(self, cond):
        docs = [doc for doc in self.all() if cond(doc)]
        return docs[:]

    # ----------- Changing the Database -----------
    def update(self, id, values):
        item = self._data[id]
        for key in values:
            setattr(item, key, values[key])
        self.save()

    def remove(self, cond=None, ):
        if cond is None :
            raise RuntimeError('Use purge() to remove all documents')

        return self.process_elements(
            lambda data, doc_id: data.pop(doc_id),
            cond, doc_ids
        )


class Table(object):


