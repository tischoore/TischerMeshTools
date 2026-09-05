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

## Data handoff between pipeline steps

Some workflows (e.g. auto-repairing a complex mesh) run as a sequence of steps across different tools/interpreters — Blender's `bpy`, FreeCAD's `freecadcmd`, and other Python mesh libraries. Each of these runs as its own OS process with its own native mesh representation, so a live mesh object cannot be shared in memory across steps that use different tools — every cross-tool step boundary requires writing the mesh to disk and re-reading it in the next step.

- Use binary PLY as the standard interchange format between pipeline steps, rather than re-exporting to STL at every step. PLY is supported by Blender, FreeCAD's Mesh module, and common Python mesh libraries, and preserves vertex normals/attributes that STL discards.
- Reserve STL for the pipeline's true starting input and final output.
- Do not merge distinct pipeline steps into one script just to keep a mesh in memory — that breaks the one-script-one-function convention above and the tool-boundary constraint makes the saving illusory for most pipelines anyway.

## Testing

- Every script has a corresponding `tests/test_<script_name>.py` that verifies it in isolation.
- Scripts meant to be chained together (e.g. pipeline steps that hand off files to one another) must also have a combination/integration test verifying the full chain, not just each script individually.
- Tests run with pytest using the Blender-bundled interpreter: `"<python_executable>" -m pytest tests/`.
