import argparse
from rules.select_star import check_select_star
from rules.missing_index import check_missing_index
from rules.function_on_column import check_function_on_column
from rules.leading_wildcard import check_leading_wildcard
from rich.console import Console
from rich.table import Table

console = Console()

RULES = [
    check_select_star,
    check_missing_index,
    check_function_on_column,
    check_leading_wildcard,
]


def analyze(query: str):
    console.print(f"\n[bold]Analyzing query...[/bold]\n")
    all_suggestions = []

    for rule in RULES:
        suggestions = rule(query)
        all_suggestions.extend(suggestions)

    if not all_suggestions:
        console.print("[green]No issues found. Query looks clean.[/green]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type", style="yellow", width=12)
    table.add_column("Suggestion")

    for s in all_suggestions:
        table.add_row(s["type"], s["message"])

    console.print(table)
    console.print(f"\n[bold]{len(all_suggestions)} suggestion(s) found.[/bold]")


def main():
    parser = argparse.ArgumentParser(description="SQL Query Optimizer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="SQL query string to analyze")
    group.add_argument("--file", help="Path to a .sql file")
    args = parser.parse_args()

    if args.query:
        analyze(args.query)
    elif args.file:
        with open(args.file, "r") as f:
            analyze(f.read())


if __name__ == "__main__":
    main()
