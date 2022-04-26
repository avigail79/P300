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


BG_COLOR = "white"
STIM_COLOR = "black"


def run_session(rec_params):

    # import psychopy only here to prevent pygame loading
    from psychopy import visual, core, event
    global visual, core, event

    # GUI
    stims_dict = params.black_shapes

    # # create list of random trials
    # session_set = params.create_session_set(params["blocks_N"], params["trials_N"])
    # target_set = params.create_target_set(blocks_N)


    # open window and display starting massage
    win = visual.Window(color=BG_COLOR, fullscr=False)
    msg1 = visual.TextStim(win, text=f"Hello {rec_params['subject_name']}! \nPress any key to start. For exit press esc", color=STIM_COLOR)
    msg2 = visual.TextStim(win, text=f"In this session will be {rec_params['blocks_N']} blocks. "
                                     f"\nYou need to count the number of the target shape. "
                                     f"\nPress qny key to start the session", color=STIM_COLOR)
    fixation = visual.GratingStim(win=win, size=0.1, pos=[0,0], sf=0, rgb=-1, mask='cross')#, color=STIM_COLOR)
    show_stim_key_press(win, msg1)
    show_stim_key_press(win, msg2)

    # open stimulus
    NON_Target = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict['NON_TARGET'][0]}.png")
    Target_1 = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict['TARGET_1'][0]}.png")
    Target_2 = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict['TARGET_2'][0]}.png")
    # todo: maybe change all the position. more confusing
    # NON_TARGET.pos = (-0.2, 0.1)
    # TARGET_1.pos = (-0.1, -0.1)
    # TARGET_2.pos = (0.1,0)


    # get_ready_msg = visual.TextStim(win, text="In this block Your target now is to count the __", color=STIM_COLOR)

    # start recording
    with Board(use_synthetic=rec_params['use_synthetic']) as board:
        for block_i in range(rec_params['blocks_N']):
            # marker the start
            if stims_dict[rec_params['target_set'][block_i]][1] == 1:
                board.insert_marker(Marker.start_with_target_1.value)
            else:
                board.insert_marker(Marker.start_with_target_2.value)
            # board.insert_marker(int(f"9{stims_dict[rec_params['target_set'][block_i]][1]}")) #todo

            # get ready period
            show_get_ready(win, progress_text(win, block_i + 1, rec_params['blocks_N'], rec_params['target_set'][block_i]),
                           progress_image(stims_dict, win, rec_params['target_set'][block_i]),
                           rec_params['get_ready_duration'])

            # calibration period
            core.wait(rec_params['calibration_duration'])

            # stimulus period
            for stim_num in rec_params['session_set'][block_i]:
                if stim_num == Marker.NON_Target.value:
                    board.insert_marker(stim_num)
                    show_stim_and_fixation(win, NON_Target, fixation, rec_params['StimOnset'], rec_params['interTime'])
                if stim_num == Marker.Target_1.value:
                    board.insert_marker(stim_num)
                    show_stim_and_fixation(win, Target_1, fixation, rec_params['StimOnset'], rec_params['interTime'])
                if stim_num == Marker.Target_2.value:
                    board.insert_marker(stim_num)
                    show_stim_and_fixation(win, Target_2, fixation, rec_params['StimOnset'], rec_params['interTime'])

        core.wait(0.5)
        win.close()
        raw = board.get_data()
    save_raw(raw, rec_params)
    core.quit()


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


def show_stim_and_fixation(win, vis_stim, fixation, StimOnset, interTime):
    # Adding this code here is an easy way to make sure we check for an escape event before showing every stimulus
    if 'escape' in event.getKeys():
        core.quit()

    vis_stim.draw()
    win.flip()
    core.wait(StimOnset)
    fixation.draw()
    win.flip()
    core.wait(interTime + float(np.random.normal(0,1,1)))  # adding noise (mean, std, num_of_elements)


def show_stim_key_press(win, txt_msg):
    txt_msg.draw()
    win.flip()
    keys_pressed = event.waitKeys()
    if 'escape' in keys_pressed:
        core.quit()


def progress_text(win, done, blocks_N, stim_name):
    txt = visual.TextStim(win=win, text=f'block {done}/{blocks_N}\n The current target is: {stim_name}\n get ready to count!',
                          color=STIM_COLOR, bold=True, alignHoriz='center', alignVert='center')
    txt.font = 'arial'
    txt.pos = (0, 0.2)
    return txt


def progress_image(stims_dict, win, stim_marker_name):
    img = visual.ImageStim(win, image=f"{IMAGES_DIR}/{stims_dict[stim_marker_name][0]}.png")
    img.pos = (0, -0.2)
    img.size = (0.2)
    return img


def save_raw(raw, rec_params):
    folder_path = create_session_folder(rec_params['subject_name'])
    raw.save(os.path.join(folder_path, "raw.fif"))

    with open(os.path.join(folder_path, "params.json"), "w") as f:
        json.dump(rec_params, f, ensure_ascii=False, indent=4)
    return os.path.basename(folder_path)


def create_session_folder(subj):
    folder_name = f'{datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}_{subj}'
    folder_path = os.path.join(RECORDINGS_DIR, folder_name)
    Path(folder_path).mkdir(exist_ok=True)
    return folder_path


if __name__ == "__main__":
    rec_params = params.total_rec_params()
    run_session(rec_params)