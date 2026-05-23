def check_select_star(query: str) -> list:
    suggestions = []
    if "SELECT *" in query.upper():
        suggestions.append({
            "type": "WARNING",
            "message": "SELECT * detected — specify only the columns you need to reduce data transfer and improve index usage."
        })
    return suggestions
