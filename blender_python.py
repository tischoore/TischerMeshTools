"""Shared helper: relaunch the running script under Blender's bundled Python.

Scripts in this repo depend on packages (`bpy`, `trimesh`) that are only
installed into the Python distribution bundled with Blender, whose path is
configured in `settings.json` as `python_executable`. If a script is
invoked with a different Python, it can call `relaunch_under_blender_python()`
to re-exec itself under the configured interpreter instead of failing with a
raw ModuleNotFoundError.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

_RELAUNCH_GUARD_ENV_VAR = "_TISCHERMESH_RELAUNCHED"


def relaunch_under_blender_python():
    if os.environ.get(_RELAUNCH_GUARD_ENV_VAR):
        raise RuntimeError(
            "Relaunched under settings.json's python_executable, but the required "
            "import still failed. That interpreter is missing a dependency this "
            "script needs. See README.md's 'Installation of dependencies' section "
            "for the pip install command to run against your Blender Python."
        )

    settings_path = Path(__file__).resolve().parent / "settings.json"
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except FileNotFoundError:
        raise RuntimeError(
            f"Could not find {settings_path}. See README.md for how to create it "
            "and set 'python_executable' to Blender's bundled Python."
        )

    python_executable = settings.get("python_executable")
    if not python_executable:
        raise RuntimeError(
            f"'{settings_path}' has no 'python_executable' entry. See README.md's "
            "'Installation of dependencies' section for how to set it."
        )
    if not os.path.isfile(python_executable):
        raise RuntimeError(
            f"settings.json's python_executable ('{python_executable}') does not "
            "exist. See README.md's 'Installation of dependencies' section for how "
            "to locate Blender's bundled Python."
        )

    env = dict(os.environ)
    env[_RELAUNCH_GUARD_ENV_VAR] = "1"
    result = subprocess.run([python_executable, sys.argv[0], *sys.argv[1:]], env=env)
    sys.exit(result.returncode)
