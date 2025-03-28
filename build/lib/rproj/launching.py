import os
import platform


def launch_vsc(directory: str):
    """Launch VSC in the given directory."""
    os.system(f"code {directory}")


def launch_file_explorer(directory: str):
    """Launch file explorer in the given directory."""
    system_name = platform.system()
    if system_name == "Windows":
        os.system(f"explorer {directory}")
    elif system_name == "Linux":
        os.system(f"xdg-open {directory}")
    else:
        raise NotImplementedError(
            f"File explorer launch not supported on {system_name}"
        )
