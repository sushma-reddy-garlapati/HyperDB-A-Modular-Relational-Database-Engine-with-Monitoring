

import streamlit as st
from minidb.buffer.buffer_manager import BufferManager
from minidb.index.index import HashIndex
from minidb.query.query_engine import QueryEngine
from minidb.storage.page import Page
import requests
import json
from collections import Counter
import time
# ------------------ Setup ------------------
st.set_page_config(page_title="HyperDB Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
# HyperDB: Real-Time Queryable Database Engine
HyperDB is a modular, in-memory database engine with real-time JSON ingestion, custom query language, and live Prometheus metrics. Built with FastAPI and Streamlit, it supports structured filtering, aggregation, joins, and dashboard-based analytics for rapid data exploration.
""")

st.sidebar.title("HyperDB") 
st.sidebar.markdown("Designed and built by Sushmareddy")

# ------------------ Session State ------------------
if "bm" not in st.session_state:
    st.session_state.bm = BufferManager(capacity=5)
if "index" not in st.session_state:
    st.session_state.index = HashIndex()
if "qe" not in st.session_state:
    st.session_state.qe = QueryEngine(buffer_manager=st.session_state.bm)

bm = st.session_state.bm
index = st.session_state.index
qe = st.session_state.qe

# ------------------ Query Parser ------------------
def parse_query(query_str):
    tokens = query_str.strip().split(" ", 1)
    if len(tokens) != 2 or "=" not in tokens[1]:
        return {"type": "invalid"}
    command, condition = tokens
    field, value = condition.split("=", 1)
    return {"type": command.upper(), "field": field.strip(), "value": value.strip()}

def run_query(parsed, records):
    results = []
    for r in records:
        try:
            json_str = r.split(": ", 1)[1]
            data = json.loads(json_str)
            if parsed["field"] in data:
                val = str(data[parsed["field"]])
                if parsed["value"].startswith("*"):
                    if val.endswith(parsed["value"][1:]):
                        results.append(r)
                else:
                    if val == parsed["value"]:
                        results.append(r)
        except:
            continue
    return results

# ------------------ Tabs ------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Insert & Lookup", "Query Engine", "Analytics", "Buffer State", "System Metrics"])

# ------------------ Tab 1: Insert & Lookup ------------------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Insert Record")
        key = st.text_input("Key", key="insert_key")
        value = st.text_input("Value", key="insert_value")
        if st.button("Insert", key="insert_button"):
            success = bm.insert_record(key, value)
            if success:
                st.success(f"Inserted: {key}")
            else:
                st.error("Insert failed — page may be full")

        
        # 🔹 View Active Records
        st.subheader("Active Records in Buffer")
        for page in bm.buffer.values():
            st.markdown(f"**Page {page.page_id}**")
            st.write(page.get_records())

    with col2:
        st.subheader("Find Record")
        lookup_key = st.text_input("Lookup Key", key="lookup_key")
        if st.button("Lookup", key="lookup_button"):
            result = bm.get_record(lookup_key)
            if result:
                st.success(f"Found: {result}")
            else:
                st.error("Key not found or record deleted")

        # 🔹 Delete Record Section
        st.subheader("Delete Record")
        active_keys = list(bm.offset_table.keys())
        delete_key = st.selectbox("Select Key to Delete", active_keys, key="delete_key")
        
        if st.button("Delete", key="delete_button"):
            success = bm.delete_record(delete_key)
            if success:
                st.success(f"Deleted record with key: {delete_key}")
            else:
                st.error("Key not found or already deleted")
        
        # 🔹 Deleted Records Viewer
        st.subheader("Deleted Records")
        if st.checkbox("Show Deleted Records"):
            for page in bm.buffer.values():
                deleted = []
                for i in page.deleted_offsets:
                    try:
                        deleted.append(page.records[i].decode('utf-8'))
                    except Exception:
                        deleted.append(f"[Corrupted record at offset {i}]")
                if deleted:
                    st.markdown(f"**Page {page.page_id}**")
                    st.write(deleted)


        
        st.subheader("Sample Data")
        if st.button("Insert Sample Users", key="sample_users"):
            sample_data = {
                "user_1": "email_1@example.com",
                "user_2": "email_2@example.com",
                "user_3": "email_3@example.com",
                "user_4": "email_4@example.com",
                "user_5": "email_5@example.com",
                "user_6": "email_6@example.com",
            }
            for key, value in sample_data.items():
                bm.insert_record(key, value)
            st.success("Inserted sample users into HyperDB!")


# ------------------ Tab 2: Query Engine ------------------
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Keyword Filter")
        keyword = st.text_input("Filter Keyword", key="filter_keyword")
        if st.button("Run Filter", key="run_query_filter"):
            scanned = qe.scan(list(index.index.values()))
            filtered = qe.filter(scanned, keyword)
            st.write(filtered)

        st.subheader("Custom Query Language")
        query_input = st.text_input("Enter query (e.g. FIND role=engineer)", key="mini_query_input")
        if st.button("Run Query", key="run_query_mini"):
            parsed = parse_query(query_input)
            scanned = qe.scan(list(index.index.values()))
            if parsed["type"] == "FIND":
                results = run_query(parsed, scanned)
                st.write(results)
            elif parsed["type"] == "COUNT":
                results = run_query(parsed, scanned)
                st.write(f"Count: {len(results)}")
            else:
                st.warning("Invalid query format. Use FIND or COUNT with field=value.")
    with col2:
        st.subheader("Join Test")
        if st.button("Run Join on Pages 1 and 2", key="join_button"):
            page1 = bm.get_page(1)
            page2 = bm.get_page(2)
            if page1 and page2:
                joined = qe.join(
                    page1.get_records(),
                    page2.get_records(),
                    key_func=lambda r: r.split(":")[0].strip()
                )
                st.write(joined)
            else:
                st.warning("Pages 1 and 2 not found in buffer.")

# ------------------ Tab 3: Analytics ------------------
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Aggregation Test")
        if st.button("Count Records Containing 'email'", key="agg_email"):
            scanned = qe.scan(list(index.index.values()))
            filtered = qe.filter(scanned, "email")
            count = qe.aggregate(filtered, lambda vals: len(vals))
            st.write(f"Total matching records: {count}")
    with col2:
        st.subheader("Insert JSON Record")
        raw_json = st.text_area("Paste JSON Record", key="json_input")
        if st.button("Insert JSON", key="insert_json"):
            try:
                parsed = json.loads(raw_json)
                records = parsed if isinstance(parsed, list) else [parsed]
                for record in records:
                    key = record["id"]
                    value = json.dumps(record)
                    page = Page(page_id=len(index.keys()) + 1)
                    page.insert_record(f"{key}: {value}")
                    bm.insert_page(page)
                    index.insert(key, page.page_id)
                st.success(f"Inserted {len(records)} JSON record(s) into HyperDB")
            except Exception as e:
                st.error(f"Invalid JSON: {e}")

        st.subheader("Role Aggregation")
        if st.button("Count Roles", key="count_roles"):
            scanned = qe.scan(list(index.index.values()))
            role_counts = qe.aggregate_by_field(scanned, "role")
            st.write(role_counts) 
            # st.bar_chart(role_counts) 
    
    
        if st.button("Count Engineers", key="count_engineers"):
            scanned = qe.scan(list(index.index.values()))
            role_counts = qe.aggregate_by_field(scanned, "role")
            st.write(f"Engineers: {role_counts.get('engineer', 0)}")

# with tab4:
#     st.subheader("Buffer State")
#     st.write(list(bm.buffer.keys()))

with tab4:
    st.subheader("📦 Buffer State Overview")

    if bm.buffer:
        for page_id, page in bm.buffer.items():
            st.markdown(f"### Page {page_id}")
            st.write(f"🔹 Total Records: {len(page.records)}")
            st.write(f"🔹 Deleted Offsets: {page.deleted_offsets}")
            #st.write(f"🔹 Pinned: {page.pinned}")
            st.write("🔹 Records:")
            try:
                decoded = [r.decode("utf-8") for r in page.records if r]
                st.write(decoded)
            except Exception:
                st.warning("Some records could not be decoded.")
    else:
        st.info("Buffer is currently empty.")


with tab5:
    st.subheader("System Metrics")
    try:
        response = requests.get("http://localhost:8000/metrics")
        metrics_text = response.text

        def extract_metric(name):
            for line in metrics_text.splitlines():
                if line.startswith(name + " "):
                    return float(line.split(" ")[1])
            return None

        api_requests = extract_metric("api_requests_total")
        buffer_evictions = extract_metric("buffer_evictions_total")
        page_loads = extract_metric("page_load_time_seconds_count")

        st.metric("API Requests", api_requests)
        st.metric("Buffer Evictions", buffer_evictions)
        st.metric("Page Loads", page_loads)

    except Exception as e:
        st.error(f"Could not fetch metrics: {e}")
def main():
    import streamlit.web.cli as stcli
    import sys
    sys.argv = ["streamlit", "run", "dashboard.py"]
    sys.exit(stcli.main())
