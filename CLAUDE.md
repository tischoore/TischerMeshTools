# CLAUDE.md

This repository is a collection of standalone Python scripts for manipulating 3D meshes.

## Structure

- Each script in this repo performs a single, well-defined function (e.g. one script decimates a mesh, another exports to a format, etc.). Scripts are not combined into a shared library or CLI — they are meant to be run independently.
- Every script must be documented in [README.md](README.md), including what it does and how to run it.
- `settings.json` holds global configuration for this repo (dependency paths, Python executable, etc.) that scripts may rely on instead of hardcoding paths.

## Python environment

Scripts run using the Python distribution bundled with Blender, not a system Python. The path to that interpreter is defined in `settings.json` under `python_executable`. Use that interpreter when running or testing scripts, since mesh-manipulation code may depend on Blender's `bpy` module.

## Conventions for new scripts

- One script = one function/purpose. Do not merge multiple mesh operations into a single script.
- Add a corresponding entry to the "Scripts" section of README.md when adding a new script.
- Read paths and settings from `settings.json` rather than hardcoding machine-specific paths.
