import launch


pip_dependencies = [
    'opencv-python',
]

for dependency in pip_dependencies:
    if not launch.is_installed("opencv-python"):
        launch.run_pip("install opencv-python", "opencv-python for sd-webui-inpaint-difference")
