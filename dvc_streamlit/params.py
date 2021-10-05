from typing import List, Optional

import streamlit as st
from dvc.api import Repo
from dvc.utils.diff import _diff
from dvc.utils.flatten import unflatten

from dvc_streamlit.rev_selector import Rev


def dvc_params(dvc_repo: Repo, selected_revs: Optional[List[Rev]]) -> None:
    st.write("# DVC Params")
    deps = st.checkbox(
        "Deps", help="Include only parameters that are stage dependencies."
    )
    if selected_revs:
        params = dvc_repo.params.show(
            revs=[rev.sha for rev in selected_revs], deps=deps
        )
        st.write("## Params files")
        for file_name in params["workspace"]["data"]:
            show_file = st.checkbox(f"{file_name}")
            if show_file:
                columns = st.columns(len(selected_revs))
                for n, rev in enumerate(selected_revs):
                    with columns[n]:
                        st.write(f"### {rev.type}")
                        st.write(rev.name)
                        if n == 0:
                            first = params[rev.sha]["data"][file_name]["data"]
                            st.json(first)
                        else:
                            current = params[rev.sha]["data"][file_name][
                                "data"
                            ]
                            diff = _diff(first, current, with_unchanged=False)
                            for k, v in diff.items():
                                diff[k] = v["new"]
                            st.json(unflatten(diff))
