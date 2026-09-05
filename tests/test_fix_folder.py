import pytest
import trimesh

import fix_folder
from fix_folder import run_folder


def _write_box_stl(path, extents=(1.0, 2.0, 3.0)):
    path.parent.mkdir(parents=True, exist_ok=True)
    trimesh.creation.box(extents=extents).export(path, file_type="stl")


def test_processes_top_level_stls_only_by_default(tmp_path):
    _write_box_stl(tmp_path / "top.stl")
    _write_box_stl(tmp_path / "sub" / "nested.stl")

    results = run_folder(tmp_path, voxel_size=0.5)

    processed = {r["input"].name for r in results}
    assert processed == {"top.stl"}


def test_recursive_processes_nested_stls(tmp_path):
    _write_box_stl(tmp_path / "top.stl")
    _write_box_stl(tmp_path / "sub" / "nested.stl")

    results = run_folder(tmp_path, voxel_size=0.5, recursive=True)

    processed = {r["input"].name for r in results}
    assert processed == {"top.stl", "nested.stl"}
    assert all(r["error"] is None for r in results)


def test_default_output_naming_next_to_input(tmp_path):
    input_path = tmp_path / "part.stl"
    _write_box_stl(input_path)

    results = run_folder(tmp_path, voxel_size=0.5)

    assert len(results) == 1
    output_path = results[0]["output"]
    assert output_path == tmp_path / "part_mesh_fix.stl"
    assert output_path.exists()


def test_output_dir_mirrors_subfolders(tmp_path):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    _write_box_stl(input_dir / "top.stl")
    _write_box_stl(input_dir / "sub" / "nested.stl")

    results = run_folder(input_dir, voxel_size=0.5, output_dir=output_dir, recursive=True)

    outputs = {r["output"] for r in results}
    assert outputs == {output_dir / "top.stl", output_dir / "sub" / "nested.stl"}
    assert all(r["error"] is None for r in results)
    for output_path in outputs:
        assert output_path.exists()


def test_ignores_non_stl_files(tmp_path):
    _write_box_stl(tmp_path / "part.stl")
    (tmp_path / "notes.txt").write_text("not a mesh")

    results = run_folder(tmp_path, voxel_size=0.5)

    assert {r["input"].name for r in results} == {"part.stl"}


def test_continues_after_one_failure(tmp_path, monkeypatch):
    good_path = tmp_path / "good.stl"
    bad_path = tmp_path / "bad.stl"
    _write_box_stl(good_path)
    _write_box_stl(bad_path)

    real_run_pipeline = fix_folder.run_pipeline

    def flaky_run_pipeline(input_path, output_path, voxel_size, overwrite=False):
        if str(input_path) == str(bad_path):
            raise RuntimeError("simulated failure")
        return real_run_pipeline(input_path, output_path, voxel_size, overwrite=overwrite)

    monkeypatch.setattr(fix_folder, "run_pipeline", flaky_run_pipeline)

    results = run_folder(tmp_path, voxel_size=0.5)

    by_name = {r["input"].name: r for r in results}
    assert by_name["good.stl"]["error"] is None
    assert isinstance(by_name["bad.stl"]["error"], RuntimeError)


def test_existing_output_without_overwrite_is_a_logged_failure(tmp_path):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    _write_box_stl(input_dir / "part.stl")
    output_path = output_dir / "part.stl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"existing content")

    results = run_folder(input_dir, voxel_size=0.5, output_dir=output_dir)

    assert len(results) == 1
    assert isinstance(results[0]["error"], FileExistsError)
    assert output_path.read_bytes() == b"existing content"

    results = run_folder(input_dir, voxel_size=0.5, output_dir=output_dir, overwrite=True)

    assert results[0]["error"] is None
    assert output_path.read_bytes() != b"existing content"


def test_rerun_does_not_reprocess_its_own_output(tmp_path):
    _write_box_stl(tmp_path / "part.stl")

    first = run_folder(tmp_path, voxel_size=0.5)
    assert {r["input"].name for r in first} == {"part.stl"}

    second = run_folder(tmp_path, voxel_size=0.5)
    assert {r["input"].name for r in second} == {"part.stl"}
    assert not (tmp_path / "part_mesh_fix_mesh_fix.stl").exists()


def test_missing_input_directory_raises_immediately(tmp_path):
    with pytest.raises(NotADirectoryError):
        run_folder(tmp_path / "does_not_exist", voxel_size=0.5)


def test_full_pipeline_integration(tmp_path):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    for name in ("a.stl", "b.stl", "c.stl"):
        _write_box_stl(input_dir / name)

    results = run_folder(input_dir, voxel_size=0.5, output_dir=output_dir)

    assert len(results) == 3
    for result in results:
        assert result["error"] is None
        output_path = result["output"]
        assert output_path.exists()
        mesh = trimesh.load(output_path, file_type="stl")
        assert len(mesh.vertices) > 0
        assert len(mesh.faces) > 0
