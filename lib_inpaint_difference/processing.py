import gradio as gr

import numpy as np
from PIL import Image

from modules import img2img
from lib_inpaint_difference.globals import DifferenceGlobals


def hijack_img2img_processing():
    original_img2img_processing = img2img.img2img

    def hijack_func(id_task: str, mode: int, prompt: str, negative_prompt: str, prompt_styles, init_img, sketch,
            init_img_with_mask, inpaint_color_sketch, inpaint_color_sketch_orig, init_img_inpaint,
            init_mask_inpaint, steps: int, sampler_name: str, mask_blur: int, mask_alpha: float,
            inpainting_fill: int, n_iter: int, batch_size: int, cfg_scale: float, image_cfg_scale: float,
            denoising_strength: float, selected_scale_tab: int, height: int, width: int, scale_by: float,
            resize_mode: int, inpaint_full_res: bool, inpaint_full_res_padding: int,
            inpainting_mask_invert: int, img2img_batch_input_dir: str, img2img_batch_output_dir: str,
            img2img_batch_inpaint_mask_dir: str, override_settings_texts, img2img_batch_use_png_info: bool,
            img2img_batch_png_info_props: list, img2img_batch_png_info_dir: str, request: gr.Request, *args
        ):
        if mode == DifferenceGlobals.tab_index:  # processing with inpaint difference
            mode = 2  # use the inpaint tab for processing
            init_img_with_mask = {
                'image': DifferenceGlobals.altered_image,
                'mask': DifferenceGlobals.generated_mask
            }

        return original_img2img_processing(id_task, mode, prompt, negative_prompt, prompt_styles, init_img, sketch,
            init_img_with_mask, inpaint_color_sketch, inpaint_color_sketch_orig, init_img_inpaint,
            init_mask_inpaint, steps, sampler_name, mask_blur, mask_alpha,
            inpainting_fill, n_iter, batch_size, cfg_scale, image_cfg_scale,
            denoising_strength, selected_scale_tab, height, width, scale_by,
            resize_mode, inpaint_full_res, inpaint_full_res_padding,
            inpainting_mask_invert, img2img_batch_input_dir, img2img_batch_output_dir,
            img2img_batch_inpaint_mask_dir, override_settings_texts, img2img_batch_use_png_info,
            img2img_batch_png_info_props, img2img_batch_png_info_dir, request, *args)

    img2img.img2img = hijack_func


def compute_mask(base_img, altered_img, is_rgb_mask, saturation):
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
