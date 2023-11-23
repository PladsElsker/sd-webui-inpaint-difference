from modules.scripts import script_callbacks
from lib_inpaint_difference.settings import create_settings_section
from lib_inpaint_difference.img2img_tab_extender import Img2imgTabExtender


def on_ui_settings():
    create_settings_section()


def setup_script_callbacks():
    script_callbacks.on_ui_settings(on_ui_settings)
    script_callbacks.on_after_component(Img2imgTabExtender.on_after_component)
