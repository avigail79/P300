from use_data import load_raw
from preprocessing import preprocess
import matplotlib.pyplot as plt
import os
import mne
from g import get_epochs
from constants import RECORDINGS_DIR
from pathlib import Path


FREQ_RANGE = (6, 30)

def create_and_save_fig(rec_folder_name):
    plt.ioff()
    raw, rec_params = load_raw(rec_folder_name)
    raw = preprocess(raw)
    # raw.info['bads'] = bad_electrodes  # todo: think and ask about

    fig_path = create_figures_folder(rec_folder_name)
    #
    # fig_raw = create_raw_fig(raw)
    # fig_raw.savefig(os.path.join(fig_path, "raw.png"))
    #
    # fig_psd = create_psd_fig(raw)
    # fig_psd.savefig(os.path.join(fig_path, "psd.png"))

    event = mne.find_events(raw)
    epochs, labels = get_epochs(raw, markers=[1, 9])
    # epochs = mne.preprocessing.compute_current_source_density(epochs)  # ask about

    # type_fig = create_raw_by_type(raw, epochs)


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


def create_raw_by_type(raw):
    events = mne.find_events(raw)
    epochs = mne.Epochs(raw, events, event_id=[1], tmin=-0.1, tmax=0.3)
    epochs = epochs.get_data()  # shape(epochs_n, chn_n, samples_n)
    epochs_m = epochs.mean(axis=1) # means on the channels
    # fig, axs = plt.subplots(epochs_m.shape[0], 1)
    # time_to_show= 0.4 * raw.info['sfreq']
    time = list(range(epochs_m.shape[1]))

    for i in range(epochs_m.shape[0]):
        ax = axs[i]
        ax.set_xlabel('Time [sec]')
        ax.set_ylabel('AMP [mv]')  # ask??
        ax.plot(epochs_m[i,:], time)
    return epochs
    # cls_epochs = epochs[9].squeeze(axis=1)


if __name__ == "__main__":
    # create_and_save_fig("2022-04-25--17-39-16_0")
    raw, rec_params = load_raw("2022-04-25--17-39-16_0")
    raw = preprocess(raw)
    print(create_raw_by_type(raw))