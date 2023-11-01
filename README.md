# sd-webui-inpaint-difference
## Overview
sd-webui-inpaint-difference is an A1111 extension to automatically find the inpaint mask to use based on the difference between an image and an altered version of the same image.  

## Installation
- Go to `extensions` > `Install from URL` in the webui
- Paste
```
https://github.com/John-WL/sd-webui-inpaint-difference
```
in the `URL for extension's git repository` checkbox  
- Click the `Install` button

## How to use
This extension will appear as a custom inpaint tab under the `img2img` tab:  
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/d6bc7b3b-d1a3-4706-88ab-623ead511c8d)

To start, upload your base image: 
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/2075367b-3076-4e95-b477-6162bb7b80c0)

Then, make some edits to the image in your favorite illustration software:
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/b2cf3ddf-b866-4f79-afe1-67dc9db10a7d)

Upload your altered image:
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/dc3509b4-5b2e-4324-9f54-c08774e71ddc)

Now that both your base and altered images are uploaded, the mask should generate:
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/5ced7d7f-0e24-46c8-9529-6ab8d30de7f8)

It's too dim right now, you can play with the settings to improve it:
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/0e49f836-e64e-484e-b732-1a4ecc30ee43)

You can improve how it looks by playing with the mask settings:
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/c185f563-2ac5-47d9-89ce-e19566b861ad)

The rest of the pipeline is as ususal! You can use controlnet or any other extension to generate images with the mask.  
The base image is only useful to generate the mask, and the altered image is used as the init image for the generation.  
(I made more edits for the hand, but you get the idea):
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/44d45e22-fbab-43cf-a994-c5841e1a8408)
