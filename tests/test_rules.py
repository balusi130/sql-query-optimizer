import pytest
from rules.select_star import check_select_star
from rules.missing_index import check_missing_index
from rules.function_on_column import check_function_on_column
from rules.leading_wildcard import check_leading_wildcard
from rules.correlated_subquery import check_correlated_subquery


def test_select_star_detected():
    assert len(check_select_star("SELECT * FROM users")) > 0


def test_select_star_not_flagged_on_specific_columns():
    assert len(check_select_star("SELECT id, name FROM users")) == 0


def test_year_function_flagged():
    issues = check_function_on_column("SELECT * FROM orders WHERE YEAR(created_at) = 2024")
    assert any("YEAR" in i["message"] for i in issues)


def test_leading_wildcard_flagged():
    issues = check_leading_wildcard("SELECT * FROM users WHERE name LIKE '%paul'")
    assert len(issues) > 0


def test_clean_like_not_flagged():
    issues = check_leading_wildcard("SELECT * FROM users WHERE name LIKE 'paul%'")
    assert len(issues) == 0


def test_correlated_subquery_flagged():
    query = "SELECT * FROM orders WHERE id IN (SELECT order_id FROM items WHERE price > 100)"
    issues = check_correlated_subquery(query)
    assert len(issues) > 0


def test_missing_index_on_where_column():
    issues = check_missing_index("SELECT * FROM orders WHERE status = 'pending'")
    assert any("status" in i["message"] for i in issues)
