from dataclasses import dataclass
import functools

import gradio as gr
from lib_inpaint_difference.gradio_helpers import GradioContextSwitch
from lib_inpaint_difference.ui import InpaintDifferenceTab


NEW_TAB_CLASSES = [
    InpaintDifferenceTab,
]


@dataclass
class TabData:
    tab_index: int
    tab_class: type
    tab_object: object


class Img2imgTabExtender:
    img2img_tabs_block = None
    inpaint_params_block = None
    amount_of_default_tabs = None
    tab_data_list = []

    @classmethod
    def on_after_component(cls, component, **kwargs):
        elem_id = kwargs.get('elem_id', None)

        if elem_id == 'img2img_batch_inpaint_mask_dir':
            cls.register_img2img_tabs_block(component)

        if elem_id == 'img2img_mask_blur':
            cls.register_inpaint_params_block(component)

        cls.register_requested_elem_ids(component, elem_id)

    @classmethod
    def register_img2img_tabs_block(cls, component):
        cls.img2img_tabs_block = component.parent.parent

    @classmethod
    def register_inpaint_params_block(cls, component):
        cls.inpaint_params_block = component.parent.parent

    @classmethod
    def register_requested_elem_ids(cls, component, elem_id):
        if elem_id is None:
            return

        for tab_class in NEW_TAB_CLASSES:
            if not hasattr(tab_class, 'requested_elem_ids'):
                continue

            if not hasattr(tab_class, '_registered_elem_ids'):
                tab_class._registered_elem_ids = dict()

            if elem_id in tab_class.requested_elem_ids:
                tab_class._registered_elem_ids[elem_id] = component

    @classmethod
    def create_custom_tabs(cls):
        cls.register_default_amount_of_tabs()

        for tab_class in NEW_TAB_CLASSES:
            tab_index = cls._find_new_tab_index()
            custom_tab_object = tab_class(tab_index)
            registered_components = getattr(tab_class, "_registered_elem_ids", None)

            with GradioContextSwitch(cls.img2img_tabs_block):
                custom_tab_object.tab()
            with GradioContextSwitch(cls.inpaint_params_block):
                custom_tab_object.section(registered_components)

            cls.register_custom_tab_data(tab_index, tab_class, custom_tab_object)

            with GradioContextSwitch(cls.inpaint_params_block):
                img2img_tabs = cls._get_img2img_tabs()
                cls.setup_navigation_events(img2img_tabs)
                for tab_data in cls.tab_data_list:
                    tab_data.tab_object.gradio_events(img2img_tabs)

    @classmethod
    def register_default_amount_of_tabs(cls):
        cls.amount_of_default_tabs = cls._find_new_tab_index()

    @classmethod
    def register_custom_tab_data(cls, tab_index, tab_class, tab_object):
        cls.tab_data_list.append(TabData(tab_index, tab_class, tab_object))

    @classmethod
    def setup_navigation_events(cls, img2img_tabs):
        block_data_iterator = zip(img2img_tabs[cls.amount_of_default_tabs:], cls.tab_data_list, strict=True)
        for tab_block, custom_tab in block_data_iterator:
            def update_func(custom_tab):
                should_show_inpaint_params = getattr(custom_tab.tab_class, 'show_inpaint_params', True)
                return gr.update(visible=should_show_inpaint_params)

            func_dict = dict(
                fn=functools.partial(update_func, custom_tab=custom_tab),
                inputs=[],
                outputs=[
                    cls.inpaint_params_block
                ]
            )

            tab_block.select(**func_dict)

    @classmethod
    def _find_new_tab_index(cls):
        img2img_tabs = [
            child
            for child in cls.img2img_tabs_block.children
            if isinstance(child, gr.TabItem)
        ]
        return len(img2img_tabs)

    @classmethod
    def _get_img2img_tabs(cls):
        return [
            child
            for child in cls.img2img_tabs_block.children
            if isinstance(child, gr.TabItem)
        ]
