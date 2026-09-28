from app.cli import main


def test_architecture_command(capsys):
    assert main(["architecture"]) == 0
    assert "canonical_learning_ir" in capsys.readouterr().out


def test_ingest_text_command(capsys):
    assert main(["ingest-text", "--document-id", "demo", "--text", "Supply and demand"]) == 0
    output = capsys.readouterr().out
    assert '"document_id": "demo"' in output
