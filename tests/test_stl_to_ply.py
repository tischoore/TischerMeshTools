import trimesh

from stl_to_ply import convert


def test_convert_produces_binary_ply_with_matching_geometry(tmp_path, sample_stl, sample_mesh):
    output_path = tmp_path / "sample.ply"

    convert(str(sample_stl), str(output_path))

    assert output_path.exists()
    with open(output_path, "rb") as f:
        header = f.read(40)
    assert b"format binary" in header

    result = trimesh.load(output_path, file_type="ply")
    assert len(result.vertices) == len(sample_mesh.vertices)
    assert len(result.faces) == len(sample_mesh.faces)
