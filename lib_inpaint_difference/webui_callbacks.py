from modules.scripts import script_callbacks

from lib_inpaint_difference.ui import inject_inpaint_difference_generation_params_ui
from lib_inpaint_difference.webui_nasty_hijacks import hijack_generation_params_ui


def on_before_component(_, **kwargs):
    elem_id = kwargs.get('elem_id', None)

    if elem_id == 'img2img_mask_alpha':
        inject_inpaint_difference_generation_params_ui()

    if elem_id == 'img2img_inpaint_full_res':
        hijack_generation_params_ui()


def setup_script_callbacks():
    script_callbacks.on_before_component(on_before_component)
