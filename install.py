import launch


if not launch.is_installed('sdwss'):
    launch.run_pip(f'install sdwss', f"sdwss for sd-webui-inpaint-difference")
