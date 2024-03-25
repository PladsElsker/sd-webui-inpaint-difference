import gradio as gr

from modules import img2img, shared

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.one_time_callable import one_time_callable

IS_WEBUI_1_9 = hasattr(shared.cmd_opts, 'unix_filenames_sanitization')

@one_time_callable
def hijack_img2img_processing_before_1_9():
    original_img2img_processing = img2img.img2img

    def hijack_func(id_task: str, mode: int, prompt: str, negative_prompt: str, prompt_styles, init_img, sketch,
            init_img_with_mask, inpaint_color_sketch, inpaint_color_sketch_orig, init_img_inpaint,
            init_mask_inpaint, steps: int, sampler_name: str, mask_blur: int, mask_alpha: float,
            inpainting_fill: int, n_iter: int, batch_size: int, cfg_scale: float, image_cfg_scale: float,
            denoising_strength: float, selected_scale_tab: int, height: int, width: int, scale_by: float,
            resize_mode: int, inpaint_full_res: bool, inpaint_full_res_padding: int,
            inpainting_mask_invert: int, img2img_batch_input_dir: str, img2img_batch_output_dir: str,
            img2img_batch_inpaint_mask_dir: str, override_settings_texts, img2img_batch_use_png_info: bool,
            img2img_batch_png_info_props: list, img2img_batch_png_info_dir: str, request: gr.Request, *args,
    ):
        if mode == DifferenceGlobals.tab_index:
            mode = 2  # use the "inpaint" operation mode for processing
            init_img_with_mask = {
                'image': DifferenceGlobals.altered_image,
                'mask': DifferenceGlobals.generated_mask,
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



MODE_IDX = 0
INIT_IMG_WITH_MASK_IDX = 6

@one_time_callable
def hijack_img2img_processing():
    original_img2img_processing = img2img.img2img

    def hijack_func(id_task: str, request: gr.Request, *args):
        args = list(args)
        if args[MODE_IDX] == DifferenceGlobals.tab_index:
            args[MODE_IDX] = 2  # use the "inpaint" operation mode for processing
            args[INIT_IMG_WITH_MASK_IDX] = {
                'image': DifferenceGlobals.altered_image,
                'mask': DifferenceGlobals.generated_mask,
            }
        return original_img2img_processing(id_task, request, *args)

    img2img.img2img = hijack_func


if not IS_WEBUI_1_9:
    hijack_img2img_processing = hijack_img2img_processing_before_1_9

