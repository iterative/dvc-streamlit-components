import pytest

from dvc_streamlit.utils import get_dvc_repo


@pytest.fixture(scope="session")
def dvc_repo(tmpdir_factory):
    output_dir = tmpdir_factory.mktemp('dvc_repo')
    return get_dvc_repo(
        "https://github.com/iterative/demo-fashion-mnist",
        output_dir,
    )
