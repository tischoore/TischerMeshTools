import pytest
import trimesh

from ply_to_stl import convert


@pytest.fixture
def sample_ply(tmp_path, sample_mesh):
    ply_path = tmp_path / "sample.ply"
    sample_mesh.export(ply_path, file_type="ply", encoding="binary")
    return ply_path


def test_convert_produces_stl_with_matching_geometry(tmp_path, sample_ply, sample_mesh):
    output_path = tmp_path / "sample.stl"

    convert(str(sample_ply), str(output_path))

    assert output_path.exists()
    result = trimesh.load(output_path, file_type="stl")
    assert len(result.vertices) == len(sample_mesh.vertices)
    assert len(result.faces) == len(sample_mesh.faces)


def test_convert_refuses_to_overwrite_by_default(tmp_path, sample_ply):
    output_path = tmp_path / "sample.stl"
    output_path.write_bytes(b"existing content")

    with pytest.raises(FileExistsError):
        convert(str(sample_ply), str(output_path))

    assert output_path.read_bytes() == b"existing content"


def test_convert_overwrites_when_permitted(tmp_path, sample_ply):
    output_path = tmp_path / "sample.stl"
    output_path.write_bytes(b"existing content")

    convert(str(sample_ply), str(output_path), overwrite=True)

    assert output_path.read_bytes() != b"existing content"
