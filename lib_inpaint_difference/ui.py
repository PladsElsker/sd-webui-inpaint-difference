import functools
import uuid
import gradio as gr

from sdwi2iextender import OperationMode
from sdwi2iextender.gradio_helpers import GradioContextSwitch

from modules.shared import opts
from modules.ui_components import ToolButton, FormRow

from lib_inpaint_difference.mask_processing import compute_mask


class InpaintDifferenceTab(OperationMode):
    show_inpaint_params = True
    requested_elem_ids = ['img2img_mask_blur', 'img2img_mask_alpha']

    def __init__(self):
        self.inpaint_img_component = None
        self.inpaint_alt_component = None
        self.inpaint_visual_mask_component = None
        self.swap_images = None

        self.mask_blur = None
        self.mask_alpha = None
        self.mask_dilation = None

    def image_components(self):
        self.inpaint_alt_component = gr.Image(label="Altered image", source="upload", interactive=True, type="pil", elem_id="alt_inpaint_difference")
        self.inpaint_alt_component.unrender()
        self.inpaint_mask_component = gr.Image(visible=False, label="Altered image", interactive=True, type="pil", elem_id="mask_inpaint_difference")
        return self.inpaint_alt_component, self.inpaint_mask_component

    def tab(self):
        with gr.TabItem(label='Inpaint difference') as self.tab:
            with gr.Row():
                self.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_difference")
                self.swap_images = ToolButton(value='⇆', elem_id=f'img2img_inpaint_difference_swap_images_{uuid.uuid4()}', elem_classes=['img2img_inpaint_difference_swap_images'], tooltip="Swap images.")
                self.inpaint_alt_component.render()

            mask_component_height = getattr(opts, 'img2img_editor_height', 512)  # 512 is for SD.Next
            self.inpaint_visual_mask_component = gr.Image(label="Difference mask", interactive=False, type="pil", elem_id="visual_mask_inpaint_difference", height=mask_component_height)

    def section(self, components):
        self.mask_blur = components["img2img_mask_blur"]
        self.mask_alpha = components["img2img_mask_alpha"]

        inpaint_block = self.mask_alpha.parent.parent.parent
        with GradioContextSwitch(inpaint_block):
            with gr.Accordion(label='Inpaint Difference', open=False, visible=False, elem_id="inpaint_difference_inpaint_params") as self.inpaint_difference_ui_params:
                with FormRow():
                    self.mask_erosion = gr.Slider(label='Mask erosion', maximum=100, step=1, value=0, elem_id='inpaint_difference_mask_erosion')
                    self.mask_dilation = gr.Slider(label='Mask dilation', maximum=100, step=1, value=0, elem_id='inpaint_difference_mask_dilation')

                with FormRow():
                    self.difference_threshold = gr.Slider(label='Difference threshold', maximum=1, step=0.01, value=1, elem_id='inpaint_difference_difference_threshold')

                with FormRow():
                    self.contours_only = gr.Checkbox(label='Contours only', value=False, elem_id='inpaint_difference_contours_only')

        # Move the accordion as the first item in the list
        inpaint_block.children[1:1], inpaint_block.children[-1:] = inpaint_block.children[-1:], []

    def gradio_events(self, selected: gr.Checkbox):
        self._update_sliders_visibility(selected)
        self._update_mask()
        self._swap_images_tool()
        self._update_resize_to_slider_dimensions()

    def _update_sliders_visibility(self, selected):
        def sliders_visibility_func(is_this_tab_selected):
            updates = [
                gr.update(visible=is_this_tab_selected),
                gr.update(visible=is_this_tab_selected),
                gr.update(visible=False) if is_this_tab_selected else gr.update(),
            ]
            return *updates,

        selected.change(
            fn=sliders_visibility_func,
            inputs=[selected],
            outputs=[
                self.mask_dilation,
                self.inpaint_difference_ui_params,
                self.mask_alpha,
            ]
        )

    def _update_mask(self):
        compute_mask_dict = dict(
            fn=compute_mask,
            inputs=[
                self.inpaint_img_component,
                self.inpaint_alt_component,
                self.mask_blur,
                self.mask_dilation,
                self.mask_erosion,
                self.difference_threshold,
                self.contours_only,
            ],
            outputs=[
                self.inpaint_mask_component,
                self.inpaint_visual_mask_component,
            ]
        )

        self.inpaint_img_component.upload(**compute_mask_dict)
        self.inpaint_img_component.clear(**compute_mask_dict)
        self.inpaint_alt_component.upload(**compute_mask_dict)
        self.inpaint_alt_component.clear(**compute_mask_dict)
        self.mask_blur.release(**compute_mask_dict)
        self.mask_dilation.release(**compute_mask_dict)
        self.mask_erosion.release(**compute_mask_dict)
        self.difference_threshold.release(**compute_mask_dict)
        self.contours_only.change(**compute_mask_dict)

    def _swap_images_tool(self):
        def swap_images_func(img, alt, *args):
            _, visual_mask = compute_mask(alt, img, *args)
            return gr.update(value=alt), gr.update(value=img), gr.update(value=visual_mask)

        self.swap_images.click(
            fn=swap_images_func,
            inputs=[
                self.inpaint_img_component,
                self.inpaint_alt_component,
                self.mask_blur,
                self.mask_dilation,
                self.mask_erosion,
                self.difference_threshold,
                self.contours_only,
            ],
            outputs=[
                self.inpaint_img_component,
                self.inpaint_alt_component,
                self.inpaint_visual_mask_component,
            ]
        )

    def _update_resize_to_slider_dimensions(self):
        self.inpaint_visual_mask_component.change(fn=lambda: None, _js="updateImg2imgResizeToTextAfterChangingImage", inputs=[], outputs=[], show_progress=False)
