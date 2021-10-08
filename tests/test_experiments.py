import hiplot as hip
import streamlit as st

from dvc_streamlit.experiments import dvc_experiments


def test_dvc_experimets(dvc_repo, mocker):
    mocker.patch("hiplot.Experiment.to_streamlit")
    st_dataframe = mocker.spy(st, "dataframe")
    hip_dataframe = mocker.spy(hip.Experiment, "from_dataframe")

    dvc_experiments(dvc_repo)

    assert st_dataframe.call_count == 1
    assert hip_dataframe.call_count == 1


def test_dvc_experimets_single(dvc_repo, mocker):
    def checkbox_side_effect(*args, **kwargs):
        if args[0] == "All branches":
            return True
        return False

    mocker.patch("streamlit.checkbox", side_effect=checkbox_side_effect)
    mocker.patch("hiplot.Experiment.to_streamlit")
    st_dataframe = mocker.spy(st, "dataframe")
    hip_dataframe = mocker.spy(hip.Experiment, "from_dataframe")

    dvc_experiments(dvc_repo)

    assert st_dataframe.call_count == 1
    assert hip_dataframe.call_count == 0
