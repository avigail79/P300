import math
import mne
import itertools
from get_figures import crop_data
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from constants import CHAN
from sklearn.model_selection import GridSearchCV
from typing import List, Dict, Union, Callable, Set, Any, Optional, Tuple
from data_utils import load_raw, log_data, json_save
from preprocessing import preprocess
from pipeline import RESAMPLE_FREQ


def raw_to_train_data(raw, chosen_electrode: List, resample_freq=RESAMPLE_FREQ) -> tuple[np.ndarray, np.ndarray]:
    """
    create concatenate matrix of the chosen channel
    :param raw: eeg data, mne instance
    :param resample_freq:
    :param chosen_electrode:
    :return: x_trian, Y_train
    """
    [raw_blocks, fs] = crop_data(raw)

    t_min_trial, t_min_epoch, t_max = -0.2, 0.2, 0.5
    tspan = int((t_max-t_min_epoch) * fs + 1)  # todo 1 because its the size after resampling
    method = 'mean'

    n_blocks = len(raw_blocks)
    time_channel = math.floor(tspan * resample_freq / fs) * len(chosen_electrode)
    ERPtarget = np.zeros((n_blocks, time_channel))
    ERPnon_target = np.zeros((n_blocks, time_channel))

    for i, raw_blk in enumerate(raw_blocks.keys()):
        events = mne.find_events(raw_blocks[raw_blk][1])
        epochs_after_stim = mne.Epochs(raw_blocks[raw_blk][1], events, tmin=t_min_trial, tmax=t_max, picks=chosen_electrode, on_missing='raise', baseline=(-0.2, 0))
        epochs_after_stim = epochs_after_stim.load_data().crop(tmin=t_min_epoch, include_tmax=True)

        # classify by the target type - create ERP - mean of all the trials
        if raw_blocks[raw_blk][0] == 92:
            ERPnon_target[i] = epochs_after_stim['3'].average(method=method).resample(resample_freq).get_data().reshape((1, time_channel)) * 10e3
            ERPtarget[i] = epochs_after_stim['2'].average(method=method).resample(resample_freq).get_data().reshape((1, time_channel)) * 10e3
        elif raw_blocks[raw_blk][0] == 93:
            ERPnon_target[i] = epochs_after_stim['2'].average(method=method).resample(resample_freq).get_data().reshape((1, time_channel)) * 10e3
            ERPtarget[i] = epochs_after_stim['3'].average(method=method).resample(resample_freq).get_data().reshape((1, time_channel)) * 10e3

    concatenate_mat = np.concatenate((ERPnon_target, ERPtarget), axis=0)
    target_vec = [0]*n_blocks + [1]*n_blocks
    return concatenate_mat, np.array(target_vec)


# def clf(raw, resample_freq):
#     [c_matrix, target_vec] = raw_to_train_data(raw, resample_freq, )
#     clf = cross_val_score(LinearDiscriminantAnalysis(), c_matrix, target_vec, cv=5)
#     clf_svm = cross_val_score(SVC(), c_matrix, target_vec, cv=5)
#     return clf_svm


