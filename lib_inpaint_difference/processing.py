import cv2

import numpy as np
from PIL import Image

from lib_inpaint_difference.globals import DifferenceGlobals


def compute_mask(
        base_img,
        altered_img,
        dilation_amount,
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
    mask = uncolorize(mask)
    mask = saturate(mask)
    mask = dilate(mask, dilation_amount)

    mask_pil = Image.fromarray(mask, mode=DifferenceGlobals.base_image.mode)
    DifferenceGlobals.generated_mask = mask_pil
    return mask_pil


def compute_diff(base, altered):
    return np.where(base > altered, base - altered, altered - base)


def uncolorize(mask):
    r = mask[:, :, 0]
    g = mask[:, :, 1]
    b = mask[:, :, 2]
    average = (r // 3 + g // 3 + b // 3) + ((r % 3 + g % 3 + b % 3) // 3)
    return np.repeat(average[:, :, np.newaxis], repeats=3, axis=2)


def saturate(mask):
    return (np.where(mask == 0, 0, 255)).astype(np.uint8)


def dilate(mask, dilation_amount):
    if dilation_amount == 0:
        return mask

    b, g, r = cv2.split(mask)

    kernel = np.ones((3, 3), np.uint8)

    dilated_b = cv2.dilate(b, kernel, iterations=dilation_amount)
    dilated_g = cv2.dilate(g, kernel, iterations=dilation_amount)
    dilated_r = cv2.dilate(r, kernel, iterations=dilation_amount)

    return np.stack((dilated_r, dilated_g, dilated_b), axis=-1).astype(np.int8)
