from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.gradio_hijacks import hijack_encode_pil_to_base64
from lib_inpaint_difference.webui_hijacks import hijack_StableDiffusionProcessingImg2Img__init__
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks


if DifferenceGlobals.is_extension_enabled:
    hijack_encode_pil_to_base64()
    hijack_StableDiffusionProcessingImg2Img__init__()


setup_script_callbacks(DifferenceGlobals.is_extension_enabled)
