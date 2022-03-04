from dvc_streamlit.rev_selector import Rev, rev_selector


def test_rev_selector(dvc_repo, mocker):
    mocker.patch(
        "streamlit.multiselect",
        return_value=[
            "Commit: Run experiments tuning random forest params (00071e8)",
            "Branch: master (00071e8)",
            "Tag: baseline-experiment (53b2d9d)",
        ],
    )

    selected_revs = rev_selector(dvc_repo)
    assert all(isinstance(x, Rev) for x in selected_revs)
    assert selected_revs[0].type == "Commit"
    assert selected_revs[1].type == "Branch"
    assert selected_revs[2].type == "Tag"
