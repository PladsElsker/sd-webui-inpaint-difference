from gradio.context import Context

from modules.scripts import script_callbacks
from lib_inpaint_difference.ui import create_inpaint_difference_generation_params_ui
from lib_inpaint_difference.webui_nasty_hijacks import hijack_generation_params_ui


class GradioParentContext:
    def __enter__(self):
        self.original_context = Context.block
        Context.block = Context.block.parent
        return self

    def __exit__(self, *args, **kwargs):
        Context.block = self.original_context


def on_before_component(_, **kwargs):
    elem_id = kwargs.get('elem_id', None)

    if elem_id == 'resize_mode':
        with GradioParentContext():
            create_inpaint_difference_generation_params_ui()

    if elem_id == 'img2img_mask_mode':
        hijack_generation_params_ui()


def setup_script_callbacks():
    script_callbacks.on_before_component(on_before_component)
