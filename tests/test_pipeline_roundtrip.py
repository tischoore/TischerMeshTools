import trimesh

from stl_to_ply import convert as stl_to_ply
from ply_to_stl import convert as ply_to_stl


def test_stl_to_ply_to_stl_preserves_geometry(tmp_path, sample_stl, sample_mesh):
    ply_path = tmp_path / "intermediate.ply"
    final_stl_path = tmp_path / "final.stl"

    stl_to_ply(str(sample_stl), str(ply_path))
    ply_to_stl(str(ply_path), str(final_stl_path))

    result = trimesh.load(final_stl_path, file_type="stl")
    assert len(result.vertices) == len(sample_mesh.vertices)
    assert len(result.faces) == len(sample_mesh.faces)
