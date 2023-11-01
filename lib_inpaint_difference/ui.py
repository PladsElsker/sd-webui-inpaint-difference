import gradio as gr
from modules.shared import opts

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.processing import compute_mask
from lib_inpaint_difference.kernels import ALLOWED_KERNEL_OPTIONS


def create_inpaint_difference_tab():
    with gr.TabItem('Inpaint difference', id='inpaint_difference', elem_id="img2img_inpaint_difference_tab") as tab_inpaint_automask:
        with gr.Row():
            with gr.Column():
                DifferenceGlobals.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_difference")
            with gr.Column():
                DifferenceGlobals.inpaint_alt_component = gr.Image(label="Altered image", source="upload", interactive=True, type="pil", elem_id="alt_inpaint_difference")
        DifferenceGlobals.inpaint_mask_component = gr.Image(label="Difference mask", interactive=False, type="pil", elem_id="mask_inpaint_difference", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

    return tab_inpaint_automask


def create_inpaint_difference_generation_params_ui():
    with gr.Group(visible=False) as inpaint_difference_ui_params:
        with gr.Tab(label='Inpaint difference parameters'):
            with gr.Row():
                with gr.Column():
                    allow_rgb_mask = gr.Checkbox(label='RGB mask', value=False, elem_id='inpaint_difference_allow_rgb_mask')
                with gr.Column():
                    mask_brightness = gr.Slider(label='Brightness', maximum=1, step=0.01, value=1, elem_id='inpaint_difference_brightness')
            with gr.Tab(label='Mask convolutions'):
                with gr.Row():
                    with gr.Column():
                        conv_kernel_type = gr.Dropdown(label='Kernel type', choices=ALLOWED_KERNEL_OPTIONS, value='Disabled', elem_id='inpaint_difference_kernel_type')
                    with gr.Column():
                        conv_iterations = gr.Slider(label='Iterations', maximum=100, step=1, value=0, elem_id='inpaint_difference_convolution_iterations')
                with gr.Row():
                    with gr.Column():
                        conv_weight = gr.Slider(label='Convolutions weight', maximum=1, step=0.01, value=1, elem_id='inpaint_difference_weight')
                        conv_intersect_weight = gr.Slider(label='Intersection weight', maximum=1, step=0.01, elem_id='inpaint_difference_intersection_weight')
                    with gr.Column():
                        pass

    params = {
        'fn': compute_mask,
        'inputs': [
            DifferenceGlobals.inpaint_img_component,
            DifferenceGlobals.inpaint_alt_component,
            allow_rgb_mask,
            mask_brightness,
            conv_kernel_type,
            conv_iterations,
            conv_weight,
            conv_intersect_weight,
        ],
        'outputs': [DifferenceGlobals.inpaint_mask_component]
    }

    DifferenceGlobals.inpaint_img_component.change(**params)
    DifferenceGlobals.inpaint_alt_component.change(**params)
    allow_rgb_mask.change(**params)
    mask_brightness.release(**params)
    conv_kernel_type.change(**params)
    conv_iterations.release(**params)
    conv_weight.release(**params)
    conv_intersect_weight.release(**params)

    DifferenceGlobals.ui_params = inpaint_difference_ui_params
