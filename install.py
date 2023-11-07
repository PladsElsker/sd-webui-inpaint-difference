import launch


if not launch.is_installed('sdlib'):
    launch.run_pip(f'install sdlib', f"sdlib for sd-webui-inpaint-difference")
