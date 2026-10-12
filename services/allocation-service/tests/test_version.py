"""Allocation version consistency."""

from pathlib import Path

from app import config

ROOT = Path(__file__).resolve().parents[1]


def test_version_file_matches_config() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == config.SERVICE_VERSION
    assert config.SERVICE_VERSION == "1.0.0"
