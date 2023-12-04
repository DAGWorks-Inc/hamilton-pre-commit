from pathlib import Path
import pytest

from hamilton import driver
from hamilton_hooks import view_dag
from testing.util import get_resource_path


def test_success_with_dest_dir(tmp_path: Path):
    exit_code = view_dag.main([
        get_resource_path("valid_module_v1.py"),
        #"-d", str(tmp_path),
    ])

    assert exit_code == 0


@pytest.mark.parametrize("dest_dir", (None, "/dest/dir/"))
def test_viz_path_png_extension(dest_dir: str):
    fake_module_path = Path("/my/file/path/module.py")
    viz_path = view_dag.get_visualization_file_path(
        module_path=fake_module_path,
        dest_dir=dest_dir
    )
    assert viz_path.suffix == ".png"


def test_viz_not_found(tmp_path: Path):
    missing_file_path = tmp_path.joinpath("missing_file.png")
    hash = "abc"
    exit_code = view_dag.check_viz_commit(file_path=missing_file_path, file_hash=hash)
    assert exit_code is True

# v1 = '01645c116147b90fbda5c259fcb5dbdf04684d71'
# v2 = '52dc0b08db408e28381de60f35a90146eeb30a01'
# invalid = 'bd7806eec7aa465eb6ec3b0f0d56b5d5025d2d6f'

# def test_viz_not_found(tmp_path):
#     missing_file_path = tmp_path.joinpath("missing_file.png")
#     hash = "abc"
#     exit_code = view_dag.check_viz_commit(file_path=missing_file_path, file_hash=hash)
#     assert exit_code is True


def test_generate_viz_at_correct_path(tmp_path: Path):
    from testing.resources import valid_module_v1
    viz_path = tmp_path.joinpath("module.png")
    dr = (
        driver.Builder()
        .with_modules(valid_module_v1)
        .build()
    )
    view_dag.visualize_dag(dr=dr, file_path=viz_path)
    assert viz_path.exists()
