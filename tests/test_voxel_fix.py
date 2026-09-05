import pytest
import trimesh

from voxel_fix import convert


@pytest.fixture
def sample_ply(tmp_path, sample_mesh):
    ply_path = tmp_path / "sample.ply"
    sample_mesh.export(ply_path, file_type="ply", encoding="binary")
    return ply_path


def test_convert_produces_binary_ply_with_geometry(tmp_path, sample_ply):
    output_path = tmp_path / "fixed.ply"

    convert(str(sample_ply), str(output_path), voxel_size=0.5)

    assert output_path.exists()
    with open(output_path, "rb") as f:
        header = f.read(40)
    assert b"format binary" in header

    result = trimesh.load(output_path, file_type="ply")
    assert len(result.vertices) > 0
    assert len(result.faces) > 0
