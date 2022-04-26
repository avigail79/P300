import json
import mne
import os

import params
from constants import RECORDINGS_DIR, RECORDING_PARAMS_PATH
import matplotlib.pyplot as plt
from preprocessing import preprocess
from pathlib import Path
from Marker import Marker
from g import get_epochs


SYNTHETIC_SUBJECT_NAME = "Synthetic"


def load_rec_params_to_session() -> dict:
    # rec_params = json_load(RECORDING_PARAMS_PATH)
    # return rec_params
    params.GUI.update(params.session_params)
    if params.GUI["use_synthetic"]:
        params.GUI["subject"] = SYNTHETIC_SUBJECT_NAME
    return params.GUI


def json_load(load_path):
    with open(load_path) as file:
        return json.load(file)


def load_raw(rec_folder_name):
    rec_folder_path = os.path.join(RECORDINGS_DIR, rec_folder_name)
    raw = mne.io.read_raw_fif(os.path.join(rec_folder_path, 'raw.fif'))
    rec_params_path = os.path.join(os.path.join(rec_folder_path, 'params.json'))
    session_path = os.path.join(os.path.join(rec_folder_path, 'session.json'))
    rec_params = json_load(rec_params_path)
    session = json_load(session_path)
    return raw, rec_params #, session


