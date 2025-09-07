from collections import Counter
import json

class QueryEngine:
    def __init__(self, buffer_manager):
        self.buffer_manager = buffer_manager

    def scan(self, page_ids):
        results = []
        for pid in page_ids:
            page = self.buffer_manager.get_page(pid)
            results.extend(page.get_records())
        return results

    def filter(self, records, keyword):
        return [r for r in records if keyword in r]

    def project(self, records, fields=None):
        # For now, just return raw records (can parse fields later)
        return records

    def aggregate(self, records, agg_func):
        values = [record.split(": ")[1] for record in records if ": " in record]
        return agg_func(values)

    def join(self, left_records, right_records, key_func):
        joined = []
        left_map = {key_func(r): r for r in left_records}
        for r in right_records:
            k = key_func(r)
            if k in left_map:
                joined.append(f"{left_map[k]} | {r}")
        return joined

    def filter(self, records, keyword):
        filtered = []
        for r in records:
            try:
                json_str = r.split(": ", 1)[1]
                data = json.loads(json_str)
                if any(keyword.lower() in str(v).lower() for v in data.values()):
                    filtered.append(r)
            except:
                if keyword.lower() in r.lower():
                    filtered.append(r)
        return filtered

    def aggregate_by_field(self, records, field_name):
        values = []
        for r in records:
            try:
                json_str = r.split(": ", 1)[1]
                data = json.loads(json_str)
                if field_name in data:
                    values.append(data[field_name])
            except:
                continue
        return Counter(values)




