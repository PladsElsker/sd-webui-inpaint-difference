from modules.shared import opts, OptionInfo
from modules.scripts import script_callbacks
from modules import ui_components

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.ui import inject_inpaint_difference_generation_params_ui
from lib_inpaint_difference.webui_nasty_hijacks import hijack_generation_params_ui


def on_before_component(_, **kwargs):
    if not DifferenceGlobals.is_extension_enabled:
        return

    elem_id = kwargs.get('elem_id', None)

    if elem_id == 'img2img_mask_alpha':
        inject_inpaint_difference_generation_params_ui()

    if elem_id == 'img2img_inpaint_full_res':
        hijack_generation_params_ui()


def on_ui_settings():
    section = ('inpaint_difference', 'Inpaint Difference')

    opts.add_option('inpaint_difference_enabled', OptionInfo(True, 'Enable inpaint-difference extension', section=section).needs_restart())
    opts.add_option('inpaint_difference_show_image_under_mask', OptionInfo(True, 'Display the altered image under the mask', section=section).needs_restart())
    opts.add_option('inpaint_difference_mask_brush_color', OptionInfo('#ffffff', 'Inpaint difference brush color', ui_components.FormColorPicker, {}, section=section).info('brush color of inpaint difference mask').needs_restart())

    update_global_settings()


def update_global_settings():
    DifferenceGlobals.is_extension_enabled = opts.data.get('inpaint_difference_enabled', True)
    DifferenceGlobals.show_image_under_mask = opts.data.get('inpaint_difference_show_image_under_mask', True)
    DifferenceGlobals.mask_brush_color = opts.data.get('inpaint_difference_mask_brush_color', '#ffffff')


def setup_script_callbacks():
    script_callbacks.on_before_component(on_before_component)
    script_callbacks.on_ui_settings(on_ui_settings)
