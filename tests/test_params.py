import streamlit as st

from dvc_streamlit.params import dvc_params
from dvc_streamlit.rev_selector import rev_selector


def test_dvc_params_single(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: cnn (d34fd8c)",
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
                {
                    "train": {
                        "batch_size": 128,
                        "dropout": 0.4,
                        "hidden_units": 64,
                        "lr": 0.01,
                        "num_epochs": 10,
                    }
                }
            ),
        ]
    )


def test_dvc_params_multi(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Tag: cnn (d34fd8c)",
            "Tag: low-lr-experiment (b06a6ba)",
            "Branch: main (fc17c19)",
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
                {
                    "train": {
                        "batch_size": 128,
                        "dropout": 0.4,
                        "hidden_units": 64,
                        "lr": 0.01,
                        "num_epochs": 10,
                    }
                }
            ),
            mocker.call({"train": {"lr": 0.001}}),
            mocker.call({"train": {"lr": 0.001}}),
        ]
    )
