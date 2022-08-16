from recording import run_session
from get_figures import create_and_save_fig
from data_utils import find_subj_file_name, load_raw, json_save
from classifier import channel_search
from preprocessing import preprocess
import os
from constants import RECORDINGS_DIR

RESAMPLE_FREQ = 100
RESAMPLE_FLAG = True

def pipline_with_recording(subj_name):
    "This function record data and built classifier and figures"
    run_session()
    rec_folder_name = find_subj_file_name(subj_name)
    raw, rec_params = load_raw(rec_folder_name)
    create_and_save_fig(raw, rec_folder_name, RESAMPLE_FREQ, RESAMPLE_FLAG)
    c = clf(raw, RESAMPLE_FREQ)
    print(c)


def pipline_with_data(subj_name):
    ""
    rec_folder_name = find_subj_file_name(subj_name)
    raw, rec_params = load_raw(rec_folder_name)
    preprosess_raw = preprocess(raw)
    # create_and_save_fig(raw, rec_folder_name, RESAMPLE_FREQ, RESAMPLE_FLAG)
    # c = clf(raw, RESAMPLE_FREQ)
    best_params = channel_search(preprosess_raw, RESAMPLE_FREQ)
    json_save(os.path.join(RECORDINGS_DIR, rec_folder_name), "best_params.json", best_params)


if __name__ == "__main__":
    # pipline_with_data("Shaked")
    pipline_with_recording("Tzur")


