import streamlit as st
from dvc.api import Repo as DvcRepo
from git import Repo as GitRepo


def get_dvc_repo(git_url, output_dir):
    GitRepo.clone_from(git_url, output_dir)
    return DvcRepo(output_dir)
