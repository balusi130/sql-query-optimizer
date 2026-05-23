# sql-query-optimizer

A CLI tool that takes a SQL query, parses it, and gives you concrete suggestions for making it faster — missing indexes, anti-patterns like `SELECT *`, unnecessary subqueries, and places where a join would work better than a nested query.

This came out of audit work I was doing on fintech database code. A lot of the performance issues I kept seeing were the same five or six problems showing up repeatedly, so I wrote tooling to catch them automatically before they hit production.

---

## What it catches

- Missing indexes on columns used in `WHERE`, `JOIN ON`, and `ORDER BY` clauses
- `SELECT *` usage — flags it and suggests explicit column lists
- Implicit cartesian joins (missing `ON` clause)
- Correlated subqueries that could be rewritten as JOINs
- `LIKE` patterns with a leading wildcard (`LIKE '%value'`) that cannot use an index
- Functions wrapped around indexed columns in WHERE clauses (e.g. `WHERE YEAR(created_at) = 2024`)
- Large `OFFSET` pagination — suggests keyset pagination instead

---

## Stack

- Python 3.10+
- `sqlglot` for SQL parsing
- `rich` for terminal output formatting
- Optional: connects to a live PostgreSQL or MySQL instance to pull `EXPLAIN` output

---

## Installation

```bash
git clone https://github.com/balusi130/sql-query-optimizer.git
cd sql-query-optimizer
pip install -r requirements.txt
```

---

## Usage

Analyze a query directly:

```bash
python optimizer.py --query "SELECT * FROM orders WHERE YEAR(created_at) = 2024"
```

Analyze a `.sql` file:

```bash
python optimizer.py --file queries/report.sql
```

Connect to a live database for EXPLAIN analysis:

```bash
python optimizer.py --file queries/report.sql --db postgresql://user:pass@localhost/mydb
```

Sample output:

```
Analyzing query...

[WARNING]  SELECT * detected — specify only the columns you need
[INDEX]    Column 'created_at' used in WHERE but may lack a functional index
[REWRITE]  YEAR(created_at) = 2024 prevents index use — rewrite as:
           created_at >= '2024-01-01' AND created_at < '2025-01-01'

2 suggestions. Estimated improvement: significant on large tables.
```

---

## Project structure

```
sql-query-optimizer/
├── optimizer.py          # CLI entry point
├── rules/
│   ├── select_star.py
│   ├── missing_index.py
│   ├── function_on_column.py
│   ├── correlated_subquery.py
│   └── leading_wildcard.py
├── db/
│   └── connector.py      # Optional live DB connection + EXPLAIN runner
├── tests/
│   └── test_rules.py
├── requirements.txt
└── README.md
```

---

## Tests

```bash
pytest tests/ -v
```

---

## Planned additions

- Support for `EXPLAIN ANALYZE` output parsing (PostgreSQL)
- JSON output mode for CI pipeline integration
- Query rewrite suggestions (not just identification)

---

MIT License