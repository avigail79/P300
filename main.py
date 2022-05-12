from recording1 import run_session
from use_data import load_rec_params_to_session, load_raw, find_subj_file
from get_figures import create_and_save_fig



def pipline(subj_name):
    rec_params = load_rec_params_to_session(subj_name)
    run_session(rec_params)
    rec_folder_name = find_subj_file(subj_name)
    raw, rec_params = load_raw(rec_folder_name)
    create_and_save_fig(raw)



if __name__ == "__main__":
    pipline('0')