from rproj.utils import log
from rproj.cli import get_args
from rproj.utils.info import list_projects
from rproj.utils.projects import validate_project_data_file
from rproj.handlers import (
    handle_create,
    handle_add,
    handle_delete,
    handle_search,
    handle_code,
    handle_file_explorer,
    handle_debug,
    handle_update,
    handle_dir,
    handle_terminal,
    handle_run,
)

COMMAND_HANDLERS = {
    "create": handle_create,
    "c": handle_create,
    "update": handle_update,
    "u": handle_update,
    "make": handle_create,
    "add": handle_add,
    "a": handle_add,
    "delete": handle_delete,
    "d": handle_delete,
    "del": handle_delete,
    "rm": handle_delete,
    "remove": handle_delete,
    "search": handle_search,
    "s": handle_search,
    "find": handle_search,
    "fetch": handle_search,
    "info": handle_search,
    "code": handle_code,
    "vsc": handle_code,
    "file": handle_file_explorer,
    "explorer": handle_file_explorer,
    "dir": handle_dir,
    "debug": handle_debug,
    "terminal": handle_terminal,
    "ter": handle_terminal,
    "run": handle_run,
}


def handle_args(args):
    """Handle command line arguments"""
    if args.command in COMMAND_HANDLERS:
        COMMAND_HANDLERS[args.command](args)
    elif args.command in ["list", "l", "li", "all"]:
        log.info("Listing projects...")
        list_projects()


def main():
    validate_project_data_file()
    args = get_args()
    handle_args(args)


if __name__ == "__main__":
    main()
