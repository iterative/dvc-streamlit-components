import plotly.graph_objects as go
import streamlit as st

from dvc_streamlit.plots import dvc_plots
from dvc_streamlit.rev_selector import rev_selector


def test_dvc_plots_single(dvc_repo, mocker):
    def multiselect_side_effect(*args, **kwargs):
        if args[0] == "Select Revisions":
            return ["Tag: baseline-experiment (53b2d9d)"]
        elif args[0] == "X":
            return ["prc.json: recall"]
        elif args[0] == "Y":
            return ["prc.json: precision"]

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
            return ["Tag: baseline-experiment (53b2d9d)"]
        elif args[0] == "X":
            return ["prc.json: recall"]
        elif args[0] == "Y":
            return ["prc.json: precision", "prc.json: precision"]

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
                "Tag: baseline-experiment (53b2d9d)",
                "Tag: bigrams-experiment (cc51022)",
            ]
        elif args[0] == "X":
            return ["prc.json: recall"]
        elif args[0] == "Y":
            return ["prc.json: precision"]

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
                "Tag: baseline-experiment (53b2d9d)",
                "Tag: bigrams-experiment (cc51022)",
            ]
        elif args[0] == "X":
            return ["prc.json: recall"]
        elif args[0] == "Y":
            return ["prc.json: precision", "prc.json: precision"]

    mocker.patch("streamlit.multiselect", side_effect=multiselect_side_effect)

    st_plotly = mocker.spy(st, "plotly_chart")
    add_trace = mocker.spy(go.Figure, "add_trace")

    selected_revs = rev_selector(dvc_repo)

    dvc_plots(dvc_repo, selected_revs)

    assert st_plotly.call_count == 1
    assert add_trace.call_count == 4
