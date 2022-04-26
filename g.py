import params
from Marker import Marker
import mne
from params import *

def get_epochs(raw, markers, on_missing='raise'):
    # duration_block = session_set * StimOnset * interTime
    reject_criteria = dict(eeg=100e-6)  # 100 µV
    flat_criteria = dict(eeg=1e-6)  # 1 µV

    events = mne.find_events(raw)
    epochs = mne.Epochs(raw, events, markers, picks="data",
                        on_missing=on_missing, baseline=None, flat=flat_criteria)
    # running get data triggers dropping of epochs, we want to make sure this happens now so that the labels are
    # consistent with the epochs
    print(epochs.drop_log)
    epochs.get_data()
    labels = epochs.events[:, -1]
    return epochs, labels


# def get_epochs(raws, trial_duration, calibration_duration,markers=[Marker.NON_TARGET, Marker.TARGET_1, Marker.TARGET_2],
#                reject_bad=False,
#                on_missing='raise'):
#     reject_criteria = dict(eeg=100e-6)  # 100 µV
#     flat_criteria = dict(eeg=1e-6)  # 1 µV
#
#     epochs_list = []
#     for raw in raws:
#         events = mne.find_events(raw)
#
#         epochs = mne.Epochs(raw, events, markers, tmin=-calibration_duration, tmax=trial_duration, picks="data",
#                             on_missing=on_missing, baseline=None, reject=reject_criteria, flat=flat_criteria)
#         epochs_list.append(epochs)
#     epochs = mne.concatenate_epochs(epochs_list)
#
#     # running get data triggers dropping of epochs, we want to make sure this happens now so that the labels are
#     # consistent with the epochs
#     epochs.get_data()
#     labels = epochs.events[:, -1]
#     print(f'Found {len(labels)} epochs')
#
#     return epochs, labels