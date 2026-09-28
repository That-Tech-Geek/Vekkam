from app.cli import main


def test_architecture_command(capsys):
    assert main(["architecture"]) == 0
    assert "canonical_learning_ir" in capsys.readouterr().out


def test_ingest_text_command(capsys):
    assert main(["ingest-text", "--document-id", "demo", "--text", "Supply and demand"]) == 0
    output = capsys.readouterr().out
    assert '"document_id": "demo"' in output


def test_llm_connect_ollama(capsys, monkeypatch, tmp_path):
    import app.llm.client as client

    monkeypatch.setattr(client, "_CONFIG_DIR", tmp_path)
    monkeypatch.setattr(client, "_CONFIG_FILE", tmp_path / "llm.json")
    assert main(["llm", "connect-ollama", "--model", "llama3.2:3b"]) == 0
    output = capsys.readouterr().out
    assert '"provider": "ollama"' in output
    assert '"model": "llama3.2:3b"' in output
    assert main(["llm", "status"]) == 0
    assert '"connected": true' in capsys.readouterr().out
