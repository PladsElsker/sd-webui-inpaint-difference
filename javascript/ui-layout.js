(() => {
    const INPAINT_DIFFERENCE_POLLING_TIMEOUT = 500;

    document.addEventListener("DOMContentLoaded", () => {
        onInpaintDifferenceTabLoaded(setupCenterStyle);
    });


    function onInpaintDifferenceTabLoaded(callback) {
        const swapButtons = getSwapButtons();
        if (swapButtons === null || swapButtons.length === 0) {
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


    function getSwapButtons() {
        return document.querySelectorAll('.img2img_inpaint_difference_swap_images');
    }
})();