# def select_best_model(results: List[Dict]) -> Dict:
#     """
#     Some heuristics to select a single model to use
#     :param results: list of dictionaries of type result search. They must have accuracy, and channel
#     :return: dictionary of the final best result
#     """
#     # filter by max accuracy
#     max_acc = max(res['accuracy'] for res in results)
#     filtered_results = list(filter(lambda res: res['accuracy'] == max_acc, results))
#     if len(filtered_results) == 1:
#         return filtered_results[0]
#     # filter by minimum amount of channels used
#     min_chan_amount = min(len(res['channels']) for res in filtered_results)
#     filtered_results = list(filter(lambda res: len(res['channels']) == min_chan_amount, results))
#     if len(filtered_results) == 1:
#         return filtered_results[0]
#     return filtered_results[-1]
#
#
# def svm_hp_search(raw, resample_freq) -> Dict:
#     """
#     Hyper parameter search for svm
#     :param train_data: final eeg training data with shape: #trial, #classes, sample
#     :param train_labels: list of labels for each trial
#     :return: dictionary with the best accuracy and parameters
#     """
#     x_train, y_train = raw_to_train_data(raw, resample_freq, )
#     params_ops = [{'kernel': ['rbf', 'sigmoid'],
#                    'C': [0.5, 0.75, 1, 1.25, 1.5],
#                    'shrinking': [True, False]
#                    },
#                   {'kernel': ['poly'],
#                    'C': [0.75, 1, 1.25],
#                    'degree': [2, 3, 4],
#                    'shrinking': [True, False]
#                    },
#                   ]
#     return grid_search_multiple_params(params_ops, x_train, y_train)
#
#
# def grid_search_multiple_params(params_lst: List, x_train: np.ndarray, y_train: np.ndarray):
#     """
#     Activate grid search on a list of multiple parameters options
#     :param params_lst: list of dictionaries for grid search
#     :param concatenate_matrix: x_train and answer
#     :return: a dictionary with the best accuracy, parameters and name
#     """
#     best_acc = 0
#     best_params = None
#     for curr_params in params_lst:
#         gs = GridSearchCV(SVC(), curr_params)
#         gs.fit(x_train, y_train)
#         if gs.best_score_ > best_acc:
#             best_acc = gs.best_score_
#             best_params = gs.best_params_
#
#     return {'name': 'SVM',
#             'accuracy': best_acc,
#             'parameters': best_params
#             }


# def mean_channel_search(channels_comb: Set, processed_raw: np.ndarray,
#                         training_labels: Union[np.ndarray, List]) -> Dict:
#     """
#     Do channel parameter search using a mean on all channels
#     :param channels_comb: set of combinations of all channels
#     :param processed_eeg: the processed eeg with shape: #trial, #classes, #channels, sample
#     :param training_labels: list of training labels with len: #trials
#     :return: A dictionary of the results of the best selected model, with keys: accuracy, parameters, channels
#     """
#     filtered_data = [processed_raw.get_data() for curr_chans in channels_comb]
#     search_func = partial(svm_hp_search, train_labels=training_labels)
#     search_res = channel_search_general(list(channels_comb), mean_channels,
#                                         filtered_data, search_func)
#     return search_res


def grid_search_svm(preprocess_raw, resample_freq):
    # create channels combination search
    chan_list = [ch for i in CHAN.values() for ch in i]
    chan_comb = [list(itertools.combinations(chan_list, i)) for i in range(1, len(chan_list))]
    channels_comb = set([y for x in chan_comb for y in x])

    # create data to use the classifier
    best_acc = 0
    best_params = None
    best_comb = ()
    params_ops = [{'kernel': ['rbf', 'sigmoid'],
                   'C': [0.5, 0.75, 1, 1.25, 1.5],
                   'shrinking': [True, False]
                   },
                  {'kernel': ['poly'],
                   'C': [0.75, 1, 1.25],
                   'degree': [2, 3, 4],
                   'shrinking': [True, False]
                   },
                  ]
    for curr_params in params_ops:
        for comb in channels_comb:
            x_train, y_train = raw_to_train_data(preprocess_raw, resample_freq, list(comb))
            gs = GridSearchCV(SVC(), curr_params)  # TODO: insert here more params
            gs.fit(x_train, y_train)
            if gs.best_score_ > best_acc:
                best_acc = gs.best_score_
                best_params = gs.best_params_
                best_comb = comb
            # log_data('results: ', best_acc, best_params)

    return {'name': 'SVM',
            'accuracy': best_acc,
            'parameters': best_params,
            'channels': best_comb}







    # Do channels search with hp search
    # channel_func_mode = [(mean_channel_search, 'mean'), (concat_channel_search, 'concat')]




# def main_search(raw, models_folder: Optional[str] = None, search_channels=True):
#     """
#     This function preforms hyperparameter and channel search (if selected) creates the best model and saves it to the
#     folder received in folder_path
#     :param raw: resample and preprocess data
#     :param models_folder: folder for saving the model - if None model will be saved in folder_path
#     :param search_channels: True if channel search is also wanted
#     :return final model
#     """
#     if search_channels:
#         log_data('Doing channels search')
#         # final_result = channels_search(preprocessed_raw, training_labels) todo!
#     else:
#         log_data('Skipping channels search')
#         final_result = None
#
#     log_data('Final Results:', final_result)
#     # final_model = final_model_train(processed_raw, training_labels, final_result)
#
#     return final_model






