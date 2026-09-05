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

## Scripts

No scripts have been added yet. As scripts are added to this repository, list each one here with its name, a one-line description of its single purpose, and how to run it, for example:

| Script | Purpose |
| --- | --- |
| `script_name.py` | One-sentence description of the single thing this script does. |
