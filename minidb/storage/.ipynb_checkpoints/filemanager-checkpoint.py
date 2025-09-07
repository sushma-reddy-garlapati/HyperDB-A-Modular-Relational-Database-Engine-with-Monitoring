import os
import pickle
from minidb.storage.page import Page

class FileManager:
    def __init__(self, db_path="data"):
        self.db_path = db_path
        os.makedirs(self.db_path, exist_ok=True)

    def save_page(self, page: Page):
        file_path = os.path.join(self.db_path, f"page_{page.page_id}.bin")
        with open(file_path, "wb") as f:
            pickle.dump(page, f)

    def load_page(self, page_id: int) -> Page:
        file_path = os.path.join(self.db_path, f"page_{page_id}.bin")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Page {page_id} not found.")
        with open(file_path, "rb") as f:
            page = pickle.load(f)
        return page
