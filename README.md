# ExamForge

Vekkam is now a **CLI-first** multimodal exam-preparation engine built around a canonical Learning IR.

There is no frontend or web server in the runtime path. The CLI is the user-facing product surface; the domain engine remains importable as a Python package.

## Pipeline

```
SOURCE MATERIAL -> MULTIMODAL EXTRACTION -> CANONICAL LEARNING IR
-> KNOWLEDGE GRAPH + VECTOR RETRIEVAL -> VISUAL BLUEPRINT
-> MANIM COMPILER + VALIDATION -> NARRATION + SYNC -> VIDEO
-> ACTIVE RECALL + FSRS -> EXAM INTELLIGENCE
```

## CLI

Install locally:

```bash
python -m pip install -e ".[dev]"
```

Then:

```bash
examforge architecture
examforge llm connect-ollama --model llama3.2:3b
examforge llm chat "Explain opportunity cost"
examforge llm connect-api --model gpt-4.1
examforge ingest-text --file notes.txt
examforge blueprint --file notes.txt
examforge questions --file notes.txt --count 4
type notes.txt | examforge ingest-text --document-id economics
```

Every command emits JSON so the CLI can be composed with shell scripts, CI, other tools, or future TUI clients.

### Commands

- `ingest-text`: text -> canonical Learning IR
- `blueprint`: text/IR-derived concept -> visual teaching blueprint
- `questions`: concept -> active-recall question set
- `review`: mastery state -> next review state
- `architecture`: inspect the engine pipeline
- `llm connect-api`: link an OpenAI-compatible API using an environment variable for the key
- `llm connect-ollama`: link a local Ollama server and installed model
- `llm status`: inspect the active provider without exposing secrets
- `llm chat`: send a prompt through the active provider

## Repository layout

- `app/core/`: canonical domain models and stable IDs
- `app/ingestion/`: document/OCR/image extraction
- `app/visual/`: graph, table and equation understanding
- `app/knowledge/`: graph and vector-store ports
- `app/blueprints/`: declarative teaching blueprints
- `app/manim/`: scene compilation and validation
- `app/audio/`: narration and synchronization
- `app/assessment/`: recall, rescue and mastery
- `app/cli.py`: product-facing CLI
- `tests/`: contracts
- `docs/`: architecture and roadmap

LLM integrations remain isolated behind `app/llm/`; provider configuration is stored locally without storing API keys. API keys are read from environment variables at request time.

Optional integrations remain isolated behind adapters: PyMuPDF/OCR/OpenCV, Neo4j, Qdrant, Manim, Kokoro/Piper and WhisperX.
