from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks


setup_script_callbacks(DifferenceGlobals.is_extension_enabled)
