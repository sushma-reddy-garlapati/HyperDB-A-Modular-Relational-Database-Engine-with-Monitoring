from fastapi import FastAPI, Query
from minidb.storage.page import Page
from minidb.buffer.buffer_manager import BufferManager
from minidb.index.index import HashIndex
from minidb.query.query_engine import QueryEngine
from fastapi import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from minidb.monitoring.metrics import api_requests_total
from minidb.monitoring.metrics import registry

app = FastAPI()
bm = BufferManager(capacity=5)
index = HashIndex()
qe = QueryEngine(buffer_manager=bm)

@app.post("/insert")
def insert_record(key: str, value: str):
    page = Page(page_id=len(index.keys()) + 1)
    page.insert_record(f"{key}: {value}")
    bm.insert_page(page)
    index.insert(key, page.page_id)
    return {"status": "inserted", "key": key, "page_id": page.page_id}

@app.get("/lookup")
def lookup_record(key: str = Query(...)):
    page_id = index.lookup(key)
    if page_id is None:
        return {"error": "Key not found"}
    page = bm.get_page(page_id)
    return {"records": page.get_records()}

@app.get("/query")
def query(keyword: str = Query(...)):
    scanned = qe.scan(list(index.index.values()))
    filtered = qe.filter(scanned, keyword)
    return {"results": filtered}

@app.middleware("http")
async def count_requests(request, call_next):
    api_requests_total.inc()
    response = await call_next(request)
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

