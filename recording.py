from constants import RECORDINGS_DIR, IMAGES_DIR
from board import Board
import os
import numpy as np
from GUI import GUI
from data_folder import create_session_folder, json_save
from Marker import Marker
import random

BG_COLOR = "white"
STIM_COLOR = "black"


def run_session():
    """
    This function record the experiment with board from brainflow.
    The markers now: is non_target-1 and target -9.
    :param rec_params: a dict
    :return: raw of mne.
    """

    # import psychopy only here to prevent pygame loading
    from psychopy import visual, core, event
    global visual, core, event

    # open GUI and insert the rec params
    g = GUI()
    rec_params = g.run_gui()
    stims_dict = rec_params['Stimulus Type']

    # create the session set
    session_set = []
    target_set = []
    for i in range(rec_params['blocks_N']):
        block_set, block_target = create_block(rec_params['trials_N'], rec_params['odd percent'])
        session_set.append(block_set)
        target_set.append(block_target)

    # open window and stimulus
    win = visual.Window(color=BG_COLOR, fullscr=False)
    msg1 = visual.TextStim(win,
                           text=f"Hello {rec_params['Subject name']}! \nPress any key to start. For exit press esc",
                           color=STIM_COLOR)
    msg2 = visual.TextStim(win, text=f"In this session will be {rec_params['blocks_N']} blocks. "
                                     f"\nYou need to count the number of the target shape. "
                                     f"\nPress any key to start the session", color=STIM_COLOR)

    # start recording
    with Board(use_synthetic=rec_params['Use synthetic']) as board:

        # display starting massage
        show_stim_key_press(win, msg1)
        show_stim_key_press(win, msg2)

        for block_idx, block in enumerate(session_set):

            # get ready period
            core.wait(rec_params['calibration duration'])
            show_get_ready(win,
                           progress_text(win, block_idx + 1, rec_params['blocks_N'],
                                         stim_name=stims_dict[target_set[block_idx].name]),
                           progress_image(win, stims_dict, target_set[block_idx].name),
                           rec_params['get ready duration'])
            board.insert_marker(target_set[block_idx].start_block_marker)

            # calibration period
            core.wait(rec_params['calibration duration'])

            # stimulus period
            for stim in block:
                board.insert_marker(stim.value)
                show_stim_and_fixation(win, stims_dict, stim.name, rec_params['StimOnset'], rec_params['interTime'])

        core.wait(0.5)
        win.close()
        raw = board.get_data()
    save_raw(raw, {'session set': session_set, 'target set': target_set}, rec_params['Subject name'])
    core.quit()


def create_block(trials_N, odd_percent):
    trials = np.random.uniform(0, 1, trials_N)
    block_traget = random.choice(Marker.all_target_stim())
    block_set = []
    for i in trials:
        if i < odd_percent:  # target
            block_set.append(block_traget)
        elif odd_percent <= i < odd_percent * 2:  # distracting
            if block_traget == Marker.TARGET_2:
                block_set.append(Marker.TARGET_1)
            else:
                block_set.append(Marker.TARGET_2)
        else:
            block_set.append(Marker.NON_TARGET)  # non-target
    return block_set, block_traget


def show_get_ready(win, msg, image_target, duration):
    # Adding this code here is an easy way to make sure we check for an escape event before showing every stimulus
    if 'escape' in event.getKeys():
        core.quit()

    msg.draw()
    image_target.draw()
    win.flip()
    core.wait(duration)
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
    core.wait(interTime + float(np.random.uniform(0, 0.2)))  # adding noise


def show_stim_key_press(win, txt_msg):
    txt_msg.draw()
    win.flip()
    keys_pressed = event.waitKeys()
    if 'escape' in keys_pressed:
        core.quit()


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


def save_raw(raw, session_set, subj_name):
    folder_path = create_session_folder(subj_name)
    raw.save(os.path.join(folder_path, "raw.fif"))
    json_save(folder_path, "session.json", session_set)
    return os.path.basename(folder_path)


if __name__ == "__main__":
    run_session()
