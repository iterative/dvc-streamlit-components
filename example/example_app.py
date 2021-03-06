from pathlib import Path

import streamlit as st

from dvc_streamlit import (dvc_experiments, dvc_metrics, dvc_params, dvc_plots, dvc_repo,
                           rev_selector)

st.set_page_config(layout="wide")

REPO_PATH = Path(__file__).parent / "dvc_repo"

st.sidebar.header("DVC Streamlit")
component = st.sidebar.radio("Component", ["Metrics", "Params", "Plots", "Experiments"])

git_url = st.text_input("Git URL", value="https://github.com/iterative/example-get-started")

if git_url:
    dvc_repo = dvc_repo(git_url, REPO_PATH)

    if component != "Experiments":
        selected_revs = rev_selector(dvc_repo)

    if component == "Metrics":
        dvc_metrics(dvc_repo, selected_revs)
    elif component == "Params":
        dvc_params(dvc_repo, selected_revs)
    elif component == "Plots":
        dvc_plots(dvc_repo, selected_revs)
    elif component == "Experiments":
        dvc_experiments(dvc_repo)
