import sdwss

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.webui_nasty_hijacks import hijack_img2img_processing
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks
from lib_inpaint_difference.ui import InpaintDifferenceTab


plugin = sdwss.register_plugin("inpaint-difference")


if DifferenceGlobals.is_extension_enabled:
    plugin.append_component(InpaintDifferenceTab, name='create_img2img_tab')
    hijack_img2img_processing()


setup_script_callbacks()
