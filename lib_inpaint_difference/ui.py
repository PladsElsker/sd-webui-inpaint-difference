import gradio as gr
from modules.shared import opts
from modules.ui_components import ToolButton, FormGroup, FormRow

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.context_pack import ParentBlock
from lib_inpaint_difference.mask_processing import compute_mask


def create_inpaint_difference_tab():
    with ParentBlock():
        with gr.TabItem('Inpaint difference', id='inpaint_difference', elem_id="img2img_inpaint_difference_tab") as tab_inpaint_difference:
            with gr.Row():
                DifferenceGlobals.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_difference")
                swap_images = ToolButton('⇆', elem_id='img2img_inpaint_difference_swap_images', tooltip="Swap images.")
                DifferenceGlobals.inpaint_alt_component = gr.Image(label="Altered image", source="upload", interactive=True, type="pil", elem_id="alt_inpaint_difference")

            DifferenceGlobals.inpaint_mask_component = gr.Image(label="Difference mask", interactive=False, type="pil", elem_id="mask_inpaint_difference", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

    def swap_images_func(img, alt):
        DifferenceGlobals.base_image = alt
        DifferenceGlobals.altered_image = img
        return gr.update(value=alt), gr.update(value=img)

    image_components = [DifferenceGlobals.inpaint_img_component, DifferenceGlobals.inpaint_alt_component]
    swap_images.click(swap_images_func, inputs=image_components, outputs=image_components)

    return tab_inpaint_difference


def inject_inpaint_difference_generation_params_ui():
    with ParentBlock():
        with FormGroup(elem_id="inpaint_difference_controls", visible=False) as inpaint_controls:
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

    compute_diff_mask = {
        'fn': compute_mask,
        'inputs': [
            DifferenceGlobals.inpaint_img_component,
            DifferenceGlobals.inpaint_alt_component,
            mask_dilation,
            mask_blur,
        ],
        'outputs': [DifferenceGlobals.inpaint_mask_component]
    }

    DifferenceGlobals.inpaint_img_component.change(**compute_diff_mask)
    DifferenceGlobals.inpaint_alt_component.change(**compute_diff_mask)
    mask_dilation.release(**compute_diff_mask)
    mask_blur.release(**compute_diff_mask)

    DifferenceGlobals.ui_params = inpaint_controls,

    def update_dup_params_fn(inpainting_mask_invert, inpainting_fill, inpaint_full_res, inpaint_full_res_padding):
        DifferenceGlobals.inpainting_mask_invert = inpainting_mask_invert
        DifferenceGlobals.inpainting_fill = inpainting_fill
        DifferenceGlobals.inpaint_full_res = inpaint_full_res
        DifferenceGlobals.inpaint_full_res_padding = inpaint_full_res_padding

    update_dup_params = {
        'fn': update_dup_params_fn,
        'inputs': [
            inpainting_mask_invert,
            inpainting_fill,
            inpaint_full_res,
            inpaint_full_res_padding,
        ],
        'outputs': []
    }

    inpainting_mask_invert.change(**update_dup_params)
    inpainting_fill.change(**update_dup_params)
    inpaint_full_res.change(**update_dup_params)
    inpaint_full_res_padding.change(**update_dup_params)
