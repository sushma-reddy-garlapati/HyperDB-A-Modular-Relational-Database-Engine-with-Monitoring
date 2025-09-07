class HashIndex:
    def __init__(self):
        self.index = {}  # key → page_id

    def insert(self, key: str, page_id: int):
        self.index[key] = page_id

    def lookup(self, key: str):
        return self.index.get(key)

    def delete(self, key: str):
        if key in self.index:
            del self.index[key]

    def keys(self):
        return list(self.index.keys())
