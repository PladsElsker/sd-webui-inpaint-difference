from modules.scripts import script_callbacks

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.settings import create_settings_section
from lib_inpaint_difference.ui import create_inpaint_difference_tab, inject_inpaint_difference_generation_params_ui
from lib_inpaint_difference.webui_nasty_hijacks import hijack_generation_params_ui, register_tabitem_to_tab_list


def on_before_component(_, **kwargs):
    if not DifferenceGlobals.is_extension_enabled:
        return

    elem_id = kwargs.get('elem_id', None)

    if elem_id == 'img2img_batch_inpaint_mask_dir':
        DifferenceGlobals.img2img_tab = create_inpaint_difference_tab()

    if elem_id == 'img2img_mask_alpha':
        inject_inpaint_difference_generation_params_ui()

    if elem_id == 'img2img_inpaint_full_res_padding':
        register_tabitem_to_tab_list()
        hijack_generation_params_ui()


def on_ui_settings():
    create_settings_section()


def setup_script_callbacks():
    script_callbacks.on_before_component(on_before_component)
    script_callbacks.on_ui_settings(on_ui_settings)
