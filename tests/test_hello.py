"""Test the reusable greeting and its command-line consumers."""

import runpy
import sys
from pathlib import Path

import pytest
import yanex

from empty_project._cli import main
from empty_project.hello import hello_world


def test_hello_world(capsys):
    assert hello_world("Student") == "Hello, Student"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [([], "Hello, World\n"), (["--name", "Student"], "Hello, Student\n")],
)
def test_cli_prints_greeting(monkeypatch, capsys, arguments, expected):
    monkeypatch.setattr(sys, "argv", ["empty-cli", *arguments])

    main()

    assert capsys.readouterr().out == expected


def test_experiment_prints_greeting_and_logs_metric(monkeypatch, capsys):
    metrics = []
    monkeypatch.setattr(yanex, "get_param", lambda name, default: "Student")
    monkeypatch.setattr(yanex, "log_metrics", metrics.append)
    script = Path(__file__).resolve().parents[1] / "experiments/greet.py"

    runpy.run_path(str(script), run_name="__main__")

    assert capsys.readouterr().out == "Hello, Student\n"
    assert metrics == [{"greeting_length": 14}]
