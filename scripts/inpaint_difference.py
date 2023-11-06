from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.webui_nasty_hijacks import hijack_img2img_processing
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks
from lib_inpaint_difference.img2img_ui import create_img2img_tab


if DifferenceGlobals.is_extension_enabled:
    create_img2img_tab()
    hijack_img2img_processing()


setup_script_callbacks()
