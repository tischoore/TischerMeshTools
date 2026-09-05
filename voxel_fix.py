"""Load a binary PLY mesh and repair it using Blender's voxel remesh.

Usage:
    python voxel_fix.py --input path/to/mesh.ply --output path/to/mesh.ply --voxel-size 0.01
"""

import argparse

try:
    import bpy
except ImportError:
    from blender_python import relaunch_under_blender_python

    relaunch_under_blender_python()


def convert(input_path, output_path, voxel_size):
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.wm.ply_import(filepath=input_path)

    obj = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj
    obj.data.remesh_voxel_size = voxel_size
    bpy.ops.object.voxel_remesh()

    bpy.ops.wm.ply_export(filepath=output_path, ascii_format=False, export_selected_objects=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the source PLY file.")
    parser.add_argument("--output", required=True, help="Path to write the repaired binary PLY file.")
    parser.add_argument("--voxel-size", required=True, type=float, help="Voxel size for Blender's voxel remesh.")
    args = parser.parse_args()

    convert(args.input, args.output, args.voxel_size)


if __name__ == "__main__":
    main()
