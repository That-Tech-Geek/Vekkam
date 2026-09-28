from app.core.ids import stable_id

def test_stable_ids_are_deterministic():
    assert stable_id("concept","doc","equilibrium")==stable_id("concept","doc","equilibrium")
    assert stable_id("concept","doc","equilibrium")!=stable_id("concept","doc","elasticity")
