"""PRC version consistency: VERSION and POLICY_VERSION files match config."""

from pathlib import Path

from app import config

ROOT = Path(__file__).resolve().parents[1]


def test_version_files_match_config() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == config.SERVICE_VERSION
    assert (ROOT / "POLICY_VERSION").read_text(encoding="utf-8").strip() == config.POLICY_VERSION
    assert config.SERVICE_VERSION == "1.1.0"
