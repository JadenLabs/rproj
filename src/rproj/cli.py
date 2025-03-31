import argparse


class Command:
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
    """Get command line arguments"""
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
            ["name", "directory", ("--description", {"nargs": argparse.REMAINDER})],
        ),
        Command("add", "Add an existing project file", ["a"], ["directory"]),
        Command("delete", "Delete a project", ["d", "del", "rm", "remove"], ["name"]),
        Command("list", "List all projects", ["l", "li", "all"], []),
        Command("search", "Search for a project", ["s", "find", "fetch"], ["name"]),
        Command("code", "Open project in VSC", ["vsc"], ["name"]),
        Command("file", "Open project in file explorer", ["explorer"], ["name"]),
        Command("debug", "Debug the project", [], ["operation"]),

        # TODO add update
        # TODO add zip
        # TODO add unzip (and unzip add to projects)
        # TODO add git clone support (maybe using pipe?)
        # TODO add run project
    ]

    for cmd in commands:
        parser_cmd = subparsers.add_parser(
            cmd.name, aliases=cmd.aliases, help=cmd.help_text
        )

        if cmd.args:
            for arg in cmd.args:
                if isinstance(arg, str):
                    parser_cmd.add_argument(arg)
                elif isinstance(arg, tuple) and len(arg) == 2:
                    parser_cmd.add_argument(arg[0], **arg[1])
                else:
                    raise ValueError(f"Invalid argument format: {arg}")

    return parser.parse_args()
