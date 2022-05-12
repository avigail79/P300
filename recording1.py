import matplotlib.pyplot as plt
import board
from constants import RECORDINGS_DIR, IMAGES_DIR
import datetime
import params
from params import *
from board import Board
import os
from pathlib import Path
import numpy as np
import json
from use_data import load_rec_params_to_session

BG_COLOR = "white"
STIM_COLOR = "black"


def run_session(rec_params):
    """
    This function record the experiment with board from brainflow.
    The markers now: is non_target-1 and target -9.
    :param rec_params: a dict
    :return: raw of mne.
    """

    # import psychopy only here to prevent pygame loading
    from psychopy import visual, core, event
    global visual, core, event

    # create the session set
    session_set = []
    target_set = []
    for i in range(rec_params['blocks_N']):
        block_set, block_target = create_block(rec_params['trials_N'], rec_params['odd percent'])
        session_set.append(block_set)
        target_set.append(block_target)

    # target_set_by_mark = [Marker.target.value for target in target_set_by_name]
    stims_dict = params.black_shapes  # todo

    # open window and stimulus
    win = visual.Window(color=BG_COLOR, fullscr=False)
    non_target = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict['NON_TARGET']}.png")
    target_1 = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict['TARGET_1']}.png")
    traget_2 = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict['TARGET_2']}.png")
    msg1 = visual.TextStim(win,
                           text=f"Hello {rec_params['subject name']}! \nPress any key to start. For exit press esc",
                           color=STIM_COLOR)
    msg2 = visual.TextStim(win, text=f"In this session will be {rec_params['blocks_N']} blocks. "
                                     f"\nYou need to count the number of the target shape. "
                                     f"\nPress qny key to start the session", color=STIM_COLOR)

    # start recording
    with Board(use_synthetic=rec_params['use_synthetic']) as board:

        # display starting massage
        show_stim_key_press(win, msg1)
        show_stim_key_press(win, msg2)

        for block_idx, block in enumerate(session_set):

            # get ready period
            board.insert_marker(target_set[block_idx].start_block_marker)
            show_get_ready(win,
                           progress_text(win, block_idx + 1, rec_params['blocks_N'],
                                         stim_name=stims_dict[target_set[block_idx].name]),
                           progress_image(win, stims_dict, target_set[block_idx].name),
                           rec_params['get ready duration'])

            # calibration period
            core.wait(rec_params['calibration duration'])

            # stimulus period
            for stim in block:
                board.insert_marker(stim.value)
                show_stim_and_fixation(win, stims_dict, stim.name, rec_params['StimOnset'], rec_params['interTime'])

        core.wait(0.5)
        win.close()
        raw = board.get_data()
    save_raw(raw, rec_params, session_set)
    core.quit()


def create_block(trials_N, odd_percent):
    low_freq_stim_N = math.floor(odd_percent * trials_N)
    block_set = [Marker.NON_TARGET] * (trials_N - 2 * low_freq_stim_N) + [Marker.TARGET_1] * low_freq_stim_N + \
                [Marker.TARGET_2] * low_freq_stim_N
    random.shuffle(block_set)
    block_traget = random.choice(Marker.all_target_stim())
    return block_set, block_traget


def show_stim_for_duration(win, vis_stim, duration):
    # Adding this code here is an easy way to make sure we check for an escape event before showing every stimulus
    if 'escape' in event.getKeys():
        core.quit()

    vis_stim.draw()
    win.flip()
    core.wait(duration)  # todo why this
    win.flip()


def show_get_ready(win, msg, image_target, duration):
    # Adding this code here is an easy way to make sure we check for an escape event before showing every stimulus
    if 'escape' in event.getKeys():
        core.quit()

    msg.draw()
    image_target.draw()
    win.flip()
    core.wait(duration)  # todo why this
    win.flip()


def show_stim_and_fixation(win, stims_dict, stim_name, StimOnset, interTime):
    # Adding this code here is an easy way to make sure we check for an escape event before showing every stimulus
    if 'escape' in event.getKeys():
        core.quit()

    vis_stim = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict[stim_name]}.png")
    fixation = visual.GratingStim(win=win, size=0.1, pos=[0, 0], sf=0, rgb=-1, mask='cross')  # , color=STIM_COLOR)

    vis_stim.draw()
    win.flip()
    core.wait(StimOnset)
    fixation.draw()
    win.flip()
    core.wait(interTime + float(np.random.normal(0, 1, 1)))  # adding noise (mean, std, num_of_elements)


def show_stim_key_press(win, txt_msg):
    txt_msg.draw()
    win.flip()
    keys_pressed = event.waitKeys()
    if 'escape' in keys_pressed:
        core.quit()



def find_stim_name(stim_num):
    if stim_num == Marker.NON_Target.value: return Marker.Target_1.name
    if stim_num == Marker.Target_1.value: return Marker.Target_1.name
    if stim_num == Marker.Target_2.value: return Marker.Target_2.name


def progress_text(win, done, blocks_N, stim_name):
    txt = visual.TextStim(win=win,
                          text=f'block {done}/{blocks_N}\n The current target is: {stim_name}\n get ready to count!',
                          color=STIM_COLOR, bold=True, alignHoriz='center', alignVert='center')
    txt.font = 'arial'
    txt.pos = (0, 0.2)
    return txt


def progress_image(win, stims_dict, stim_cls):
    img = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict[stim_cls]}.png")
    img.pos = (0, -0.2)
    img.size = (0.2)
    return img


def save_raw(raw, rec_params, session_set):
    folder_path = create_session_folder(rec_params['subject name'])
    raw.save(os.path.join(folder_path, "raw.fif"))

    with open(os.path.join(folder_path, "params.json"), "w") as f:
        json.dump(rec_params, f, ensure_ascii=False, indent=4)
    with open(os.path.join(folder_path, "session.json"), "w") as f:
        json.dump(session_set, f, ensure_ascii=False, indent=4)
    return os.path.basename(folder_path)


def create_session_folder(subj):
    folder_name = f'{datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}_{subj}'
    folder_path = os.path.join(RECORDINGS_DIR, folder_name)
    Path(folder_path).mkdir(exist_ok=True)
    return folder_path


if __name__ == "__main__":
    rec_params = load_rec_params_to_session()  # this us a dict todo: how to load this. now it is a params. i want that to be json
    run_session(rec_params)
