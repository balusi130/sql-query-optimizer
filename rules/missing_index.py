import re

def check_missing_index(query: str) -> list:
    suggestions = []
    where_cols = re.findall(r"WHERE\s+(\w+)\s*=", query, re.IGNORECASE)
    join_cols = re.findall(r"JOIN\s+\w+\s+ON\s+\w+\.(\w+)\s*=", query, re.IGNORECASE)
    order_cols = re.findall(r"ORDER BY\s+(\w+)", query, re.IGNORECASE)

    for col in set(where_cols + join_cols + order_cols):
        suggestions.append({
            "type": "INDEX",
            "message": f"Column '{col}' appears in WHERE/JOIN/ORDER BY — ensure it has an index. "
                       f"Run EXPLAIN to confirm index usage."
        })
    return suggestions
