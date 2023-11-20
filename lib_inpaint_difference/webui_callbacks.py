from modules.scripts import script_callbacks
from lib_inpaint_difference.settings import create_settings_section


def on_ui_settings():
    create_settings_section()


def setup_script_callbacks():
    script_callbacks.on_ui_settings(on_ui_settings)
