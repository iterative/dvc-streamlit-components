from dataclasses import dataclass
from typing import Dict, List, Optional

import streamlit as st
from dvc.api import Repo


@dataclass
class Rev:
    type: str
    name: str
    sha: str

    def __repr__(self) -> str:
        return f"{self.type}: {self.name} ({self.sha[:7]})"


def rev_selector(dvc_repo: Repo) -> Optional[List[Rev]]:

    revs: List[Rev] = []
    revs += [
        Rev("Commit", commit.message.strip(), commit.hexsha)
        for commit in dvc_repo.scm.gitpython.repo.iter_commits()
    ]
    revs += [
        Rev("Branch", branch.name, branch.commit.hexsha)
        for branch in dvc_repo.scm.gitpython.repo.branches
    ]
    revs += [
        Rev("Tag", tag.name, tag.commit.hexsha)
        for tag in dvc_repo.scm.gitpython.repo.tags
    ]

    # TODO investigate exception raised
    # https://github.com/streamlit/streamlit/blob/develop/lib/streamlit/elements/multiselect.py#L125
    # When passing directly list of dataclasses
    selected_revs_str = st.multiselect(
        "Select Revisions", [str(x) for x in revs]
    )

    rev_str_to_object: Dict[str, Rev] = {str(x): x for x in revs}

    if selected_revs_str:
        return [rev_str_to_object[x] for x in selected_revs_str]
