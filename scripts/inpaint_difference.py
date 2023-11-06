import sdlib
plugin = sdlib.register_plugin("inpaint-difference")

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.webui_nasty_hijacks import hijack_img2img_processing
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks
from lib_inpaint_difference.img2img_ui import InpaintDifferenceTab


if DifferenceGlobals.is_extension_enabled:
    plugin.append_component(InpaintDifferenceTab, name='create_img2img_tab')
    hijack_img2img_processing()


setup_script_callbacks()
