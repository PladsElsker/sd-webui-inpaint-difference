from modules.shared import opts, OptionInfo
from modules import ui_components

from lib_inpaint_difference.globals import DifferenceGlobals


def create_settings_section():
    section = ('inpaint_difference', 'Inpaint Difference')

    opts.add_option('inpaint_difference_enabled', OptionInfo(True, 'Enable inpaint-difference extension', section=section).needs_restart())
    opts.add_option('inpaint_difference_show_image_under_mask', OptionInfo(True, 'Display the altered image under the mask', section=section))
    opts.add_option('inpaint_difference_mask_brush_color', OptionInfo('#ffffff', 'Inpaint difference brush color', ui_components.FormColorPicker, {}, section=section).info('brush color of inpaint difference mask'))

    update_global_settings()


def update_global_settings():
    DifferenceGlobals.is_extension_enabled = opts.data.get('inpaint_difference_enabled', True)
    DifferenceGlobals.show_image_under_mask = opts.data.get('inpaint_difference_show_image_under_mask', True)
    DifferenceGlobals.mask_brush_color = opts.data.get('inpaint_difference_mask_brush_color', '#ffffff')

    def image_under_mask_visibility_changed():
        DifferenceGlobals.show_image_under_mask = opts.data.get('inpaint_difference_show_image_under_mask', True)

    def mask_brush_color_changed():
        DifferenceGlobals.mask_brush_color = opts.data.get('inpaint_difference_mask_brush_color', '#ffffff')

    opts.onchange('inpaint_difference_show_image_under_mask', image_under_mask_visibility_changed)
    opts.onchange('inpaint_difference_mask_brush_color', mask_brush_color_changed)
