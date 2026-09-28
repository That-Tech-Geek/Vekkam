from app.core.models import SceneAction

def build_timeline(actions: list[SceneAction], word_timestamps: list[dict[str,float]]) -> list[dict[str,object]]:
    return [{"start":a.start,"end":a.end,"action":a.action,
             "words":[w for w in word_timestamps if a.start<=w["start"]<=a.end]} for a in actions]
