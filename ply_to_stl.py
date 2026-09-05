"""Load a PLY mesh and serialize it as STL.

Usage:
    python ply_to_stl.py --input path/to/mesh.ply --output path/to/mesh.stl [--overwrite]
"""

import argparse
import os

try:
    import trimesh
except ImportError:
    from blender_python import relaunch_under_blender_python

    relaunch_under_blender_python()


def convert(input_path, output_path, overwrite=False):
    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(
            f"Output file '{output_path}' already exists. Pass overwrite=True to replace it."
        )

    mesh = trimesh.load(input_path, file_type="ply")
    mesh.export(output_path, file_type="stl")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the source PLY file.")
    parser.add_argument("--output", required=True, help="Path to write the STL file.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting the output file if it already exists.",
    )
    args = parser.parse_args()

    convert(args.input, args.output, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
