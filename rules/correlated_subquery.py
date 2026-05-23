import re


def check_correlated_subquery(query: str) -> list:
    """
    Flags SELECT subqueries in WHERE clauses that reference the outer table.
    These are often rewritable as JOINs for better performance.
    """
    suggestions = []
    pattern = re.compile(r"WHERE\s+\w+\s+IN\s*\(\s*SELECT", re.IGNORECASE)
    if pattern.search(query):
        suggestions.append({
            "type": "REWRITE",
            "message": (
                "IN (SELECT ...) subquery detected. If this references the outer table, "
                "rewriting as a JOIN usually performs significantly better on large datasets."
            )
        })
    return suggestions
