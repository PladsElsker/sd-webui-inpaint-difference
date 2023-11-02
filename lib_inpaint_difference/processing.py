import cv2

import numpy as np
from PIL import Image

from modules.shared import opts

from lib_inpaint_difference.globals import DifferenceGlobals


def compute_mask(
        base_img,
        altered_img,
        dilation_amount,
        show_image_under_mask,
):
    DifferenceGlobals.base_image = base_img
    DifferenceGlobals.altered_image = altered_img

    if DifferenceGlobals.base_image is None or DifferenceGlobals.altered_image is None:
        return None

    base_pil = DifferenceGlobals.base_image
    altered_pil = DifferenceGlobals.altered_image
    same_size = base_pil.size == altered_pil
    if not same_size:
        base_pil = base_pil.resize((altered_pil.width, altered_pil.height))

    base = np.array(base_pil).astype(np.int32)
    altered = np.array(altered_pil).astype(np.int32)

    mask = compute_diff(base, altered)
    mask = uncolorize(mask)
    mask = saturate(mask)
    mask = dilate(mask, dilation_amount)

    mask_pil = Image.fromarray(mask.astype(np.uint8), mode=DifferenceGlobals.base_image.mode)
    DifferenceGlobals.generated_mask = mask_pil

    visual_mask = colorize(mask)
    if show_image_under_mask:
        visual_mask = add_image_under_mask(mask, visual_mask, altered)

    return Image.fromarray(visual_mask.astype(np.uint8), mode=DifferenceGlobals.base_image.mode)


def compute_diff(base, altered):
    return np.abs(base - altered)


def uncolorize(mask):
    b, g, r = cv2.split(mask)
    average = (r + g + b) // 3
    return np.repeat(average[:, :, np.newaxis], repeats=3, axis=2)


def saturate(mask):
    return np.ceil(mask/255) * 255


def dilate(mask, dilation_amount):
    if dilation_amount == 0:
        return mask

    b, g, r = cv2.split(mask)

    kernel = np.ones((3, 3), np.uint8)

    dilated_b = cv2.dilate(b, kernel, iterations=dilation_amount)
    dilated_g = cv2.dilate(g, kernel, iterations=dilation_amount)
    dilated_r = cv2.dilate(r, kernel, iterations=dilation_amount)

    return np.stack((dilated_r, dilated_g, dilated_b), axis=-1)


def colorize(mask):
    color_str = opts.img2img_inpaint_mask_brush_color
    color = np.array([int(color_str[i:i+2], 16)/255 for i in range(1, 7, 2)])
    return mask * color


def add_image_under_mask(original_mask, colorized_mask, altered, t=0.8):
    opacity_mask = (altered*(1-t) + colorized_mask*t)
    return np.where(original_mask == 0, altered, opacity_mask)
