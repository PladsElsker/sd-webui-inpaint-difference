(() => {
    const INPAINT_DIFFERENCE_POLLING_TIMEOUT = 500;
    const COPY_SVG = `<svg xmlns="http://www.w3.org/2000/svg" height="100%" viewBox="0 -960 960 960" width="100%" fill="currentColor"><path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/></svg>`;

    document.addEventListener("DOMContentLoaded", () => {
        onInpaintDifferenceTabLoaded(setupCenterStyle);
        onInpaintDifferenceTabLoaded(() => watch_gradio_image('#visual_mask_inpaint_difference', setupCopyMaskToClipboardButton));
    });


    function onInpaintDifferenceTabLoaded(callback) {
        const swapButtons = getSwapButtons();
        const components = [
            swapButtons,
        ];

        if (components.includes(null) || swapButtons.length === 0) {
            setTimeout(() => { onInpaintDifferenceTabLoaded(callback); }, INPAINT_DIFFERENCE_POLLING_TIMEOUT);
            return;
        }

        callback();
    }


    function setupCenterStyle() {
        const swapButtons = getSwapButtons();
        for(const swapButton of swapButtons) {
            const form = swapButton.parentElement;
            form.style.position = 'relative';
            form.style.flexGrow = '0';
            form.style.padding = '10px';
        }
    }


    function setupCopyMaskToClipboardButton(_) {
        const elementToClone = document.querySelector('#visual_mask_inpaint_difference > .icon-buttons > *');
        if(elementToClone === null) return;
        if(elementToClone.parentElement.children.length >= 2) return;

        const copyButton = elementToClone.tagName === "button" ? elementToClone.cloneNode(true) : elementToClone.querySelector("button").cloneNode(true);
        const svgParent = copyButton.querySelector("svg").parentElement;
        svgParent.innerHTML = COPY_SVG;
        copyButton.setAttribute("aria-label", "Copy mask");
        copyButton.setAttribute("title", "Copy mask");

        elementToClone.parentElement.insertBefore(copyButton, elementToClone);

        copyButton.addEventListener("click", _ => {
            const image = getMaskElement();

            const canvas = document.createElement('canvas');
            canvas.width = image.naturalWidth;
            canvas.height = image.naturalHeight;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(image, 0, 0);

            canvas.toBlob(blob => {
                const data = [new ClipboardItem({ 'image/png': blob })];
                navigator.clipboard.write(data).then(
                    () => {
                        console.log('[sd-webui-inpaint-difference] Mask copied to clipboard');
                    },
                    error => {
                        console.error('[sd-webui-inpaint-difference] Error copying mask: ', error);
                    }
                );
            }, 'image/png');
        });
    }


    function getSwapButtons() {
        return document.querySelectorAll('.img2img_inpaint_difference_swap_images');
    }


    function getMaskElement() {
        return document.querySelector('#mask_inpaint_difference > div[data-testid="image"] > div > img');
    }


    function watch_gradio_image(id, modifiedCallback) {
        const targetNode = document.querySelector(id);
        const config = { childList: true, subtree: true, attributes: true, attributeFilter: ['src'] };
        const callback = function(mutationsList, _) {
            const completed = [];
            for(const mutation of mutationsList) {
                if(mutation.type === "childList") {
                    mutation.addedNodes.forEach(node => {
                        if(
                            node.tagName === "IMG" && 
                            node.alt === "" && 
                            !completed.includes(node)
                        ) {
                            modifiedCallback(node.src);
                            completed.push(node);
                        }
                    });
                    mutation.removedNodes.forEach(node => {
                        if(
                            node.tagName === "IMG" && 
                            node.alt === "" && 
                            !completed.includes(node)
                        ) {
                            modifiedCallback("");
                            completed.push(node);
                        }
                    });
                }
                else if(
                    mutation.type === "attributes" && 
                    mutation.attributeName === "src" && 
                    mutation.target.tagName === "IMG" && 
                    !completed.includes(mutation.target)
                ) {
                    modifiedCallback(mutation.target.src);
                    completed.push(mutation.target);
                }
            }
        };
        const observer = new MutationObserver(callback);
        observer.observe(targetNode, config);
        return observer;
    }
})();
