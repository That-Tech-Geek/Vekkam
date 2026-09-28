# Canonical Learning IR

Every artifact receives a stable ID and provenance.

```
document_id
page_id
visual_id
concept_id
blueprint_id
scene_id
question_id
video_id
```

Concept lineage is preserved as:

```
concept -> source page -> source region -> extracted artifact -> interpretation -> generated artifacts
```

Graph IR stores axes, curves/objects, intersections, annotations, semantic interpretation, reconstructability and confidence. Equations store both LaTeX and semantic metadata. Tables store normalized columns and rows.

Downstream systems must consume these IR objects instead of re-reading source material independently.
