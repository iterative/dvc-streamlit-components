import os
from pathlib import Path
from shutil import rmtree
from typing import Union

import streamlit as st

from dvc.api import Repo as DvcRepo
from git import Repo as GitRepo


def get_dvc_repo(git_url: str, output_dir: str):
    GitRepo.clone_from(git_url, output_dir)
    return DvcRepo(output_dir)

@st.cache(allow_output_mutation=True)
def init_repo(git_url: str, repo_path: str):
    if Path(repo_path).exists():
        rmtree(repo_path, ignore_errors=True)
    return get_dvc_repo(git_url, repo_path)
