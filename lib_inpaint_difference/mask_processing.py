import torch
import numpy as np
from PIL import Image
import cv2

from lib_inpaint_difference.globals import DifferenceGlobals


def compute_mask(
        base_img,
        altered_img,
        blur_amount,
        dilation_amount,
        erosion_amount,
        difference_threshold,
        contours_only,
):
    DifferenceGlobals.base_image = base_img
    DifferenceGlobals.altered_image = altered_img

    if not validate_input_images(base_img, altered_img):
        return None

    base_img, altered_img = ensure_same_size(base_img, altered_img)

    base = np.array(base_img).astype(np.int32)
    altered = np.array(altered_img).astype(np.int32)

    img2img_processing_mask = compute_base_mask(base, altered, dilation_amount, erosion_amount, difference_threshold, contours_only)
    visual_mask = compute_visual_mask(altered, img2img_processing_mask, blur_amount)
    return Image.fromarray(visual_mask.astype(np.uint8), mode=DifferenceGlobals.base_image.mode)


def validate_input_images(base_img, altered_img):
    return base_img is not None and altered_img is not None


def ensure_same_size(base_img, altered_img):
    same_size = base_img.size == altered_img.size
    if not same_size:
        base_img = base_img.resize((altered_img.width, altered_img.height))

    return base_img, altered_img


def compute_base_mask(
        base,
        altered,
        dilation_amount,
        erosion_amount,
        difference_threshold,
        contours_only,
):
    mask = compute_diff(base, altered)
    mask = uncolorize(mask)
    mask = saturate(mask, difference_threshold)
    mask = extract_contours(mask, contours_only)
    mask = dilate(mask, dilation_amount)
    mask = erode(mask, erosion_amount)

    mask_pil = Image.fromarray(mask.astype(np.uint8), mode=DifferenceGlobals.base_image.mode)
    DifferenceGlobals.generated_mask = mask_pil
    return mask


def compute_visual_mask(
        altered,
        mask,
        blur_amount,
):
    mask = blur(mask, blur_amount)
    visual_mask = mask
    visual_mask = colorize(visual_mask)
    visual_mask = process_image_under_mask(mask, visual_mask, altered)
    return visual_mask


def compute_diff(base, altered):
    return np.abs(base - altered)


def uncolorize(mask):
    b, g, r = cv2.split(mask)
    average = (r + g + b) // 3
    return np.repeat(average[:, :, np.newaxis], repeats=3, axis=-1)


def saturate(mask, difference_threshold):
    return np.where(mask/255 > 1 - difference_threshold, 255.0, 0.0)


def extract_contours(mask, contours_only):
    if not contours_only:
        return mask

    output_mask = mask.copy().astype(np.uint8)

    for i in range(mask.shape[2]):
        mask_comp = output_mask[:, :, i]
        _, threshold = cv2.threshold(mask_comp, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_img = np.zeros_like(mask_comp)
        cv2.drawContours(contours_img, contours, -1, 255, 1)
        output_mask[:, :, i] = contours_img
    
    output_mask[0, :, :] = 0
    output_mask[-1, :, :] = 0
    output_mask[:, 0, :] = 0
    output_mask[:, -1, :] = 0

    return output_mask.astype(np.float32)


def dilate(mask, dilation_amount):
    if dilation_amount == 0:
        return mask

    tensor_mask = torch.from_numpy((mask / 255).astype(np.float32)).permute(2, 0, 1).unsqueeze(0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tensor_mask = tensor_mask.to(device)
    kernel = torch.ones(1, 1, 3, 3).to(device)

    tensor_mask_r = tensor_mask[:, 0:1, :, :]
    tensor_mask_g = tensor_mask[:, 1:2, :, :]
    tensor_mask_b = tensor_mask[:, 2:3, :, :]
    for _ in range(dilation_amount):
        tensor_mask_r = (torch.nn.functional.conv2d(tensor_mask_r, kernel, padding=1) > 0).float()
        tensor_mask_g = (torch.nn.functional.conv2d(tensor_mask_g, kernel, padding=1) > 0).float()
        tensor_mask_b = (torch.nn.functional.conv2d(tensor_mask_b, kernel, padding=1) > 0).float()

    tensor_mask = torch.cat((tensor_mask_r, tensor_mask_g, tensor_mask_b), dim=1)
    dilated_mask = tensor_mask.squeeze(0).permute(1, 2, 0).cpu().numpy()
    return (dilated_mask * 255).astype(np.uint8)


def apply_recursive_component_wise_tensor_operation(img, iterations, operation):
    if iterations == 0:
        return img

    tensor_img = torch.from_numpy((img / 255).astype(np.float32)).permute(2, 0, 1).unsqueeze(0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tensor_img = tensor_img.to(device)

    tensor_img_r = tensor_img[:, 0:1, :, :]
    tensor_img_g = tensor_img[:, 1:2, :, :]
    tensor_img_b = tensor_img[:, 2:3, :, :]
    for _ in range(iterations):
        tensor_img_r = operation(tensor_img_r).float()
        tensor_img_g = operation(tensor_img_g).float()
        tensor_img_b = operation(tensor_img_b).float()

    tensor_img = torch.cat((tensor_img_r, tensor_img_g, tensor_img_b), dim=1)
    transformed_img = tensor_img.squeeze(0).permute(1, 2, 0).cpu().numpy()
    return (transformed_img * 255).astype(np.uint8)


def erode(mask, erosion_amount):
    if erosion_amount == 0:
        return mask

    tensor_mask = torch.from_numpy((mask / 255).astype(np.float32)).permute(2, 0, 1).unsqueeze(0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tensor_mask = tensor_mask.to(device)
    kernel = torch.ones(1, 1, 3, 3).to(device)

    tensor_mask_r = tensor_mask[:, 0:1, :, :]
    tensor_mask_g = tensor_mask[:, 1:2, :, :]
    tensor_mask_b = tensor_mask[:, 2:3, :, :]
    for _ in range(erosion_amount):
        tensor_mask_r = (torch.nn.functional.conv2d(1 - tensor_mask_r, kernel, padding=1) == 0).float()
        tensor_mask_g = (torch.nn.functional.conv2d(1 - tensor_mask_g, kernel, padding=1) == 0).float()
        tensor_mask_b = (torch.nn.functional.conv2d(1 - tensor_mask_b, kernel, padding=1) == 0).float()

    tensor_mask = torch.cat((tensor_mask_r, tensor_mask_g, tensor_mask_b), dim=1)
    eroded_mask = tensor_mask.squeeze(0).permute(1, 2, 0).cpu().numpy()
    return (eroded_mask * 255).astype(np.uint8)


# similar to how StableDiffusionProcessingImg2Img does it
def blur(mask, blur_amount):
    np_mask = np.array(mask)
    kernel_size = 2 * int(2.5 * blur_amount + 0.5) + 1
    return cv2.GaussianBlur(np_mask, (kernel_size, kernel_size), blur_amount)


def colorize(mask):
    color_str = DifferenceGlobals.mask_brush_color
    color = np.array([int(color_str[i:i+2], 16)/255 for i in range(1, 7, 2)])
    return mask * color


def process_image_under_mask(original_mask, colorized_mask, altered):
    if not DifferenceGlobals.show_image_under_mask:
        return colorized_mask

    normalized_mask = original_mask / 255
    return altered*(1-normalized_mask) + colorized_mask*normalized_mask
