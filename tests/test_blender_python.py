import json
import subprocess
import sys

import pytest

from blender_python import relaunch_under_blender_python, _RELAUNCH_GUARD_ENV_VAR


@pytest.fixture(autouse=True)
def clean_relaunch_guard(monkeypatch):
    monkeypatch.delenv(_RELAUNCH_GUARD_ENV_VAR, raising=False)


def test_raises_when_settings_file_missing(monkeypatch, tmp_path):
    fake_module_path = tmp_path / "blender_python.py"
    fake_module_path.write_text("")
    monkeypatch.setattr("blender_python.__file__", str(fake_module_path))

    with pytest.raises(RuntimeError, match="Could not find"):
        relaunch_under_blender_python()


def test_raises_when_python_executable_missing_from_settings(monkeypatch, tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(json.dumps({}))
    fake_module_path = tmp_path / "blender_python.py"
    fake_module_path.write_text("")
    monkeypatch.setattr("blender_python.__file__", str(fake_module_path))

    with pytest.raises(RuntimeError, match="no 'python_executable' entry"):
        relaunch_under_blender_python()


def test_raises_when_python_executable_does_not_exist_on_disk(monkeypatch, tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(json.dumps({"python_executable": str(tmp_path / "nope.exe")}))
    fake_module_path = tmp_path / "blender_python.py"
    fake_module_path.write_text("")
    monkeypatch.setattr("blender_python.__file__", str(fake_module_path))

    with pytest.raises(RuntimeError, match="does not exist"):
        relaunch_under_blender_python()


def test_relaunch_guard_prevents_infinite_loop(monkeypatch):
    monkeypatch.setenv(_RELAUNCH_GUARD_ENV_VAR, "1")

    with pytest.raises(RuntimeError, match="still failed"):
        relaunch_under_blender_python()


def test_successful_relaunch_invokes_configured_interpreter(monkeypatch, tmp_path):
    python_executable = tmp_path / "python.exe"
    python_executable.write_text("")
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(json.dumps({"python_executable": str(python_executable)}))
    fake_module_path = tmp_path / "blender_python.py"
    fake_module_path.write_text("")
    monkeypatch.setattr("blender_python.__file__", str(fake_module_path))

    monkeypatch.setattr(sys, "argv", ["some_script.py", "--input", "a.stl"])

    calls = {}

    def fake_run(args, env=None):
        calls["args"] = args
        calls["env"] = env

        class Result:
            returncode = 7

        return Result()

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        relaunch_under_blender_python()

    assert exc_info.value.code == 7
    assert calls["args"] == [str(python_executable), "some_script.py", "--input", "a.stl"]
    assert calls["env"][_RELAUNCH_GUARD_ENV_VAR] == "1"
