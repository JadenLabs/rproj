import os
import platform
import subprocess
from rproj import log


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


def launch_terminal(directory: str, terminal_type: str = "ps"):
    """Launch terminal in the given directory."""
    system_name = platform.system()
    if system_name == "Windows":
        launch_terminal_on_windows(directory, terminal_type)
    elif system_name == "Linux":
        launch_terminal_on_linux(directory, terminal_type)
    else:
        raise NotImplementedError(f"Terminal launch not supported on {system_name}")


def launch_terminal_on_windows(directory: str, terminal_type: str):
    """Launch terminal in the given directory on Windows."""
    match terminal_type:
        case "cmd":
            subprocess.run(f'start cmd /K "cd /d {directory}"', shell=True)
        case "powershell" | "ps":
            subprocess.run(
                f'start powershell -NoExit -Command "cd {directory}"', shell=True
            )
        case "pwsh":
            subprocess.run(f'start pwsh -NoExit -Command "cd {directory}"', shell=True)
        case "wt":
            subprocess.run(f'wt new-tab -p "PowerShell" -d "{directory}"', shell=True)
        case _:
            log.err(f"Terminal type {terminal_type} not supported on Windows")


def launch_terminal_on_linux(directory: str, terminal_type: str = "gnome"):
    """Launch terminal in the given directory on Linux."""
    match terminal_type:
        case "gnome":
            subprocess.run(f'gnome-terminal --working-directory="{directory}"', shell=True)
        case "konsole":
            subprocess.run(f'konsole --workdir "{directory}"', shell=True)
        case "xterm":
            subprocess.run(f'xterm -e "cd {directory}"', shell=True)
        case "xfce4-terminal":
            subprocess.run(f'xfce4-terminal --working-directory="{directory}"', shell=True)
        case "alacritty":
            subprocess.run(f'alacritty --working-directory "{directory}"', shell=True)
        case "kitty":
            subprocess.run(f'kitty --working-directory "{directory}"', shell=True)
        case _:
            log.err(f"Terminal type {terminal_type} not supported on Linux")
