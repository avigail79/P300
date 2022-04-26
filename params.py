import random
import math
from Marker import Marker

GUI = {"use_synthetic": True,
       "subject name": '0',
       "blocks_N": 3,
       "trials_N": 7,
       "stimulus Type": 'black_shapes',
       "odd percent": 0.2  # include the target and non-target
       }

session_params = {
    "get ready duration": 5,
    "calibration duration": 1,
    "StimOnset": 0.3,  # time to present the stimulus
    "interTime": 0.15,  # time between stimulus
}


def create_session_set(blocks_N, trials_N, odd_percent):
    """
    classes of stim:
    1- high freq non-target
    2- low freq 1
    3- low freq 2
    :return list,list
    """

    # block set - list of num
    def create_block(trials_N):
        low_freq_stim_N = math.floor(odd_percent * trials_N)
        block_set = [1] * (trials_N - low_freq_stim_N) + [2] * low_freq_stim_N + [3] * low_freq_stim_N
        random.shuffle(block_set)
        return block_set

    # target set - list of num
    target_set = [random.choice([2, 3]) for i in range(blocks_N)]
    # this loop check that the targets is different
    if all(map(lambda x: x == target_set[0], target_set)):
        if target_set[0] == 2:
            target_set[0] = 3
        else:
            target_set[0] = 2

    # session
    session_set_by_class = [create_block(trials_N) for i in range(blocks_N)]
    # session_set_by_target = [create_block(trials_N) for i in range(blocks_N)]
    # for i, block in enumerate(session_set_by_target):
    #     if target_set[i] == 2:
    #         block = list(map(lambda x: x.replace("2", "9"), block))
    #         block = list(map(lambda x: x.replace("3", "1"), block))
    #         session_set_by_target[i] = block
    #     else:
    #         block = list(map(lambda x: x.replace("3", "9"), block))
    #         block = list(map(lambda x: x.replace("2", "1"), block))
    #         session_set_by_target[i] = block
    #
    # session_set = {"session_set_by_class": session_set_by_class,
    #                "session_set_by_target": session_set_by_target,
    #                "target_set": target_set
    #                }
    return session_set_by_class, target_set


# black_shapes = {
#     "1": "black circle",
#     "2": "black square",
#     "3": "black triangle"
# }

black_shapes = {
    "NON_TARGET": ["black circle", 11],
    "TARGET_1": ["black square", 1],
    "TARGET_2": ["black triangle", 2]
}

# rec_params = {
#         "calibration_duration": 1,
#         "StimOnset": 0.3,  # time to present the stimulus
#         "interTime": 0.15,  # time between stimulus
#         "blocks_N": 3,
#         "trials_N": 7,  # trials per block without targets!!
#         "odd_percent": 0.2
#     }

# def total_rec_params():
#     # recording params
#     GUI = {"use_synthetic": True,
#            "subject name": 'Avigail',
#            "get ready duration": 5,
#            "calibration duration": 1,
#            "StimOnset": 0.3,  # time to present the stimulus
#            "interTime": 0.15,  # time between stimulus
#            "blocks_N": 3,
#            "trials_N": 7,
#            }
#
#     rec_params = {
#         # "use_synthetic": True,
#         # "subject_name": 'Avigail',
#         # "get_ready_duration": 5,
#         "calibration_duration": 1,
#         "StimOnset": 0.3,  # time to present the stimulus
#         "interTime": 0.15,  # time between stimulus
#         "blocks_N": 3,
#         "trials_N": 7,  # trials per block without targets!!
#         "odd_percent": 0.2
#     }

# update experiment params
# targets_N = math.floor(rec_params["trials_N"] * rec_params["odd_percent"])
# session_set = create_session_set(rec_params["blocks_N"], rec_params["trials_N"], targets_N)
# target_set = create_target_set(rec_params["blocks_N"])
# rec_params.update({"targets_N": targets_N, "session_set": session_set, "target_set": target_set})
# return rec_params

#
# def create_session_set(blocks_N, trials_N, targets_N):
#     session_set = [[Marker.NON_TARGET.value] * trials_N + Marker.all_target_stim() * targets_N for i in range(blocks_N)]
#     [random.shuffle(session_set[i]) for i in range(blocks_N)]
#     return session_set


# def create_target_set(blocks_N):
#     target_stims = Marker.all_target_stim_names()
#     target_set = [random.choice(target_stims) for i in range(blocks_N)]
#     if all(marker == target_set[0] for marker in target_set):
#         if target_set[0] == target_stims[0]:
#             target_set[0] = target_stims[1]
#         else:
#             target_set[0] = target_stims[0]
#     # target_set_name = [stims_dict[stm][0] for stm in target_set_marker]
#     return target_set


# target_set = [random.choice(Marker.all_target_stim_names()) for i in range(params.blocks_N)]
# stimulusType = (type of stimulus to load and present- different pictures\ audio \ etc.)


# shapes params
# blue_shapes = {
#     "NON_TARGET": ["circle", 11],
#     "TARGET_1": ["square", 1],
#     "TARGET_2": ["triangular", 2]
# }




# images
# Target_i = load("./image/circle.png")
# non_tagert =

if __name__ == "__main__":
    session_set_by_num, session_set_by_target, target_set = create_session_set(GUI['blocks_N'], GUI['trials_N'],
                                                                               GUI['odd percent'])
