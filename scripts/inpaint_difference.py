from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.webui_nasty_hijacks import hijack_gradio_tabs, hijack_img2img_processing
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks


if DifferenceGlobals.is_extension_enabled:
    hijack_gradio_tabs()
    hijack_img2img_processing()

setup_script_callbacks()
