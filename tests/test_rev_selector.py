import streamlit as st

from dvc_streamlit.rev_selector import Rev, rev_selector


def test_rev_selector(dvc_repo, mocker):
    mocker.patch("streamlit.multiselect", return_value=[
        "Commit: Build and evaluate CNN (d34fd8c)",
        "Branch: main (fc17c19)",
        "Tag: neural-net (02b68b7)"
    ])

    selected_revs = rev_selector(dvc_repo)
    assert all(isinstance(x, Rev) for x in selected_revs)
    assert selected_revs[0].type == "Commit"
    assert selected_revs[1].type == "Branch"
    assert selected_revs[2].type == "Tag"
