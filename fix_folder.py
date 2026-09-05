"""Batch mesh-fix: run mesh_fix.py's repair pipeline over every STL in a directory.

Usage:
    python fix_folder.py --input path/to/dir --voxel-size 0.01
        [--output path/to/out_dir] [--overwrite] [--recursive]
"""

import argparse
import os
from pathlib import Path

# mesh_fix imports stl_to_ply etc., which already carry the Blender-relaunch
# import guard (see blender_python.py), so no separate guard is needed here.
from mesh_fix import run_pipeline


_OUTPUT_SUFFIX = "_mesh_fix"


def _default_output_path(input_path):
    return input_path.with_name(f"{input_path.stem}{_OUTPUT_SUFFIX}{input_path.suffix}")


def run_folder(input_dir, voxel_size, output_dir=None, overwrite=False, recursive=False):
    input_dir = Path(input_dir)
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory '{input_dir}' does not exist.")

    glob = input_dir.rglob if recursive else input_dir.glob
    stl_files = sorted(p for p in glob("*.stl") if p.suffix.lower() == ".stl" and p.is_file())

    if output_dir is None:
        # Without a separate output directory, outputs land back in the
        # scanned folder as "<name>_mesh_fix.stl" — exclude prior outputs so
        # re-running this script doesn't re-fix its own results.
        stl_files = [p for p in stl_files if not p.stem.endswith(_OUTPUT_SUFFIX)]

    results = []
    for input_path in stl_files:
        if output_dir is not None:
            output_path = Path(output_dir) / input_path.relative_to(input_dir)
        else:
            output_path = _default_output_path(input_path)

        error = None
        try:
            os.makedirs(output_path.parent, exist_ok=True)
            run_pipeline(str(input_path), str(output_path), voxel_size, overwrite=overwrite)
        except Exception as exc:
            error = exc

        results.append({"input": input_path, "output": output_path, "error": error})

    return results


def _print_summary(results):
    failures = [r for r in results if r["error"] is not None]
    print(f"Processed {len(results)} file(s): {len(results) - len(failures)} succeeded, {len(failures)} failed.")
    for r in failures:
        print(f"  FAILED: {r['input']} -> {r['output']}: {r['error']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Directory containing STL files to fix.")
    parser.add_argument("--voxel-size", required=True, type=float, help="Voxel size for Blender's voxel remesh.")
    parser.add_argument(
        "--output",
        help="Directory to write repaired STL files into, mirroring the input's subfolder structure. "
        "If omitted, each output is written next to its input as '<name>_mesh_fix.stl'.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting output files that already exist.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Also process STL files in subdirectories of --input.",
    )
    args = parser.parse_args()

    results = run_folder(
        args.input,
        args.voxel_size,
        output_dir=args.output,
        overwrite=args.overwrite,
        recursive=args.recursive,
    )
    _print_summary(results)

    if any(r["error"] is not None for r in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
