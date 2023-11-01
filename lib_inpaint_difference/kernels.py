from enum import Enum

import numpy as np


class AllowedKernels(Enum):
    DISABLED = ('Disabled', None)
    BLUR = ('Blur', np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1],
    ]) / 16)
    SHARPEN = ('Sharpen', np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0],
    ]))


AllowedKernels.item_map = {
    kernel_item.value[0]: kernel_item.value[1]
    for kernel_item in list(AllowedKernels)
}


ALLOWED_KERNEL_OPTIONS = [kernel_item.value[0] for kernel_item in list(AllowedKernels)]
