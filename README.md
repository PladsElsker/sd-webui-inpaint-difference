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
![image](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/9c3492a7-a15b-4852-8177-3893f33c721d)

The process can be broken down into 2 steps:
- Generate the mask
- Generate an image like you normally would


To start, upload your base image. Then, do some modifications to the base image in the illustration software of your choice, and upload the altered image:


