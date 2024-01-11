import numpy as np
from cv2 import imencode
import base64
import gradio as gr
from lib_inpaint_difference.one_time_callable import one_time_callable


@one_time_callable
def hijack_encode_pil_to_base64():
    # from https://github.com/gradio-app/gradio/issues/2635#issuecomment-1423531319
    def encode_pil_to_base64_new(pil_image):
        image_arr = np.asarray(pil_image)[:,:,::-1]
        _, byte_data = imencode('.png', image_arr)
        base64_data = base64.b64encode(byte_data)
        base64_string_opencv = base64_data.decode("utf-8")
        return "data:image/png;base64," + base64_string_opencv

    gr.processing_utils.encode_pil_to_base64 = encode_pil_to_base64_new
