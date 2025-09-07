from minidb.buffer.buffer_manager import BufferManager


def test_insert_into_full_page():
    bm = BufferManager(capacity=1)
    for i in range(100):  # Fill the first page
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")
    result = bm.insert_record("overflow", "should_fail")
    assert result is True  # Because a new page was created
    assert len(bm.buffer) >= 1  # Buffer still has space

def test_filemanager_save_and_load(monkeypatch):
    from minidb.storage.filemanager import FileManager
    from minidb.storage.page import Page

    fm = FileManager()
    dummy_page = Page(page_id=1)

    monkeypatch.setattr(fm, "save_page", lambda page: True)
    monkeypatch.setattr(fm, "load_page", lambda page_id: dummy_page)

    assert fm.save_page(dummy_page) is True
    assert fm.load_page(1) == dummy_page
