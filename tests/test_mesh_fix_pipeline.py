import pytest
import trimesh

from mesh_fix import run_pipeline


def test_run_pipeline_produces_stl_with_geometry(tmp_path, sample_stl):
    output_path = tmp_path / "fixed.stl"

    run_pipeline(str(sample_stl), str(output_path), voxel_size=0.5)

    assert output_path.exists()
    result = trimesh.load(output_path, file_type="stl")
    assert len(result.vertices) > 0
    assert len(result.faces) > 0


def test_run_pipeline_refuses_to_overwrite_by_default(tmp_path, sample_stl):
    output_path = tmp_path / "fixed.stl"
    output_path.write_bytes(b"existing content")

    with pytest.raises(FileExistsError):
        run_pipeline(str(sample_stl), str(output_path), voxel_size=0.5)

    assert output_path.read_bytes() == b"existing content"


def test_run_pipeline_overwrites_when_permitted(tmp_path, sample_stl):
    output_path = tmp_path / "fixed.stl"
    output_path.write_bytes(b"existing content")

    run_pipeline(str(sample_stl), str(output_path), voxel_size=0.5, overwrite=True)

    assert output_path.read_bytes() != b"existing content"
