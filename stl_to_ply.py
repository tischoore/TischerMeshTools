"""Load an STL mesh and serialize it as binary PLY.

Usage:
    python stl_to_ply.py --input path/to/mesh.stl --output path/to/mesh.ply
"""

import argparse

try:
    import trimesh
except ImportError:
    from blender_python import relaunch_under_blender_python

    relaunch_under_blender_python()


def convert(input_path, output_path):
    mesh = trimesh.load(input_path, file_type="stl")
    mesh.export(output_path, file_type="ply", encoding="binary")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the source STL file.")
    parser.add_argument("--output", required=True, help="Path to write the binary PLY file.")
    args = parser.parse_args()

    convert(args.input, args.output)


if __name__ == "__main__":
    main()
