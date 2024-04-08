import launch
import pkg_resources


sdwi2iextender_version = "0.0.10"
if not launch.is_installed('sdwi2iextender'):
    launch.run_pip(f'install sdwi2iextender=={sdwi2iextender_version}', f"sdwi2iextender for sd-webui-inpaint-difference")
else:
    current_version = pkg_resources.get_distribution("sdwi2iextender").version
    if pkg_resources.parse_version(current_version) != pkg_resources.parse_version(sdwi2iextender_version):
        launch.run_pip(f'install sdwi2iextender=={sdwi2iextender_version}', f"sdwi2iextender=={sdwi2iextender_version} for sd-webui-inpaint-difference")
