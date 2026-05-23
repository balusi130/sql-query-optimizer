import re

def check_function_on_column(query: str) -> list:
    suggestions = []
    patterns = [
        (r"YEAR\s*\((\w+)\)", "YEAR({col}) in WHERE prevents index use. Rewrite as a date range: {col} >= 'YYYY-01-01' AND {col} < 'YYYY+1-01-01'"),
        (r"LOWER\s*\((\w+)\)", "LOWER({col}) in WHERE prevents index use. Consider a case-insensitive index (CITEXT in Postgres) or store data normalised."),
        (r"DATE\s*\((\w+)\)", "DATE({col}) in WHERE prevents index use. Use a range condition on the raw timestamp column instead."),
    ]
    for pattern, message in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            col = match.group(1)
            suggestions.append({
                "type": "REWRITE",
                "message": message.format(col=col)
            })
    return suggestions
