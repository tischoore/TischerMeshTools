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
5. This repo's scripts and tests currently require `trimesh` (and its dependency `numpy`) and `pytest`:
   ```
   "C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe" -m pip install trimesh pytest
   ```

## Scripts

| Script | Purpose |
| --- | --- |
| `stl_to_ply.py` | Loads an STL mesh and serializes it as binary PLY. Run with `--input <path.stl> --output <path.ply>`. |
| `ply_to_stl.py` | Loads a PLY mesh and serializes it as STL. Run with `--input <path.ply> --output <path.stl>`, and pass `--overwrite` to allow replacing an existing output file (otherwise it refuses to overwrite). |

## Tests

Tests live in `tests/` and run with pytest, using the Blender-bundled interpreter:
```
"C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe" -m pytest tests/
```
