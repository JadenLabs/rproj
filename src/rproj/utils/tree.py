import os
import re
from rich import print


def print_project_structure(
    root_dir: str,
    prefix: str = "",
    max_depth: int = 4,
    current_depth: int = 0,
    ignore: list = None,
    use_regex: bool = False,
) -> None:
    """
    Prints the directory structure of a given directory in a tree format.

    Args:
        root_dir (str): The root directory.
        prefix (str): The prefix used for indentation.
        max_depth (int): The maximum depth to print.
        current_depth (int): The current depth in the recursion.
        ignore (list): List of directories or files to ignore.
    """

    if current_depth > max_depth:
        return

    try:
        items = []
        for item in os.listdir(root_dir):
            if ignore:
                if use_regex:
                    if any(re.search(pattern, item) for pattern in ignore):
                        continue
                else:
                    if item in ignore:
                        continue
            items.append(item)
        items.sort()
    except PermissionError:
        print(f"{prefix}Permission denied: {root_dir}")
        return

    for index, item in enumerate(items):
        item_path = os.path.join(root_dir, item)
        is_dir = os.path.isdir(item_path)
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "

        if item.endswith(".py"):
            color = "green"
        elif item.endswith(".txt"):
            color = "blue"
        elif item.endswith(".md"):
            color = "yellow"
        elif item.endswith(".json"):
            color = "cyan"
        elif item.endswith(".csv"):
            color = "magenta"
        elif item.endswith(".yaml") or item.endswith(".yml"):
            color = "red"
        elif is_dir:
            color = "bright_black"
        else:
            color = "white"

        print(f"{prefix}{connector}[{color}]{item}[/]")

        if is_dir:
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_project_structure(
                item_path, new_prefix, max_depth, current_depth + 1, ignore, use_regex
            )
