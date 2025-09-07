import sys
import pytest
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from minidb.buffer.buffer_manager import BufferManager
from minidb.storage.page import Page


def test_insert_and_lookup():
    bm = BufferManager(capacity=2)
    bm.insert_record("user_1", "alice@example.com")
    bm.insert_record("user_2", "bob@example.com")

    assert bm.get_record("user_1") == "user_1: alice@example.com"
    assert bm.get_record("user_2") == "user_2: bob@example.com"

def test_delete_record():
    bm = BufferManager()
    bm.insert_record("user_1", "alice@example.com")
    assert bm.get_record("user_1") is not None

    bm.delete_record("user_1")
    assert bm.get_record("user_1") is None

class DummyMetrics:
    def __init__(self):
        self.counts = {}
    def increment(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1

def test_metrics_increment():
    bm = BufferManager(metrics=DummyMetrics())
    bm.insert_record("user_1", "alice@example.com")
    bm.delete_record("user_1")

    assert bm.metrics.counts["insert_total"] == 1
    assert bm.metrics.counts["delete_total"] == 1


def test_eviction_logic(monkeypatch):
    bm = BufferManager(capacity=1)

    monkeypatch.setattr(bm.file_manager, "save_page", lambda page: setattr(page, "flushed", True))
    monkeypatch.setattr(bm.file_manager, "load_page", lambda page_id: Page(page_id=page_id))

    bm.insert_record("user_1", "alice@example.com")
    bm.insert_record("user_2", "bob@example.com")  # Should trigger eviction

    assert "user_2" in bm.offset_table
    assert "user_1" in bm.offset_table  # Still tracked even if evicted

def test_insert_into_full_page():
    bm = BufferManager(capacity=1)
    for i in range(100):  # Fill the page
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")
    result = bm.insert_record("overflow", "should_fail")
    assert result is True  # Because a new page was created when the first was full


# def test_flush_all(monkeypatch):
#     saved_pages = []

#     def mock_save_page(page):
#         saved_pages.append(page.page_id)

#     bm = BufferManager(capacity=2)
#     monkeypatch.setattr(bm.file_manager, "save_page", mock_save_page)

#     bm.insert_record("user_1", "alice@example.com")
#     bm.insert_record("user_2", "bob@example.com")

#     expected_ids = list(bm.buffer.keys())  # Capture before flush
#     bm.flush_all()

#     assert sorted(saved_pages) == sorted(expected_ids)
#     assert len(bm.buffer) == 0
def test_insert_fails_when_all_pages_full(monkeypatch):
    bm = BufferManager(capacity=2)

    # Create two pages and fill buffer manually
    page1 = Page(page_id=1)
    page2 = Page(page_id=2)
    bm.insert_page(page1)
    bm.insert_page(page2)
    monkeypatch.setattr(Page, "insert_record", lambda self, record, **kwargs: None)


    result = bm.insert_record("overflow", "should_fail")
    assert result is False  # No space, no new page allowed
def test_flush_all(monkeypatch):
    flushed = []

    def mock_save_page(page):
        flushed.append(page.page_id)

    bm = BufferManager(capacity=2)
    monkeypatch.setattr(bm.file_manager, "save_page", mock_save_page)

    bm.insert_record("user_1", "alice@example.com")
    bm.insert_record("user_2", "bob@example.com")

    expected_ids = list(bm.buffer.keys())
    bm.flush_all()

    assert sorted(flushed) == sorted(expected_ids)
    assert len(bm.buffer) == 0

