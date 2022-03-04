import streamlit as st

from dvc_streamlit.params import dvc_params
from dvc_streamlit.rev_selector import rev_selector


def test_dvc_params_single(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: baseline-experiment (53b2d9d)",
        ],
    )
    mocker.patch("streamlit.checkbox", return_value=True)

    st_json = mocker.spy(st, "json")
    selected_revs = rev_selector(dvc_repo)

    dvc_params(dvc_repo, selected_revs)

    assert st_json.call_count == 1
    st_json.assert_has_calls(
        [
            mocker.call(
                {"train": {"min_split": 2, "n_est": 50, "seed": 20170428}}
            ),
        ]
    )


def test_dvc_params_multi(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: baseline-experiment (53b2d9d)",
            "Tag: bigrams-experiment (cc51022)",
            "Tag: random-forest-experiments (00071e8)",
        ],
    )
    mocker.patch("streamlit.checkbox", return_value=True)

    st_json = mocker.spy(st, "json")
    selected_revs = rev_selector(dvc_repo)

    dvc_params(dvc_repo, selected_revs)

    assert st_json.call_count == 3
    st_json.assert_has_calls(
        [
            mocker.call(
                {"train": {"min_split": 2, "n_est": 50, "seed": 20170428}}
            ),
            mocker.call({}),
            mocker.call({"train": {"n_est": 100, "min_split": 64}}),
        ]
    )
