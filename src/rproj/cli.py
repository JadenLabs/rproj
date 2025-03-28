import os
import json
import argparse
from rproj import log, FILE_EXTENSION
from rproj.file import RProjFile, validate_project_data_file, PROJECT_DATA_PATH
from rproj.info import list_projects, search_project
from rproj.launching import launch_vsc, launch_file_explorer


def get_args():
    """Get command line arguments"""
    parser = argparse.ArgumentParser(
        prog="rproj", description="Create, manage, and view your projects"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create subcommand
    create_parser = subparsers.add_parser(
        "create", aliases=["c", "make"], help="Create a new project"
    )
    create_parser.add_argument("name", help="Name of the project")
    create_parser.add_argument(
        "directory", help="Path to the project directory enclosed in quotes"
    )
    create_parser.add_argument(
        "-desc",
        "--description",
        help="Description of the project",
        nargs=argparse.REMAINDER,
    )

    # Add subcommand
    add_parser = subparsers.add_parser(
        "add", aliases=["a"], help="Add an existing project file"
    )
    add_parser.add_argument("directory", help="The directory of the project.")

    # Delete subcommand
    delete_parser = subparsers.add_parser(
        "delete", aliases=["d", "del", "rm", "remove"], help="Delete a project"
    )
    delete_parser.add_argument("name", help="Name of the project")

    # List subcommand
    subparsers.add_parser("list", aliases=["l", "li", "all"], help="List all projects")

    # Search subcommand
    search_parser = subparsers.add_parser(
        "search", aliases=["s", "find", "fetch"], help="Search for a project"
    )
    search_parser.add_argument("name", help="Name of the project")

    # Code subcommand
    code_parser = subparsers.add_parser(
        "code", aliases=["vsc"], help="Open project in VSC"
    )
    code_parser.add_argument("name", help="Name of the project")

    # File explorer subcommand
    file_parser = subparsers.add_parser(
        "file", aliases=["explorer"], help="Open project in file explorer"
    )
    file_parser.add_argument("name", help="Name of the project")

    # Debug subcommands
    debug_parser = subparsers.add_parser("debug", help="Debug the project")
    debug_parser.add_argument(
        "operation", help="Operation to perform", choices=["projects"]
    )

    return parser.parse_args()


def handle_create(args: argparse.Namespace):
    # check if name and directory provided
    if not args.name or not args.directory:
        log.err("Please provide a name and directory for the project")
        return
    if search_project(args.name):
        log.err("Project name already exists")
        return

    log.info("Creating project...")
    description = " ".join(args.description) if args.description else ""

    project = RProjFile(
        project_name=args.name, directory=args.directory, description=description
    )
    project.create()


def handle_add(args: argparse.Namespace):
    if not args.directory:
        log.err("Please provide a directory for the project")
        return
    if not os.path.exists(args.directory):
        log.err("Directory does not exist")
        return

    log.info("Adding project...")
    path = os.path.abspath(os.path.join(args.directory, FILE_EXTENSION))
    try:
        project = RProjFile.load(path)
    except FileNotFoundError:
        log.err("Project file not found")

    if search_project(project.project_name):
        log.err("Project name already exists")
        return

    with open(PROJECT_DATA_PATH, "r") as file:
        project_paths = json.loads(file.read()) or []
        project_paths.append(project.path)
        project_paths = list(set(project_paths))
    with open(PROJECT_DATA_PATH, "w") as file:
        file.write(json.dumps(project_paths))


def handle_delete(args: argparse.Namespace):
    if not args.name:
        log.err("Please provide a name for the project")
        return

    log.info("Deleting project...")
    project = search_project(args.name)
    if project is False:
        log.err("Project not found")
        return
    project.delete()


def handle_search(args: argparse.Namespace):
    if not args.name:
        log.err("Please provide a name for the project")
        return

    log.info("Searching project...")
    project = search_project(args.name)
    if project is False:
        log.err("Project not found")
        return
    print(project)


def handle_code(args: argparse.Namespace):
    if not args.name:
        log.err("Please provide a name for the project")
        return

    log.info("Opening project in VSC...")
    project = search_project(args.name)
    if project is False:
        log.err("Project not found")
        return
    launch_vsc(project.directory)


def handle_file_explorer(args: argparse.Namespace):
    if not args.name:
        log.err("Please provide a name for the project")
        return

    log.info("Opening project in file explorer...")
    project = search_project(args.name)
    if project is False:
        log.err("Project not found")
        return

    launch_file_explorer(project.directory)


def handle_args(args: argparse.Namespace):
    """Handle command line arguments"""
    # === handle operations
    match args.command:
        case "create" | "c" | "make":
            handle_create(args)
        case "delete" | "d" | "del" | "rm" | "remove":
            handle_delete(args)
        case "list" | "l" | "li" | "all":
            log.info("Listing projects...")
            list_projects()
        case "search" | "s" | "find" | "fetch":
            handle_search(args)
        case "code" | "vsc":
            handle_code(args)
        case "file" | "explorer":
            handle_file_explorer(args)
        case "add" | "a":
            handle_add(args)
        case "debug":
            if args.operation == "projects":
                data_dir = PROJECT_DATA_PATH.removesuffix("projects.json")
                log.info(f"Project data at {PROJECT_DATA_PATH}\n      Dir: {data_dir}")

        # TODO add update
        # TODO add zip
        # TODO add unzip (and unzip add to projects)
        # TODO add git clone support (maybe using pipe?)
        # TODO add run project


def main():
    validate_project_data_file()
    args = get_args()
    handle_args(args)


if __name__ == "__main__":
    main()
