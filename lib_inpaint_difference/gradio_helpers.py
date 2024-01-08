import gradio.context
from gradio.context import Context as GradioContext


def _find_root_block(block):
    root = block
    while root.parent is not None:
        root = root.parent

    return root


class GradioContextSwitch:
    def __init__(self, block):
        self.block = block
        self.root_block = _find_root_block(block)

    def __enter__(self):
        self.previous_root_block = gradio.context.Context.root_block
        gradio.context.Context.root_block = self.root_block

        self.previous_block = GradioContext.block
        GradioContext.block = self.block
        return self

    def __exit__(self, *args, **kwargs):
        GradioContext.block = self.previous_block
        gradio.context.Context.root_block = self.previous_root_block
