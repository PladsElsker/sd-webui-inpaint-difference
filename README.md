# sd-webui-inpaint-difference
## Overview
An A1111 extension to add a new operation mode in the `img2img` tab. It finds the inpaint mask to use based on the difference between two images.  

## Usage
Here is the suggested workflow for this extension:  

![Untitled](https://github.com/John-WL/sd-webui-inpaint-difference/assets/34081873/28027417-a4f2-4145-861a-2d54734854e4)


## Installation
1) Go to Extensions > Available
2) Click the `Load from:` button
3) Enter "inpaint difference" in the search bar
4) Click the `Install` button of the "inpaint difference" Tab cell
5) Restart the webui

## How to use
1) Get your image.
2) Modify it in your favorite illustration software.
3) Upload your initial image in the `Base image`, and upload the modified image in the `Altered image`.
4) Once both images are uploaded, the `Generated mask` will appear.
5) You're done! When clicking the `Generate` button, the operation mode will use the `Altered image` and the `Generated mask` to inpaint the image like you would normally expect with the other operation modes.

> Additional parameters are added under the operation mode as well to edit the mask. You can also look into the settings for the brush color and other options like that. 

