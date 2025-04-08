import argparse


class Command:
    """
    Represents a command.

    Args:
        name (str): The name of the command.
        help_text (str): A description of the command.
        aliases (list[str], optional): Alternative names for the command. Defaults to an empty list.
        args (list[str | tuple], optional): Arguments for the command. Defaults to an empty list.

    Example:
        ```
        command = Command(
            name="name",
            help_text="description",
            aliases=["n"],
            args=["name", ("--advanced-arg", {"kwarg": value})],
        )
        ```
    """

    def __init__(
        self,
        name: str,
        help_text: str,
        aliases: list[str] = [],
        args: list[str | tuple] = [],
    ):
        self.name = name
        self.aliases = aliases
        self.help_text = help_text
        self.args = args


def get_args():
    """
    Parse and return command-line arguments for the rproj CLI.\n
    ---

    This function sets up the argument parser.\n
    Each subcommand may have its own set of arguments, including positional and
    optional arguments. Aliases are also provided for some subcommands.
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    # Create the main argument parser
    parser = argparse.ArgumentParser(
        prog="rproj", description="Create, manage, and view your projects"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # List of commands
    commands = [
        Command(
            "create",
            "Create a new project",
            ["c", "make"],
            [
                "name",
                "directory",
                "--run",
                "--github",
                ("--description", {"nargs": argparse.REMAINDER}),
            ],
        ),
        Command(
            "update",
            "Update info on a project",
            ["u"],
            [
                "name",
                "--project_name",
                "--github",
                "--run",
                ("--description", {"nargs": argparse.REMAINDER}),
            ],
        ),
        Command("add", "Add an existing project file", ["a"], ["directory"]),
        Command("delete", "Delete a project", ["d", "del", "rm", "remove"], ["name"]),
        Command(
            "list",
            "List all projects",
            ["l", "li", "all"],
            [("--tags", {"nargs": "+"})],
        ),
        Command(
            "search", "Search for a project", ["s", "find", "fetch", "info"], ["name"]
        ),
        Command("code", "Open project in VSC", ["vsc"], ["name"]),
        Command("file", "Open project in file explorer", ["explorer"], ["name"]),
        Command("debug", "Debug the project", [], ["operation"]),
        Command("dir", "Print dir of project", [], ["name"]),
        Command(
            "terminal", "Open terminal in project", ["ter"], ["name", "--type", "-t"]
        ),
        Command("run", "Run the project", ["r"], ["name", "-t"]),
        Command(
            "tree",
            "Print project tree",
            ["tr"],
            [
                "name",
                ("--ignore", {"nargs": "+"}),
                ("--max-depth", {"type": int}),
                ("--use-regex", {"action": "store_true"}),
            ],
        ),
        Command(
            "tag",
            "Add or manage tags for a project",
            ["t"],
            [
                "name",
                ("--add", {"nargs": "+"}),
                ("--remove", {"nargs": "+"}),
                ("--list", {"action": "store_true"}),
            ],
        ),
        Command(
            "note",
            "Add or remove notes from a project",
            ["n"],
            [
                "name",
                ("--add", {"nargs": "+"}),
                ("--remove", {"type": int, "nargs": "+"}),
                ("--list", {"action": "store_true"}),
            ],
        ),
    ]

    # Add each command to the parser
    for cmd in commands:
        parser_cmd = subparsers.add_parser(
            cmd.name, aliases=cmd.aliases, help=cmd.help_text
        )

        # Add arguments for the command
        if cmd.args:
            for arg in cmd.args:
                if isinstance(arg, str):
                    parser_cmd.add_argument(arg)
                elif isinstance(arg, tuple) and len(arg) == 2:
                    parser_cmd.add_argument(arg[0], **arg[1])
                else:
                    raise ValueError(f"Invalid argument format: {arg}")

    return parser.parse_args()
