from datetime import datetime, timedelta
from app.core.models import MasteryState

def schedule_review(state: MasteryState, recalled: bool) -> MasteryState:
    now=datetime.utcnow(); state.last_review=now
    if recalled:
        state.stability=max(1.0,state.stability*1.35+1.0)
        state.retrievability=min(1.0,state.retrievability+0.2)
    else:
        state.stability=max(0.2,state.stability*0.55)
        state.retrievability=max(0.0,state.retrievability-0.3)
    state.next_review=now+timedelta(days=max(1,round(state.stability)))
    state.review_history.append({"at":now.isoformat(),"recalled":recalled})
    return state
