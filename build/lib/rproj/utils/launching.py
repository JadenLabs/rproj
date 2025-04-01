import os
import platform
import subprocess
from rproj.utils import log


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


def launch_terminal(directory: str, terminal_type: str = "ps", command: str = None):
    """Launch terminal in the given directory and optionally run a command."""
    system_name = platform.system()
    if system_name == "Windows":
        launch_terminal_on_windows(directory, terminal_type, command)
    elif system_name == "Linux":
        launch_terminal_on_linux(directory, terminal_type, command)
    else:
        raise NotImplementedError(f"Terminal launch not supported on {system_name}")


def launch_terminal_on_windows(directory: str, terminal_type: str, command: str):
    """Launch terminal in the given directory on Windows and optionally run a command."""
    if terminal_type in ["powershell", "ps", "pwsh"]:
        command = (
            f'Set-Location -Path "{directory}"; {command}'
            if command
            else f'Set-Location -Path "{directory}"'
        )
    else:
        command = (
            f'cd /d "{directory}" && {command}' if command else f'cd /d "{directory}"'
        )

    match terminal_type:
        case "cmd":
            subprocess.run(f'start cmd /K "{command}"', shell=True)
        case "powershell" | "ps":
            subprocess.run(f'start powershell -NoExit -Command "{command}"', shell=True)
        case "pwsh":
            subprocess.run(f'start pwsh -NoExit -Command "{command}"', shell=True)
        case "wt":
            subprocess.run(
                f'wt new-tab -p "PowerShell" -d "{directory}" powershell -NoExit -Command "{command}"',
                shell=True,
            )
        case _:
            log.err(f"Terminal type {terminal_type} not supported on Windows")


def launch_terminal_on_linux(directory: str, terminal_type: str, command: str):
    """Launch terminal in the given directory on Linux and optionally run a command."""
    if command:
        command = f'cd "{directory}" && {command}; exec bash'
    else:
        command = f'cd "{directory}"; exec bash'

    match terminal_type:
        case "gnome":
            subprocess.run(f'gnome-terminal -- bash -c "{command}"', shell=True)
        case "konsole":
            subprocess.run(
                f'konsole --workdir "{directory}" -e bash -c "{command}"', shell=True
            )
        case "xterm":
            subprocess.run(f"xterm -e \"bash -c '{command}'\"", shell=True)
        case "xfce4-terminal":
            subprocess.run(
                f'xfce4-terminal --working-directory="{directory}" -e "bash -c \'{command}\'"',
                shell=True,
            )
        case "alacritty":
            subprocess.run(
                f'alacritty --working-directory "{directory}" -e bash -c "{command}"',
                shell=True,
            )
        case "kitty":
            subprocess.run(
                f'kitty --working-directory "{directory}" bash -c "{command}"',
                shell=True,
            )
        case _:
            log.err(f"Terminal type {terminal_type} not supported on Linux")
