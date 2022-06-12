from recording1 import run_session
from use_data import load_rec_params_to_session, load_raw, find_subj_file_name
from get_figures import create_and_save_fig, crop_data
from preprocessing import down_sampling
from features import concatenate_matrix, clf


def record_pipline(subj_name):
    rec_params = load_rec_params_to_session(subj_name)
    run_session()
    rec_folder_name = find_subj_file_name(subj_name)
    raw, rec_params = load_raw(rec_folder_name)
    create_and_save_fig(raw, rec_folder_name)


def use_record_data(rec_folder_name):
    #down sampling
    raw, rec_params = load_raw(rec_folder_name)
    raw_blocks = crop_data(raw)
    # first_block = raw_blocks[0]
    for b in raw_blocks:
        down_sampling(b, 100)


if __name__ == "__main__":
    # record_pipline('99')
    # use_recording_data(2022-05-17--12-30-48_IDO2)
    rec_folder_name = find_subj_file_name('Ido')
    raw, rec_params = load_raw(rec_folder_name)
    # down_sampling(raw, 100)
    # create_and_save_fig(raw, rec_folder_name)
    # concatenate_matrix(raw, 100)
    c = clf(raw)
    print(c)