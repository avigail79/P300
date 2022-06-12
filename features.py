import mne
from get_figures import crop_data
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score


def concatenate_matrix(raw, new_sampling):
    n_channel = 13
    raw = raw.resample(new_sampling)
    [raw_blocks, fs] = crop_data(raw)

    t_min = 0.2
    t_max = 0.5
    tspan = int((t_max-t_min) * fs + 1)  # todo 1 because its the size after resampling

    n_blocks = len(raw_blocks)
    evokeds_target = np.zeros((n_blocks, tspan*n_channel))
    evokeds_non_target = np.zeros((n_blocks, tspan*n_channel))

    for i, raw_blk in enumerate(raw_blocks.keys()):
        events = mne.find_events(raw_blocks[raw_blk][1])
        epochs = mne.Epochs(raw_blocks[raw_blk][1], events, tmin=t_min, tmax=t_max, picks='data', on_missing='raise',
                            baseline=None)
        # classify by the target type
        if raw_blocks[raw_blk][0] == 92:
            evokeds_non_target[i] = epochs['3'].average().get_data().reshape((1, tspan*n_channel)) * 10e3
            evokeds_target[i] = epochs['2'].average().get_data().reshape((1, tspan*n_channel)) * 10e3
        elif raw_blocks[raw_blk][0] == 93:
            evokeds_non_target[i] = epochs['2'].average().get_data().reshape((1, tspan * n_channel)) * 10e3
            evokeds_target[i] = epochs['3'].average().get_data().reshape((1, tspan * n_channel)) * 10e3

    concatenate_matrix = np.concatenate((evokeds_non_target, evokeds_target), axis=0)
    target_vec = [0]*n_blocks + [1]*n_blocks
    return concatenate_matrix, target_vec


def clf(raw):
    raw_sampling = 60
    [c_matrix, target_vec] = concatenate_matrix(raw, raw_sampling)
    clf = cross_val_score(LinearDiscriminantAnalysis(), c_matrix, target_vec, cv=5)
    return clf
