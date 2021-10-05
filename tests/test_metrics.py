import streamlit as st

from dvc_streamlit.metrics import dvc_metrics
from dvc_streamlit.rev_selector import rev_selector


def test_dvc_metrics_single(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: baseline-nn-experiment (02b68b7)",
        ],
    )
    mocker.patch("streamlit.checkbox", return_value=True)

    st_metric = mocker.spy(st, "metric")
    selected_revs = rev_selector(dvc_repo)

    dvc_metrics(dvc_repo, selected_revs)

    assert st_metric.call_count == 2
    st_metric.assert_has_calls(
        [
            mocker.call("accuracy", 0.8482999801635742),
            mocker.call("loss", 0.4460402727127075)
        ],
        any_order=True
    ) 


def test_dvc_metrics_multi(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: baseline-nn-experiment (02b68b7)",
            "Tag: cnn (d34fd8c)",
            "Tag: low-lr-experiment (b06a6ba)"
        ],
    )
    mocker.patch("streamlit.checkbox", return_value=True)

    st_metric = mocker.spy(st, "metric")
    selected_revs = rev_selector(dvc_repo)

    dvc_metrics(dvc_repo, selected_revs)

    assert st_metric.call_count == 6
    st_metric.assert_has_calls(
        [
            mocker.call("accuracy", 0.8928999900817871, 0.04460000991821289),
            mocker.call("accuracy", 0.909500002861023, 0.06120002269744873),
        ],
        any_order=True
    ) 