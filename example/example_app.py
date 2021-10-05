from pathlib import Path

import streamlit as st

from dvc_streamlit.metrics import dvc_metrics
from dvc_streamlit.rev_selector import rev_selector
from dvc_streamlit.utils import init_repo

st.set_page_config(layout="wide")

REPO_PATH = Path(__file__).parent / "dvc_repo"

st.sidebar.header("DVC Streamlit")
component = st.sidebar.radio(
    "Component",
    [
        "Metrics",
    ]
)

git_url = st.text_input("Git URL")

if git_url:
    dvc_repo = init_repo(git_url, REPO_PATH)
    selected_revs = rev_selector(dvc_repo)

    if component == "Metrics":
        dvc_metrics(dvc_repo, selected_revs)