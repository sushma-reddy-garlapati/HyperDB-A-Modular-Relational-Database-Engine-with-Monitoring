from collections import OrderedDict
from minidb.storage.filemanager import FileManager
from minidb.storage.page import Page
from minidb.monitoring.metrics import buffer_evictions_total
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class BufferManager:

    def __init__(self, capacity=5, metrics=None):
        self.capacity = capacity
        self.buffer = OrderedDict()
        self.file_manager = FileManager()
        self.offset_table = {}
        self.metrics = metrics


    def get_page(self, page_id):
        if page_id in self.buffer:
            self.buffer.move_to_end(page_id)
            return self.buffer[page_id]
        page = self.file_manager.load_page(page_id)
        self.insert_page(page)
        return page

    def insert_page(self, page: Page):
        if page.page_id in self.buffer:
            self.buffer.move_to_end(page.page_id)
        else:
            if len(self.buffer) >= self.capacity:
                self.evict_page()
            self.buffer[page.page_id] = page

    def evict_page(self):
        evicted_id, evicted_page = self.buffer.popitem(last=False)
        self.file_manager.save_page(evicted_page)
        self.offset_table = {
    k: v for k, v in self.offset_table.items() if v[0] != evicted_id
}
        buffer_evictions_total.inc()
        print(f"Evicted page {evicted_id} from buffer.")
        logger.info(f"Evicted page {evicted_id} from buffer.")

    def flush_all(self):
        for page_id, page in self.buffer.items():
            self.file_manager.save_page(page)
        self.buffer.clear()

    def insert_record(self, key: str, value: str):
        for page in self.buffer.values():
            offset = page.insert_record(f"{key}: {value}")
            if offset is not None:
                self.offset_table[key] = (page.page_id, offset)
                if self.metrics:
                    self.metrics.increment("insert_total")
                return True
    
        new_page_id = max(self.buffer.keys(), default=0) + 1
        new_page = Page(page_id=new_page_id)
        offset = new_page.insert_record(f"{key}: {value}", reuse_deleted=True)
        if offset is not None:
            self.offset_table[key] = (new_page.page_id, offset)
            self.insert_page(new_page)
            if self.metrics:
                self.metrics.increment("insert_total")
            return True
        return False


    def delete_record(self, key: str):
        if key not in self.offset_table:
            return False
        page_id, offset = self.offset_table[key]
        page = self.get_page(page_id)
        if page:
            page.mark_deleted(offset)
            del self.offset_table[key]
            if self.metrics:
                self.metrics.increment("delete_total")
            return True
        return False

    def get_record(self, key: str):
        if key not in self.offset_table:
            return None
        page_id, offset = self.offset_table[key]
        page = self.get_page(page_id)
        if page:
            return page.read_record(offset)
        return None



