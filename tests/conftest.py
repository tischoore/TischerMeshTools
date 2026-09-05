import sys
from pathlib import Path

import trimesh
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def sample_mesh():
    return trimesh.creation.box(extents=(1.0, 2.0, 3.0))


@pytest.fixture
def sample_stl(tmp_path, sample_mesh):
    stl_path = tmp_path / "sample.stl"
    sample_mesh.export(stl_path, file_type="stl")
    return stl_path
