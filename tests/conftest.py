import pytest

from dvc_streamlit.utils import get_dvc_repo


@pytest.fixture
def dvc_repo(tmp_path):
    return get_dvc_repo(
        "https://github.com/iterative/demo-fashion-mnist", tmp_path / "dvc_repo"
    )
