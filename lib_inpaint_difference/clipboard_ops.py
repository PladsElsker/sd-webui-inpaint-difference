from io import BytesIO
import platform


def pil_to_clipboard(img):
    os_name = platform.system()
    if os_name == "Windows":
        pil_to_clipboard_windows(img)
    elif os_name == "Linux":
        pil_to_clipboard_linux(img)
    else:
        raise "OS not supported for clipboard operation"


def pil_to_clipboard_windows(img):
    with BytesIO() as buffer:
        img.convert("RGB").save(buffer, format="BMP")
        image_bytes = buffer.getvalue()[14:]
    
    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, image_bytes)
    win32clipboard.CloseClipboard()


def pil_to_clipboard_linux(img):
    with BytesIO() as output:
        img.save(output, format="PNG")
        image_bytes = output.getvalue()
    
    import subprocess
    process = subprocess.Popen(["xclip", "-selection", "clipboard", "-t", "image/png", "-i"], stdin=subprocess.PIPE)
    process.communicate(input=image_bytes)