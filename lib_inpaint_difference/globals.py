from modules.shared import opts


class DifferenceGlobals:
    is_extension_enabled = opts.data.get('inpaint_difference_enabled', True)
    show_image_under_mask = opts.data.get('inpaint_difference_show_image_under_mask', True)
    mask_brush_color = opts.data.get('inpaint_difference_mask_brush_color', '#ffffff')
