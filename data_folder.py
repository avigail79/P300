import os
from pathlib import Path
import datetime
import json
from constants import RECORDINGS_DIR
import mne


def create_session_folder(subj):
    folder_name = f'{datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}_{subj}'
    folder_path = os.path.join(RECORDINGS_DIR, folder_name)
    Path(folder_path).mkdir(exist_ok=True)
    return folder_path


def json_save(folder_path, j_name, j_save):
    with open(os.path.join(folder_path, j_name), "w") as f:
        json.dump(j_save, f, ensure_ascii=False, indent=4)


def json_load(load_path):
    with open(load_path) as file:
        return json.load(file)


def find_subj_file_name(subj_name, path=RECORDINGS_DIR):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            if d[-len(subj_name):] == subj_name:
                return d


def load_raw(rec_folder_name):
    rec_folder_path = os.path.join(RECORDINGS_DIR, rec_folder_name)
    raw = mne.io.read_raw_fif(os.path.join(rec_folder_path, 'raw.fif'))
    rec_params_path = os.path.join(os.path.join(rec_folder_path, 'params.json'))
    # session_path = os.path.join(os.path.join(rec_folder_path, 'session.json'))
    rec_params = json_load(rec_params_path)
    # session = json_load(session_path)
    return raw



# if __name__ == "__main__":
#     find_subj_file_name('Ido')