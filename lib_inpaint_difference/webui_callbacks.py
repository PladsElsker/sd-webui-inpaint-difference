import gradio as gr

from modules.scripts import script_callbacks

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.settings import create_settings_section
from lib_inpaint_difference.ui import create_inpaint_difference_ui
from lib_inpaint_difference.context_pack import BlockManager
from lib_inpaint_difference.webui_nasty_hijacks import (
    grab_img2img_tabs_block,
    grab_ui_params_blocks,
    register_tab_index,
)


def on_after_component(_, **kwargs):
    if not DifferenceGlobals.is_extension_enabled:
        return

    elem_id = kwargs.get('elem_id', None)

    if elem_id == 'img2img_batch_inpaint_mask_dir':
        grab_img2img_tabs_block()

    if elem_id == 'img2img_mask_blur':
        grab_ui_params_blocks()

        register_tab_index()

        with BlockManager(DifferenceGlobals.registered_blocks['img2img_tabs']):
            tab = gr.TabItem('Inpaint difference', id='inpaint_difference', elem_id="img2img_inpaint_difference_tab")
        with BlockManager(DifferenceGlobals.registered_blocks['ui_params']):
            ui_params = gr.Group()
            DifferenceGlobals.ui_params = ui_params  # for hiding/showing when clicking on a tab
        create_inpaint_difference_ui(
            BlockManager(tab),
            BlockManager(ui_params)
        )

    if elem_id == 'img2img_mask_alpha':
        img2img_tabs = [
            child
            for child in DifferenceGlobals.registered_blocks['img2img_tabs'].children
            if isinstance(child, gr.TabItem)
        ]
        for i, tab in enumerate(img2img_tabs):
            tab.select(
                fn=lambda tab_id=i: gr.update(visible=tab_id == DifferenceGlobals.tab_index),
                inputs=[],
                outputs=[DifferenceGlobals.ui_params]
            )
            if i > 5:
                tab.select(
                    fn=lambda tab_id=i: gr.update(visible=False),
                    inputs=[],
                    outputs=[DifferenceGlobals.registered_blocks['inpaint_params']]
                )


def on_ui_settings():
    create_settings_section()


def setup_script_callbacks():
    script_callbacks.on_after_component(on_after_component)
    script_callbacks.on_ui_settings(on_ui_settings)
