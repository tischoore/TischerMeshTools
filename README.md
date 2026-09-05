# TischerMeshTools

A collection of standalone Python scripts for manipulating 3D meshes. Each script performs a single, specific function and can be run independently.

## Installation of dependencies

These scripts rely on the Python distribution bundled with Blender (for the `bpy` module and related mesh-processing libraries), rather than a standalone system Python install.

1. Install [Blender](https://www.blender.org/download/).
2. Locate Blender's bundled Python executable, e.g. on Windows:
   ```
   C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe
   ```
3. Set that path (and the corresponding dependencies path) in [`settings.json`](settings.json):
   ```json
   {
     "python_executable": "C:\\Program Files\\Blender Foundation\\Blender 5.1\\5.1\\python\\bin\\python.exe",
     "dependencies_path": "C:\\Program Files\\Blender Foundation\\Blender 5.1\\5.1\\python\\lib\\site-packages"
   }
   ```
4. Install any additional required packages using that Python executable, e.g.:
   ```
   "C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe" -m pip install <package>
   ```
5. This repo's scripts and tests currently require `trimesh` (and its dependency `numpy`), `pytest`, and the standalone `bpy` package matching your installed Blender version:
   ```
   "C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe" -m pip install trimesh pytest bpy==5.1.2
   ```

Once `settings.json` is set up, you don't need to invoke that interpreter by hand: each script (via the shared `blender_python.py` helper) detects when it's been started with a different Python, and automatically relaunches itself under the `python_executable` from `settings.json`. So `python mesh_fix.py --input ...` works from any Python on your PATH, as long as `settings.json` points at a working Blender Python with the dependencies above installed.

## Scripts

| Script | Purpose |
| --- | --- |
| `stl_to_ply.py` | Loads an STL mesh and serializes it as binary PLY. Run with `--input <path.stl> --output <path.ply>`. |
| `ply_to_stl.py` | Loads a PLY mesh and serializes it as STL. Run with `--input <path.ply> --output <path.stl>`, and pass `--overwrite` to allow replacing an existing output file (otherwise it refuses to overwrite). |
| `voxel_fix.py` | Loads a binary PLY mesh and repairs it using Blender's voxel remesh. Run with `--input <path.ply> --output <path.ply> --voxel-size <size>`. |
| `mesh_fix.py` | Pipeline that converts an STL to PLY, repairs it with `voxel_fix.py`, then converts the result back to STL. Run with `--input <path.stl> --output <path.stl> --voxel-size <size>`, and pass `--overwrite` to allow replacing an existing output file (otherwise it refuses to overwrite). |
| `fix_folder.py` | Runs the `mesh_fix.py` repair pipeline over every `.stl` file in a directory. Run with `--input <dir> --voxel-size <size>`, optionally `--output <dir>` (defaults to writing `<name>_mesh_fix.stl` next to each input), `--recursive` to include subfolders, and `--overwrite` to allow replacing existing outputs. Per-file failures are logged and skipped rather than stopping the batch; the script exits non-zero if any file failed. |

## Tests

Tests live in `tests/` and run with pytest, using the Blender-bundled interpreter:
```
"C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe" -m pytest tests/
```
