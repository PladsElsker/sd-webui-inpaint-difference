from PIL import ImageOps

from modules import processing

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_difference.one_time_callable import one_time_callable


@one_time_callable
def hijack_StableDiffusionProcessingImg2Img__init__():
    original_StableDiffusionProcessingImg2Img__init__ = processing.StableDiffusionProcessingImg2Img.__init__

    def hijack_func(*args, **kwargs):
        if not DifferenceGlobals.tab_selected:
            return original_StableDiffusionProcessingImg2Img__init__(*args, **kwargs)
        
        image = ImageOps.exif_transpose(DifferenceGlobals.altered_image)
        mask = processing.create_binary_mask(DifferenceGlobals.generated_mask)

        kwargs["init_images"] = [image]
        kwargs["mask"] = mask

        return original_StableDiffusionProcessingImg2Img__init__(*args, **kwargs)

    processing.StableDiffusionProcessingImg2Img.__init__ = hijack_func
