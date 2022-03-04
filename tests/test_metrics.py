import streamlit as st

from dvc_streamlit.metrics import dvc_metrics
from dvc_streamlit.rev_selector import rev_selector


def test_dvc_metrics_single(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: baseline-experiment (53b2d9d)",
        ],
    )
    mocker.patch("streamlit.checkbox", return_value=True)

    st_metric = mocker.spy(st, "metric")
    selected_revs = rev_selector(dvc_repo)

    dvc_metrics(dvc_repo, selected_revs)

    assert st_metric.call_count == 2
    st_metric.assert_has_calls(
        [
            mocker.call("avg_prec", 0.5204838673030754),
            mocker.call("roc_auc", 0.9032012604172255),
        ],
        any_order=True,
    )


def test_dvc_metrics_multi(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: baseline-experiment (53b2d9d)",
            "Tag: bigrams-experiment (cc51022)",
            "Tag: random-forest-experiments (00071e8)",
        ],
    )
    mocker.patch("streamlit.checkbox", return_value=True)

    st_metric = mocker.spy(st, "metric")
    selected_revs = rev_selector(dvc_repo)

    dvc_metrics(dvc_repo, selected_revs)

    assert st_metric.call_count == 6
    st_metric.assert_has_calls(
        [
            mocker.call("avg_prec", 0.6040544652105823, 0.08357059790750687),
            mocker.call("roc_auc", 0.9608017142900953, 0.05760045387286983),
        ],
        any_order=True,
    )
