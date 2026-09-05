"""Mesh-fix pipeline: STL -> PLY -> voxel remesh -> STL.

Usage:
    python mesh_fix.py --input path/to/mesh.stl --output path/to/fixed.stl --voxel-size 0.01 [--overwrite]
"""

import argparse
import os
import tempfile

# stl_to_ply's own import guard relaunches this whole script under Blender's
# Python if needed (see blender_python.py), so no separate guard is needed here.
from stl_to_ply import convert as stl_to_ply
from voxel_fix import convert as voxel_fix
from ply_to_stl import convert as ply_to_stl


def run_pipeline(input_path, output_path, voxel_size, overwrite=False):
    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(
            f"Output file '{output_path}' already exists. Pass overwrite=True to replace it."
        )

    with tempfile.TemporaryDirectory() as tmp_dir:
        raw_ply = os.path.join(tmp_dir, "raw.ply")
        fixed_ply = os.path.join(tmp_dir, "fixed.ply")

        stl_to_ply(input_path, raw_ply)
        voxel_fix(raw_ply, fixed_ply, voxel_size)
        ply_to_stl(fixed_ply, output_path, overwrite=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the source STL file.")
    parser.add_argument("--output", required=True, help="Path to write the repaired STL file.")
    parser.add_argument("--voxel-size", required=True, type=float, help="Voxel size for Blender's voxel remesh.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting the output file if it already exists.",
    )
    args = parser.parse_args()

    run_pipeline(args.input, args.output, args.voxel_size, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
