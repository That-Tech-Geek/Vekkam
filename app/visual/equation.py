import re
from app.core.models import EquationIR

def parse_equation(latex: str, equation_type: str="unknown", operation: str|None=None) -> EquationIR:
    variables=sorted(set(re.findall(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])", latex)))
    return EquationIR(latex=latex, type=equation_type, variables=variables, operation=operation)
