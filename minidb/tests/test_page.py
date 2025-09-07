import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from minidb.storage.page import Page
from minidb.buffer.buffer_manager import BufferManager


def test_insert_and_read():
    page = Page(page_id=1)
    offset = page.insert_record("user_1: alice@example.com")
    assert offset == 0
    assert page.read_record(offset) == "user_1: alice@example.com"

def test_mark_deleted():
    page = Page(page_id=1)
    offset = page.insert_record("user_1: alice@example.com")
    page.mark_deleted(offset)
    assert page.read_record(offset) is None

def test_get_records_excludes_deleted():
    page = Page(page_id=1)
    offset1 = page.insert_record("user_1: alice@example.com")
    offset2 = page.insert_record("user_2: bob@example.com")
    page.mark_deleted(offset1)

    records = page.get_records()
    assert len(records) == 1
    assert records[0] == "user_2: bob@example.com"
# def test_reuse_deleted_slot():
#     page = Page(page_id=1)
#     offset1 = page.insert_record("user_1: alice@example.com")
#     page.mark_deleted(offset1)

#     offset2 = page.insert_record("user_2: bob@example.com")
#     assert offset2 == offset1  # Should reuse the deleted slot
#     assert page.read_record(offset2) == "user_2: bob@example.com"
def test_compact_page():
    page = Page(page_id=1)
    page.insert_record("user_1: alice@example.com")
    page.insert_record("user_2: bob@example.com")
    page.mark_deleted(0)

    before = page.get_records()
    assert len(before) == 1

    page.compact()
    after = page.get_records()
    assert len(after) == 1
    assert after[0] == "user_2: bob@example.com"
    assert page.used_space == sum(len(r.encode('utf-8')) for r in after)
def test_reuse_deleted_slot():
    page = Page(page_id=1)
    offset1 = page.insert_record("user_1: alice@example.com")
    page.mark_deleted(offset1)

    offset2 = page.insert_record("user_2: bob@example.com", reuse_deleted=True)
    assert offset2 == offset1  # Should reuse the deleted slot

def test_slot_reuse_via_buffer():
    bm = BufferManager()
    bm.insert_record("user_1", "alice@example.com")
    bm.delete_record("user_1")
    bm.insert_record("user_2", "bob@example.com")
    assert bm.get_record("user_2") == "user_2: bob@example.com"

