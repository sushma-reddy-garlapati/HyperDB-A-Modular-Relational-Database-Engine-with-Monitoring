
class Page:
    def __init__(self, page_id, page_size=4096):
        self.page_id = page_id
        self.page_size = page_size
        self.records = []
        self.used_space = 0
        self.deleted_offsets = set()

    def insert_record(self, record: str, reuse_deleted=False):
        encoded = record.encode('utf-8')
        record_size = len(encoded)

        if reuse_deleted and self.deleted_offsets:
            offset = self.deleted_offsets.pop()
            self.records[offset] = encoded
            return offset

        if self.used_space + record_size > self.page_size:
            return None

        offset = len(self.records)
        self.records.append(encoded)
        self.used_space += record_size
        return offset


    def get_records(self):
        return [
            r.decode('utf-8')
            for i, r in enumerate(self.records)
            if i not in self.deleted_offsets
        ]

    def mark_deleted(self, offset):
        self.deleted_offsets.add(offset)


    def read_record(self, offset):
        if offset in self.deleted_offsets:
            return None
        return self.records[offset].decode('utf-8')

    def compact(self):
        new_records = []
        new_deleted = set()
        for i, r in enumerate(self.records):
            if i not in self.deleted_offsets:
                new_records.append(r)
        self.records = new_records
        self.deleted_offsets = new_deleted
        self.used_space = sum(len(r) for r in self.records)






