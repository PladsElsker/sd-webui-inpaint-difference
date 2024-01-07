from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.webui_nasty_hijacks import hijack_img2img_processing, hijack_create_ui
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks


if DifferenceGlobals.is_extension_enabled:
    hijack_img2img_processing()
    hijack_create_ui()


setup_script_callbacks()
