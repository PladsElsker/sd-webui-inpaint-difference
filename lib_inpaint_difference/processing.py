import gradio as gr

import numpy as np
from PIL import Image
from scipy.signal import convolve2d

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.kernels import AllowedKernels


def compute_mask(
        base_img,
        altered_img,
        is_rgb_mask,
        saturation,
        conv_kernel_type,
        iterations,
        conv_weight,
        conv_intersect_weight
):
    DifferenceGlobals.base_image = base_img
    DifferenceGlobals.altered_image = altered_img

    if DifferenceGlobals.base_image is None or DifferenceGlobals.altered_image is None:
        return None

    same_size = DifferenceGlobals.base_image.size == DifferenceGlobals.altered_image.size

    base_pil = DifferenceGlobals.base_image if same_size else DifferenceGlobals.base_image.resize((DifferenceGlobals.altered_image.width, DifferenceGlobals.altered_image.height))
    altered_pil = DifferenceGlobals.altered_image

    base = np.array(base_pil)
    altered = np.array(altered_pil)

    mask = compute_diff(base, altered)
    mask = handle_rgb_uncolorization(mask, is_rgb_mask)
    mask = compute_staturation(mask, saturation)
    mask = apply_convolutions(mask, conv_kernel_type, iterations, conv_weight, conv_intersect_weight)

    mask_pil = Image.fromarray(mask, mode=DifferenceGlobals.base_image.mode)
    DifferenceGlobals.generated_mask = mask_pil
    return mask_pil


def compute_diff(base, altered):
    return np.where(base > altered, base - altered, altered - base)


def handle_rgb_uncolorization(mask, is_rgb_mask):
    if is_rgb_mask:
        return mask

    r = mask[:, :, 0]
    g = mask[:, :, 1]
    b = mask[:, :, 2]
    average = (r // 3 + g // 3 + b // 3) + ((r % 3 + g % 3 + b % 3) // 3)
    return np.repeat(average[:, :, np.newaxis], repeats=3, axis=2)


def compute_staturation(mask, saturation):
    clamped = np.where(mask == 0, 0, 255)
    return (mask*(1-saturation) + clamped*saturation).astype(np.uint8)


def apply_convolutions(mask, conv_kernel_type, iterations, conv_weight, conv_intersect_weight):
    if iterations == 0:
        return mask

    kernel = AllowedKernels.item_map[conv_kernel_type]
    if kernel is None:
        return mask

    mask_before = mask

    mask_r = mask[:, :, 0]
    mask_g = mask[:, :, 1]
    mask_b = mask[:, :, 2]
    for _ in range(iterations):
        mask_r = convolve2d(mask_r, kernel, mode='same')
        mask_g = convolve2d(mask_g, kernel, mode='same')
        mask_b = convolve2d(mask_b, kernel, mode='same')

    mask = np.stack((mask_r, mask_g, mask_b), axis=-1)

    cropped_conv = np.where(mask_before == 0, mask, mask_before)

    mask = cropped_conv*conv_intersect_weight + mask*(1-conv_intersect_weight)
    mask = mask*conv_weight + mask_before*(1-conv_weight)

    return mask.astype(np.uint8)
