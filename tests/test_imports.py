import json

from litmap import __version__, describe_pipeline, load_config


def test_package_imports(tmp_path):
    assert __version__
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "project": {"name": "test-run", "run_dir": "./runs"},
                "source": {"type": "csv", "params": {"path": "./data/papers.csv"}},
            }
        ),
        encoding="utf-8",
    )
    config = load_config(config_path)
    steps = describe_pipeline(config)
    assert steps
    assert steps[0].name == "ingest"
