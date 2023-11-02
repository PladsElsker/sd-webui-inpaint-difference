from modules import scripts

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.webui_nasty_hijacks import hijack_gradio_tabs, hijack_img2img_processing
from lib_inpaint_difference.webui_callbacks import setup_script_callbacks


class DummyInpaintDifferenceScript(scripts.Script):
    def title(self):
        return 'Inpaint Difference'

    def show(self, is_img2img):
        return False

    def ui(self, is_img2img):
        return []


if DifferenceGlobals.is_extension_enabled:
    hijack_gradio_tabs()
    hijack_img2img_processing()

setup_script_callbacks()
