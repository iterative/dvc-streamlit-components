from collections import defaultdict
from typing import List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dvc.api import Repo

from dvc_streamlit.rev_selector import Rev


def dvc_plots(dvc_repo: Repo, selected_revs: Optional[List[Rev]]) -> None:
    st.write("# DVC Plots")

    if selected_revs:
        sha_to_name = {
            rev.sha: f"{rev.type}: {rev.name}" for rev in selected_revs
        }
        plots = dvc_repo.plots.show(revs=[rev.sha for rev in selected_revs])

        plot_files_to_list = defaultdict(list)
        for rev in plots:
            for file in plots[rev]["data"]:
                data = []
                for row in plots[rev]["data"][file]["data"]:
                    row["rev"] = rev
                    data.append(row)
                plot_files_to_list[file].extend(data)

        dfs = {k: pd.DataFrame(v) for k, v in plot_files_to_list.items()}

        all_columns = []
        for k, v in dfs.items():
            all_columns.extend([f"{k}: {column}" for column in v.columns])

        template = st.radio("Template", ["linear", "scatter"])

        x_axis = st.selectbox("X", all_columns)
        y_axis = st.multiselect("Y", all_columns)
        if x_axis and y_axis:
            x_file, x_column = x_axis.replace(" ", "").split(":")
            x = [float(x) for x in dfs[x_file][x_column]]
            fig = go.Figure()
            for y_trace in y_axis:
                y_file, y_column = y_trace.replace(" ", "").split(":")
                for n, (rev, df) in enumerate(dfs[y_file].groupby("rev")):
                    y = [float(val) for val in df[y_column]]
                    fig.add_trace(
                        go.Scatter(
                            x=x,
                            y=y,
                            mode="lines+markers"
                            if template == "linear"
                            else "markers",
                            line=dict(color=px.colors.qualitative.Plotly[n]),
                            name=sha_to_name[rev].split(" (")[0][:30],
                            legendgroup=sha_to_name[rev].split(" (")[0][:30],
                        )
                    )

            st.plotly_chart(fig)
