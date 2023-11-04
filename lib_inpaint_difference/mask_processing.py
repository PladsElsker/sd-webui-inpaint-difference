import cv2

import numpy as np
from PIL import Image

from lib_inpaint_difference.globals import DifferenceGlobals


def compute_mask(
        base_img,
        altered_img,
        dilation_amount,
        blur_amount,
):
    DifferenceGlobals.base_image = base_img
    DifferenceGlobals.altered_image = altered_img
    DifferenceGlobals.mask_blur = blur_amount

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

    # mask used for computation by StableDiffusionProcessingImg2Img
    mask_pil = Image.fromarray(mask.astype(np.uint8), mode=DifferenceGlobals.base_image.mode)
    DifferenceGlobals.generated_mask = mask_pil

    # the rest of the calculations are either duplicates of StableDiffusionProcessingImg2Img or visual only
    mask = blur(mask, blur_amount)

    visual_mask = mask
    visual_mask = colorize(visual_mask)
    visual_mask = process_image_under_mask(mask, visual_mask, altered)

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


# similar to how StableDiffusionProcessingImg2Img does it
def blur(mask, blur_amount):
    np_mask = np.array(mask)
    kernel_size = 2 * int(2.5 * blur_amount + 0.5) + 1
    return cv2.GaussianBlur(np_mask, (kernel_size, kernel_size), blur_amount)


def colorize(mask):
    color_str = DifferenceGlobals.mask_brush_color
    color = np.array([int(color_str[i:i+2], 16)/255 for i in range(1, 7, 2)])
    return mask * color


def process_image_under_mask(original_mask, colorized_mask, altered):
    if not DifferenceGlobals.show_image_under_mask:
        return colorized_mask

    normalized_mask = original_mask / 255
    return altered*(1-normalized_mask) + colorized_mask*normalized_mask
