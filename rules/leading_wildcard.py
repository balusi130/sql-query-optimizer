import re

def check_leading_wildcard(query: str) -> list:
    suggestions = []
    if re.search(r"LIKE\s+[\"']\%", query, re.IGNORECASE):
        suggestions.append({
            "type": "INDEX",
            "message": "Leading wildcard in LIKE '%value' cannot use a B-tree index. "
                       "Consider a full-text search index (pg_trgm in Postgres or FULLTEXT in MySQL) for this pattern."
        })
    return suggestions
