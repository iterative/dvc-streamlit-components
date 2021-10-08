from pathlib import Path

import hiplot as hip
import pandas as pd
import streamlit as st
from dvc.utils.flatten import flatten


def dvc_experiments(dvc_repo):
    st.write("# DVC Experiments")

    columns = st.columns(3)
    with columns[0]:
        all_commits = st.checkbox("All commits", value=True)
    with columns[1]:
        all_branches = st.checkbox("All branches", value=False)
    with columns[2]:
        all_tags = st.checkbox("All tags", value=False)

    st.write("---")

    param_deps = st.checkbox("Param deps", value=True)

    all_experiments = dvc_repo.experiments.show(
        all_commits=all_commits,
        all_branches=all_branches,
        all_tags=all_tags,
        param_deps=param_deps,
    )

    experiments = []
    for k, v in all_experiments.items():
        experiment = {"uid": k}
        for p_name, p_val in flatten(v["baseline"]["data"]["params"]).items():
            experiment[Path(p_name).name.split(".")[-1]] = p_val
        for m_name, m_val in flatten(v["baseline"]["data"]["metrics"]).items():
            experiment[Path(m_name).name.split(".")[-1]] = m_val
        experiments.append(experiment)

    df = pd.DataFrame(experiments)
    df.dropna(inplace=True)
    df.drop_duplicates(
        subset=[x for x in df.columns if x != "uid"], inplace=True
    )

    st.dataframe(df)

    if len(df) > 1:
        xp = hip.Experiment.from_dataframe(df)
        xp.to_streamlit(ret="selected_uids", key="hip").display()
