from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.gradio_hijack import hijack_encode_pil_to_base64
from lib_inpaint_difference.webui_nasty_hijacks import hijack_img2img_processing, hijack_ui_settings
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks


if DifferenceGlobals.is_extension_enabled:
    hijack_encode_pil_to_base64()
    hijack_img2img_processing()
    hijack_ui_settings()


setup_script_callbacks()
