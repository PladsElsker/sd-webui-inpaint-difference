from dataclasses import dataclass
import functools
import gradio as gr
from gradio.context import Context as GradioContext
from gradio.blocks import Block as GradioBlock
from lib_inpaint_difference.ui import InpaintDifferenceTab


class GradioContextSwitch:
    def __init__(self, block):
        self.block = block

    def __enter__(self):
        self.previous_block = GradioContext.block
        GradioContext.block = self.block
        return self

    def __exit__(self, *args, **kwargs):
        GradioContext.block = self.previous_block


@dataclass
class TabData:
    tab_index: int
    ui_params: GradioBlock


class Img2imgTabExtender:
    img2img_tabs_block = None
    ui_params_block = None
    inpaint_params_block = None
    amount_of_default_tabs = None
    tab_data_list = []

    @classmethod
    def on_after_component(cls, component, **kwargs):
        elem_id = kwargs.get('elem_id', None)

        if elem_id == 'img2img_batch_inpaint_mask_dir':
            cls.register_img2img_tabs_block(component)
            cls.create_custom_tabs_if_initialized()

        if elem_id == 'img2img_mask_blur':
            cls.register_inpaint_params_block(component)
            cls.register_custom_ui_params_block(component)
            cls.create_custom_tabs_if_initialized()

    @classmethod
    def create_custom_tabs_if_initialized(cls):
        if None in [cls.img2img_tabs_block, cls.inpaint_params_block, cls.ui_params_block]:
            return

        cls.register_default_amount_of_tabs()
        cls.create_custom_tabs()
        cls.setup_navigation_events()

    @classmethod
    def register_img2img_tabs_block(cls, component):
        cls.img2img_tabs_block = component.parent.parent

    @classmethod
    def register_inpaint_params_block(cls, component):
        cls.inpaint_params_block = component.parent.parent

    @classmethod
    def register_custom_ui_params_block(cls, component):
        cls.ui_params_block = component.parent.parent.parent

    @classmethod
    def register_default_amount_of_tabs(cls):
        cls.amount_of_default_tabs = cls._find_new_tab_index()

    @classmethod
    def create_custom_tabs(cls):
        for tab_class in [InpaintDifferenceTab]:
            tab_index = cls._find_new_tab_index()
            custom_tab_object = tab_class(tab_index)

            with GradioContextSwitch(cls.img2img_tabs_block):
                custom_tab_object.tab()
            with GradioContextSwitch(cls.ui_params_block):
                with gr.Group() as tab_ui_params:
                    custom_tab_object.section()

            custom_tab_object.gradio_events()

            cls.register_custom_tab_data(tab_index, tab_ui_params)

    @classmethod
    def register_custom_tab_data(cls, tab_index, tab_ui_params):
        cls.tab_data_list.append(TabData(tab_index, tab_ui_params))

    @classmethod
    def setup_navigation_events(cls):
        img2img_tabs = [
            child
            for child in cls.img2img_tabs_block.children
            if isinstance(child, gr.TabItem)
        ]
        for custom_tab in cls.tab_data_list:
            for i, tab in enumerate(img2img_tabs):
                def update_func(tab_id, custom_tab_data):
                    return gr.update(visible=tab_id == custom_tab_data.tab_index)

                tab.select(
                    fn=functools.partial(update_func, tab_id=i, custom_tab_data=custom_tab),
                    inputs=[],
                    outputs=[custom_tab.ui_params]
                )

                # extend the behavior of hiding the default inpaint_params
                if i >= cls.amount_of_default_tabs:
                    tab.select(
                        fn=lambda tab_id=i: gr.update(visible=False),
                        inputs=[],
                        outputs=[cls.inpaint_params_block]
                    )

    @classmethod
    def _find_new_tab_index(cls):
        img2img_tabs = [
            child
            for child in cls.img2img_tabs_block.children
            if isinstance(child, gr.TabItem)
        ]
        return len(img2img_tabs)
