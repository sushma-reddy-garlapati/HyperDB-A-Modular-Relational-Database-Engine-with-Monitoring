
def test_insert_and_retrieve():
    from minidb.storage.page import Page
    page = Page(page_id=1)
    offset = page.insert_record("test")
    assert offset is not None
    assert page.read_record(offset) == "test"
