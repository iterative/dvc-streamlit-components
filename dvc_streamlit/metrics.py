from typing import List, Optional

import streamlit as st
from dvc.api import Repo
from dvc.utils.diff import _diff
from dvc.utils.flatten import unflatten

from dvc_streamlit.rev_selector import Rev


def dvc_metrics(dvc_repo: Repo, selected_revs: Optional[List[Rev]]) -> None:
    st.write("# DVC Metrics")
    if selected_revs:
        metrics = dvc_repo.metrics.show(
            revs=[rev.sha for rev in selected_revs]
        )
        st.write("## Metrics files")
        for file_name in metrics["workspace"]["data"]:
            show_file = st.checkbox(f"{file_name}")
            if show_file:
                columns = st.columns(len(selected_revs))
                for n, rev in enumerate(selected_revs):
                    with columns[n]:
                        st.write(f"### {rev.type}")
                        st.write(rev.name)
                        if n == 0:
                            first = metrics[rev.sha]["data"][file_name]["data"]
                            for k, v in sorted(first.items()):
                                st.metric(k, v)
                        else:
                            current = metrics[rev.sha]["data"][file_name][
                                "data"
                            ]
                            diff = unflatten(
                                _diff(first, current, with_unchanged=False)
                            )
                            for k, v in sorted(diff.items()):
                                st.metric(k, v["new"], v["diff"])
