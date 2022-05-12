import numpy as np
from mne.viz import plot_compare_evokeds

import Marker
from use_data import load_raw
from preprocessing import preprocess
import matplotlib.pyplot as plt
import os
import mne
from constants import RECORDINGS_DIR
from pathlib import Path


FREQ_RANGE = (6, 30)


def crop_data(raw):
    """
    The function returns dict. key = start block time, val = [target type, raw].
    """
    events = mne.find_events(raw)
    start_event = [event for event in events if event[2] == 91 or event[2] == 92]
    start_data = {data[0] / raw.info['sfreq']: data[2] for data in start_event}
    raw_blocks = {}
    keys = list(start_data.keys())
    for i, block_time in enumerate(keys):
        raw_copy = mne.io.Raw.copy(raw)
        if i == (len(keys)-1):
            raw_blocks[block_time] = [start_data[block_time], raw_copy.crop(tmin=block_time, include_tmax=True)]
        else:
            raw_blocks[block_time] = [start_data[block_time], raw_copy.crop(tmin=block_time, tmax=keys[i + 1], include_tmax=False)]
    return raw_blocks


def create_raw_plots(raw):
    raw_blocks = crop_data(raw)
    plt.ioff()
    fig, axs = plt.subplots(len(raw_blocks), 3, sharex='all', sharey='all')
    fig.supxlabel('time(ms)')
    fig.supylabel('Amp(Hz)')

    t_min = -0.2
    t_max = 0.5
    t = np.linspace(t_min, t_max, 176) # todo change 176
    for i, raw_key in enumerate(raw_blocks.keys()):
        events = mne.find_events(raw_blocks[raw_key][1])
        epochs = mne.Epochs(raw, events, tmin=t_min, tmax=t_max, on_missing='raise', baseline=None)
        evokeds = {Marker.Marker(int(stim)).name: epochs[stim].average() for stim in epochs.event_id.keys()}
        curr_target = 'Target 1' if raw_blocks[raw_key][0] == 92 else 'Target 2'

        #lets plot
        plot_compare_evokeds(evokeds, combine='mean', title=f'Block No.{i+1}.\nCurrent Target: {curr_target}')

        for j, stim_key in enumerate(evokeds.keys()):
            ax = axs[j][i]
            y = evokeds[stim_key].get_data().mean(axis=0)
            ax.plot(t, y)
            ax.axvline(x=0, color='k')
            if j == 0:
                ax.set_title(f'Block No.{i+1}, Current Target{curr_target}.\nStim Type: {stim_key}.', fontsize=10)
            else:
                ax.set_title(f'Stim Type:{stim_key}', fontsize=10)
    return fig


def create_and_save_fig(rec_folder_name):
    plt.ioff()
    raw, rec_params = load_raw(rec_folder_name)
    raw = preprocess(raw)
    # raw.info['bads'] = bad_electrodes  # todo
    fig_path = create_figures_folder(rec_folder_name)

    fig_raw_class = create_raw_plots(raw)
    fig_raw_class.savefig(os.path.join(fig_path, "raw.png"))


def create_figures_folder(rec_folder_name):
    rec_folder_path = os.path.join(RECORDINGS_DIR, rec_folder_name)
    fig_path = os.path.join(rec_folder_path, "figures")
    Path(fig_path).mkdir(exist_ok=True)
    return fig_path


def create_raw_fig(raw):
    events = mne.find_events(raw)
    # event_dict = {marker.name: marker.value for marker in Marker}
    fig = mne.viz.plot_raw(raw, events=events, clipping=None, show=False, event_id={"non_target": 1, "target": 9},
                           show_scrollbars=False, start=10)
    return fig


def create_psd_fig(raw):
    fig = mne.viz.plot_raw_psd(raw, fmin=FREQ_RANGE[0], fmax=FREQ_RANGE[1], show=False)
    # raw.plot_psd()
    return fig

# if __name__ == "__main__":