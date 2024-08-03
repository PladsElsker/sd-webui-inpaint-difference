import launch
import pkg_resources
import platform


minimum_sdwi2iextender_version = "0.2.0"
if not launch.is_installed("sdwi2iextender"):
    launch.run_pip(f"install sdwi2iextender", f"sdwi2iextender for sd-webui-inpaint-difference")
else:
    current_version = pkg_resources.get_distribution("sdwi2iextender").version
    if pkg_resources.parse_version(current_version) < pkg_resources.parse_version(minimum_sdwi2iextender_version):
        launch.run_pip(f"install sdwi2iextender=={minimum_sdwi2iextender_version}", f"sdwi2iextender=={minimum_sdwi2iextender_version} for sd-webui-inpaint-difference")


if platform.system() == "Windows":
    if not launch.is_installed("pywin32"):
        launch.run_pip(f"install pywin32", f"pywin32 for sd-webui-inpaint-difference on windows")
