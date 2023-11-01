from enum import Enum

import numpy as np


class AllowedKernels(Enum):
    DISABLED = ('Disabled', None)
    BLUR = ('Blur', np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1],
    ]) / 16)


AllowedKernels.item_map = {
    kernel_item.value[0]: kernel_item.value[1]
    for kernel_item in list(AllowedKernels)
}


ALLOWED_KERNEL_OPTIONS = [kernel_item.value[0] for kernel_item in list(AllowedKernels)]
