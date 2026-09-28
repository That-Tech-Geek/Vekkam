from app.core.models import TableIR

def parse_table(columns: list[str], rows: list[list[object]]) -> TableIR:
    if any(len(row)!=len(columns) for row in rows):
        raise ValueError("Every table row must match the column count.")
    return TableIR(columns=columns, rows=rows)
