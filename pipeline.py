from recording import run_session
from get_figures import create_and_save_fig
from data_folder import find_subj_file_name, load_raw
from features import clf


def pipline(subj_name, rec_flag):
    if rec_flag:
        run_session()
    rec_folder_name = find_subj_file_name(subj_name)
    raw = load_raw(rec_folder_name)
    create_and_save_fig(raw, rec_folder_name)
    c = clf(raw)
    print(c)

if __name__ == "__main__":
    pipline('Ido', False)


