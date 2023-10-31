import inspect

import gradio as gr

from modules.shared import opts
from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.processing import compute_mask


def create_inpaint_automask_tab():
    with gr.TabItem('Inpaint difference', id='inpaint_automask', elem_id="img2img_inpaint_automask_tab") as tab_inpaint_automask:
        with gr.Row():
            with gr.Column():
                automask_inpaint_img = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_automask")
            with gr.Column():
                automask_inpaint_alt = gr.Image(label="Altered image", source="upload", interactive=True, type="pil", elem_id="diff_inpaint_automask")
        automask_inpaint_mask = gr.Image(label="Difference mask", interactive=False, type="pil", elem_id="mask_inpaint_automask", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

        with gr.Row():
            with gr.Column():
                rgb_mask = gr.Checkbox(label='RGB mask')
            with gr.Column():
                saturation = gr.Slider(label='Brightness', maximum=1, step=0.01)
        with gr.Tab(label='Mask convolutions'):
            with gr.Row():
                with gr.Column():
                    gr.Dropdown(label='Kernel type', choices=['Disabled', 'Blur'], value='Disabled')
                with gr.Column():
                    gr.Slider(label='Iterations')
            with gr.Row():
                with gr.Column():
                    gr.Slider(label='Weight')
                    gr.Slider(label='Intersection weight')
                with gr.Column():
                    pass

    params = {
        'fn': compute_mask,
        'inputs': [
            automask_inpaint_img,
            automask_inpaint_alt,
            rgb_mask,
            saturation,
        ],
        'outputs': [automask_inpaint_mask]
    }

    automask_inpaint_img.change(**params)
    automask_inpaint_alt.change(**params)
    rgb_mask.change(**params)
    saturation.release(**params)

    return tab_inpaint_automask


def hijack_gradio_tabs():
    original_gr_tabs = gr.Tabs

    class HijackedGrTabs(gr.Tabs):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __exit__(self, *args, **kwargs):
            if self.elem_id == "mode_img2img":
                tab_automask = create_inpaint_automask_tab()
                DifferenceGlobals.img2img_tab = tab_automask
                append_tabitem_to_img2img_tabs(tab_automask)

            super().__exit__(*args, **kwargs)
            self.__class__ = original_gr_tabs

    gr.Tabs = HijackedGrTabs


def append_tabitem_to_img2img_tabs(tabitem):
    stack = inspect.stack()

    for frame_info in stack:
        code_ctx = frame_info.code_context
        if len(code_ctx) == 0:
            continue

        code_ctx = code_ctx[0]
        if f'elem_id="mode_img2img"' not in code_ctx:
            continue

        f_locals = frame_info.frame.f_locals
        img2img_tabs = f_locals.get('img2img_tabs', None)
        img2img_selected_tab = f_locals.get('img2img_selected_tab', None)

        img2img_tabs.append(tabitem)
        DifferenceGlobals.tab_index = len(img2img_tabs)-1
        tabitem.select(fn=lambda tabnum=DifferenceGlobals.tab_index: tabnum, inputs=[], outputs=[img2img_selected_tab])
        return
