from enum import IntEnum, unique
from constants import IMAGES_DIR
import os


@unique
class Marker(IntEnum):
    NON_TARGET = 1
    TARGET_1 = 2
    TARGET_2 = 3
    start_with_target_1 = 92
    start_with_target_2 = 93

    # @property
    # def image_path(self):
    #     return os.path.join(IMAGES_DIR, f"{self.name}.png")

    # @property
    # def shape(self):

    # @classmethod
    # def all(cls):
    #     return [stim.value for stim in cls]
    #
    # @classmethod
    # def all_target_stim(cls):
    #     return [stim.value for stim in cls if (stim.name == "TARGET_1" or stim.name == "TARGET_2")]
    #
    # @classmethod
    # def all_target_stim_names(cls):
    #     return [stim.name for stim in cls if (stim.name == "TARGET_1" or stim.name == "TARGET_2")]


# if __name__ == "__main__":
