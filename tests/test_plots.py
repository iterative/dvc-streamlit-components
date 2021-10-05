import plotly.graph_objects as go
import streamlit as st

from dvc_streamlit.plots import dvc_plots
from dvc_streamlit.rev_selector import rev_selector


def test_dvc_plots_single(dvc_repo, mocker):
    def multiselect_side_effect(*args, **kwargs):
        if args[0] == "Select Revisions":
            return ["Tag: cnn (d34fd8c)"]
        elif args[0] == "Y":
            return ["output/train_logs.csv: accuracy"]

    mocker.patch("streamlit.multiselect", side_effect=multiselect_side_effect)

    st_plotly = mocker.spy(st, "plotly_chart")
    add_trace = mocker.spy(go.Figure, "add_trace")

    selected_revs = rev_selector(dvc_repo)

    dvc_plots(dvc_repo, selected_revs)

    assert st_plotly.call_count == 1
    assert add_trace.call_count == 1


def test_dvc_multi_y(dvc_repo, mocker):
    def multiselect_side_effect(*args, **kwargs):
        if args[0] == "Select Revisions":
            return ["Tag: cnn (d34fd8c)"]
        elif args[0] == "Y":
            return [
                "output/train_logs.csv: accuracy",
                "output/train_logs.csv: loss",
            ]

    mocker.patch("streamlit.multiselect", side_effect=multiselect_side_effect)

    st_plotly = mocker.spy(st, "plotly_chart")
    add_trace = mocker.spy(go.Figure, "add_trace")

    selected_revs = rev_selector(dvc_repo)

    dvc_plots(dvc_repo, selected_revs)

    assert st_plotly.call_count == 1
    assert add_trace.call_count == 2


def test_dvc_multi_rev(dvc_repo, mocker):
    def multiselect_side_effect(*args, **kwargs):
        if args[0] == "Select Revisions":
            return [
                "Tag: cnn (d34fd8c)",
                "Tag: low-lr-experiment (b06a6ba)",
            ]
        elif args[0] == "Y":
            return ["output/train_logs.csv: accuracy"]

    mocker.patch("streamlit.multiselect", side_effect=multiselect_side_effect)

    st_plotly = mocker.spy(st, "plotly_chart")
    add_trace = mocker.spy(go.Figure, "add_trace")

    selected_revs = rev_selector(dvc_repo)

    dvc_plots(dvc_repo, selected_revs)

    assert st_plotly.call_count == 1
    assert add_trace.call_count == 2


def test_dvc_multi_y_and_multi_rev(dvc_repo, mocker):
    def multiselect_side_effect(*args, **kwargs):
        if args[0] == "Select Revisions":
            return [
                "Tag: cnn (d34fd8c)",
                "Tag: low-lr-experiment (b06a6ba)",
            ]
        elif args[0] == "Y":
            return [
                "output/train_logs.csv: accuracy",
                "output/train_logs.csv: loss",
            ]

    mocker.patch("streamlit.multiselect", side_effect=multiselect_side_effect)

    st_plotly = mocker.spy(st, "plotly_chart")
    add_trace = mocker.spy(go.Figure, "add_trace")

    selected_revs = rev_selector(dvc_repo)

    dvc_plots(dvc_repo, selected_revs)

    assert st_plotly.call_count == 1
    assert add_trace.call_count == 4
