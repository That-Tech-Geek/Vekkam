from app.visual.equation import parse_equation
from app.visual.graph import interpret_graph
from app.visual.table import parse_table

def test_equation_ir():
    eq=parse_equation(r"\frac{d}{dx}x^2 = 2x","derivative","differentiation")
    assert eq.operation=="differentiation" and "x" in eq.variables

def test_graph_ir():
    graph=interpret_graph("fig_1","Quantity","Price",[("D","curve","negative"),("S","curve","positive")])
    assert graph.reconstructability.value=="RECONSTRUCTABLE" and len(graph.objects)==2

def test_table_ir():
    assert parse_table(["Year","GDP"],[[2024,100]]).rows[0][1]==100
