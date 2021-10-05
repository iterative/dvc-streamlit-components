from pathlib import Path
from shutil import rmtree

import streamlit as st

from dvc_streamlit.rev_selector import rev_selector
from dvc_streamlit.utils import get_dvc_repo

repo_path = Path(__file__).parent / "dvc_repo"


@st.cache(allow_output_mutation=True)
def init_repo(git_url):
    if repo_path.exists():
        rmtree(repo_path, ignore_errors=True)
    return get_dvc_repo(git_url, repo_path)


git_url = st.text_input("Git URL")

if git_url:
    dvc_repo = init_repo(git_url)
    selected_revs = rev_selector(dvc_repo)
