import gradio as gr
from modules.shared import opts
from modules.ui_components import ToolButton, FormRow

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.mask_processing import compute_mask


def create_inpaint_difference_ui(tab_manager, ui_params_manager):
    with tab_manager:
        # create the ui for the tab here
        with gr.Row():
            DifferenceGlobals.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_difference")
            swap_images = ToolButton('⇆', elem_id='img2img_inpaint_difference_swap_images', tooltip="Swap images.")
            DifferenceGlobals.inpaint_alt_component = gr.Image(label="Altered image", source="upload", interactive=True, type="pil", elem_id="alt_inpaint_difference")

        DifferenceGlobals.inpaint_mask_component = gr.Image(label="Difference mask", interactive=False, type="pil", elem_id="mask_inpaint_difference", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

    with ui_params_manager:
        # create the ui for the options that will appear under the tab when it is selected
        with FormRow():
            mask_blur = gr.Slider(label='Mask blur', minimum=0, maximum=64, step=1, value=4, elem_id="inpaint_difference_mask_blur")
            mask_dilation = gr.Slider(label='Mask dilation', maximum=100, step=1, value=0, elem_id='inpaint_difference_mask_dilation')

        with FormRow():
            inpainting_mask_invert = gr.Radio(label='Mask mode', choices=['Inpaint masked', 'Inpaint not masked'], value='Inpaint masked', type="index", elem_id="inpaint_difference_mask_mode")

        with FormRow():
            inpainting_fill = gr.Radio(label='Masked content', choices=['fill', 'original', 'latent noise', 'latent nothing'], value='original', type="index", elem_id="inpaint_difference_inpainting_fill")

        with FormRow():
            with gr.Column():
                inpaint_full_res = gr.Radio(label="Inpaint area", choices=["Whole picture", "Only masked"], type="index", value="Whole picture", elem_id="inpaint_difference_inpaint_full_res")

            with gr.Column(scale=4):
                inpaint_full_res_padding = gr.Slider(label='Only masked padding, pixels', minimum=0, maximum=256, step=4, value=32, elem_id="inpaint_difference_inpaint_full_res_padding")

        compute_mask_dict = {
            'fn': compute_mask,
            'inputs': [
                DifferenceGlobals.inpaint_img_component,
                DifferenceGlobals.inpaint_alt_component,
                mask_blur,
                mask_dilation,
            ],
            'outputs': [DifferenceGlobals.inpaint_mask_component]
        }

        DifferenceGlobals.inpaint_img_component.upload(**compute_mask_dict)
        DifferenceGlobals.inpaint_img_component.clear(**compute_mask_dict)
        DifferenceGlobals.inpaint_alt_component.upload(**compute_mask_dict)
        DifferenceGlobals.inpaint_alt_component.clear(**compute_mask_dict)
        mask_blur.release(**compute_mask_dict)
        mask_dilation.release(**compute_mask_dict)

    def swap_images_func(img, alt, blur_amount, dilation_amount):
        visual_mask = compute_mask(alt, img, blur_amount, dilation_amount)
        DifferenceGlobals.base_image = alt
        DifferenceGlobals.altered_image = img
        return gr.update(value=alt), gr.update(value=img), gr.update(value=visual_mask)

    swap_images.click(
        fn=swap_images_func,
        inputs=compute_mask_dict['inputs'],
        outputs=[
            DifferenceGlobals.inpaint_img_component,
            DifferenceGlobals.inpaint_alt_component,
            DifferenceGlobals.inpaint_mask_component,
        ]
    )

    def update_ui_params_globals(mask_blur, mask_dilation, inpainting_mask_invert, inpainting_fill, inpaint_full_res, inpaint_full_res_padding):
        DifferenceGlobals.mask_blur = mask_blur
        DifferenceGlobals.mask_dilation = mask_dilation
        DifferenceGlobals.inpainting_mask_invert = inpainting_mask_invert
        DifferenceGlobals.inpainting_fill = inpainting_fill
        DifferenceGlobals.inpaint_full_res = inpaint_full_res
        DifferenceGlobals.inpaint_full_res_padding = inpaint_full_res_padding

    update_custom_ui_globals_dict = {
        'fn': update_ui_params_globals,
        'inputs': [mask_blur, mask_dilation, inpainting_mask_invert, inpainting_fill, inpaint_full_res, inpaint_full_res_padding],
        'outputs': []
    }

    tab_manager.block.select(**update_custom_ui_globals_dict)
    mask_blur.release(**update_custom_ui_globals_dict)
    mask_dilation.release(**update_custom_ui_globals_dict)
    inpainting_mask_invert.change(**update_custom_ui_globals_dict)
    inpainting_fill.change(**update_custom_ui_globals_dict)
    inpaint_full_res.change(**update_custom_ui_globals_dict)
    inpaint_full_res_padding.release(**update_custom_ui_globals_dict)
