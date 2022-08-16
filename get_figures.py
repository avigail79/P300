import numpy as np
from mne.viz import plot_compare_evokeds
from math import ceil
import Marker
from preprocessing import preprocess, down_sampling
import matplotlib.pyplot as plt
import os
import mne
from constants import RECORDINGS_DIR, CHAN
from pathlib import Path


FREQ_RANGE = (6, 30)


def crop_data(raw):
    """
    The function returns dict. key = start block time, val = [target type, raw].
    """
    fs = raw.info['sfreq']
    events = mne.find_events(raw)
    start_event = [event for event in events if event[2] == 93 or event[2] == 92]
    raw_blocks = {data[0] / raw.info['sfreq']: data[2] for data in start_event}
    start_data_times = list(raw_blocks.keys())
    for i, block_time in enumerate(start_data_times):
        raw_copy = mne.io.Raw.copy(raw)
        if i < (len(start_data_times)-1):
            raw_blocks[block_time] = raw_blocks[block_time], raw_copy.crop(tmin=block_time, tmax=start_data_times[i+1], include_tmax=False)
        else:
            raw_blocks[block_time] = raw_blocks[block_time], raw_copy.crop(tmin=block_time, include_tmax=True)
    return [raw_blocks, fs]


def create_raw_plots(raw_blocks, fs):
    plt.ioff()
    fig, axs = plt.subplots(len(raw_blocks), 3, sharex='all', sharey='all')
    fig.supxlabel('time(ms)')
    fig.supylabel('Amp(Hz)')

    t_min = -0.2
    t_max = 0.5
    t_times = ceil((t_max-t_min) * fs)
    t = np.linspace(t_min, t_max, t_times)
    for i, raw_blk in enumerate(raw_blocks.keys()):
        events = mne.find_events(raw_blocks[raw_blk][1])
        epochs = mne.Epochs(raw_blocks[raw_blk][1], events, tmin=t_min, tmax=t_max, on_missing='raise', baseline=None)
        evokeds = {Marker.Marker(int(stim)).name: epochs[stim].average() for stim in epochs.event_id.keys()}
        curr_target = 'TARGET_1' if raw_blocks[raw_blk][0] == 92 else 'TARGET_2'

        #lets plot
        plot_compare_evokeds(evokeds, combine='mean', title=f'Block No.{i+1}.\nCurrent Target: {curr_target}')

        for j, stim_key in enumerate(evokeds.keys()):
            ax = axs[i][j]
            y = evokeds[stim_key].get_data().mean(axis=0)
            ax.plot(t, y)
            ax.axvline(x=0, color='k')
            if i == 0:
                ax.set_title(f'{stim_key}', fontsize=8)
            if curr_target == stim_key:
                ax.spines["right"].set_color("orange")
                ax.spines["right"].set_linewidth(3)
    return fig


def create_target_plot(raw, resample_freq, resample_flag):
    n_channel = 13
    if resample_flag:
        raw = raw.resample(resample_freq)
    [raw_blocks, fs] = crop_data(raw)

    t_min = -0.2
    t_max = 0.5
    tspan = int((t_max-t_min) * fs + 1)  # todo 1 because its the size after resampling

    evokeds_target = np.zeros((n_channel, tspan))
    evokeds_non_target = np.zeros((n_channel, tspan))

    for i, raw_blk in enumerate(raw_blocks.keys()):
        events = mne.find_events(raw_blocks[raw_blk][1])
        epochs = mne.Epochs(raw_blocks[raw_blk][1], events, tmin=t_min, tmax=t_max, picks='data',on_missing='raise', baseline=None)

        method = 'mean'
        if raw_blocks[raw_blk][0] == 92:
            evokeds_non_target += epochs['3'].average(method=method).get_data() * 10e3
            evokeds_target += epochs['2'].average(method=method).get_data() * 10e3
        elif raw_blocks[raw_blk][0] == 93:
            evokeds_non_target += epochs['2'].average(method=method).get_data() * 10e3
            evokeds_target += epochs['3'].average(method=method).get_data() * 10e3

    j=0
    figures = []
    for ch_type in CHAN.keys():
        fig, axs = plt.subplots(len(CHAN[ch_type]), sharex='all', sharey='all')
        t = np.linspace(t_min, t_max, tspan)
        fig.supxlabel('time(ms)')
        fig.supylabel('mV')
        fig.legend(['target', 'non target'], loc='upper center')
        fig.suptitle(ch_type)
        for c, ch in enumerate(CHAN[ch_type]):
            ax = axs[c]
            ax.plot(t, evokeds_target[j])
            ax.plot(t, evokeds_non_target[j])
            ax.axvline(x=0, color='k')
            ax.set_title(ch, loc='right')
            j += 1
        figures.append(fig)

    return figures


def create_and_save_fig(raw, rec_folder_name, resample_freq, resample_flag):
    plt.ioff()
    raw = preprocess(raw)
    fig_path = create_figures_folder(rec_folder_name)
    # raw_blocks, fs = crop_data(raw)

    # fig_raw_class = create_raw_plots(raw_blocks, fs)
    # fig_raw_class.savefig(os.path.join(fig_path, "raw.png"))

    figures_target = create_target_plot(raw, resample_freq, resample_flag)
    for i, fig in enumerate(figures_target):
        fig.savefig(os.path.join(fig_path, f"target{i}.png"))


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