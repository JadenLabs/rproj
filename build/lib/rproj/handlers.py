import os
from rproj.utils import log
from rproj import FILE_EXTENSION
from rproj.utils.file import RProjFile
from rproj.utils.info import search_project
from rproj.utils.tree import print_project_structure
from rproj.utils.projects import add_project_to_projects, PROJECT_DATA_PATH
from rproj.utils.launching import launch_vsc, launch_file_explorer, launch_terminal
from rproj.utils.checks import (
    check_project_exists,
    check_directory_exists,
    check_project_already_exists,
)


@check_project_already_exists
def handle_create(args):
    """Creates a new project with the given name and description."""
    log.info("Creating project...")
    description = " ".join(args.description) if args.description else ""
    github = args.github if args.github else ""
    run_cmd = args.run if args.run else ""
    RProjFile(args.name, args.directory, description, github, run_cmd).create()


@check_project_exists
def handle_update(args):
    """Updates the project with the given name."""
    log.info("Updating project...")
    project = search_project(args.name)
    if args.project_name:
        project.update_field("project_name", args.project_name)
    if args.description:
        project.update_field("description", " ".join(args.description))
    if args.github:
        project.update_field("github", args.github)
    if args.run:
        project.update_field("run_cmd", args.run)


@check_directory_exists
def handle_add(args):
    """Adds an existing rproj project to the projects.json file."""
    log.info("Adding project...")
    path = os.path.abspath(os.path.join(args.directory, FILE_EXTENSION))
    try:
        project = RProjFile.load(path)
    except FileNotFoundError:
        log.err("Project file not found")
        return

    if search_project(project.project_name):
        log.err("Project name already exists")
        return

    add_project_to_projects(project)  # Update projects.json


@check_project_exists
def handle_delete(args):
    """Deletes the project with the given name."""
    log.info("Deleting project...")
    search_project(args.name).delete()


@check_project_exists
def handle_search(args):
    """Searches for the project with the given name."""
    log.info("Searching project...")
    search_project(args.name).print_details()


@check_project_exists
def handle_code(args):
    """Opens the project in Visual Studio Code."""
    # TODO Add support for other editors
    log.info("Opening project in VSC...")
    launch_vsc(search_project(args.name).directory)


@check_project_exists
def handle_file_explorer(args):
    """Opens the project in the file explorer."""
    log.info("Opening project in file explorer...")
    launch_file_explorer(search_project(args.name).directory)


@check_project_exists
def handle_dir(args):
    """Prints the directory of the project."""
    # Prints the directory of the project
    # ex: cd "$(python ./src dir ...)"
    project = search_project(args.name)
    if project and os.path.isdir(project.directory):
        print(project.directory)


@check_project_exists
def handle_terminal(args):
    """Opens the project in the terminal."""
    log.info("Opening project in terminal...")
    terminal_type = args.type or args.t or "ps"
    launch_terminal(search_project(args.name).directory, terminal_type)


@check_project_exists
def handle_run(args):
    """Runs the project."""
    log.info("Running project...")
    project = search_project(args.name)
    if not project.run_cmd:
        log.err("No run command found in project")
        return

    launch_terminal(
        search_project(args.name).directory,
        args.t or "ps",
        command=project.run_cmd,
    )

def handle_debug(args):
    """Handles debugging commands."""
    if args.operation == "projects":
        log.info(
            f"Project data at {PROJECT_DATA_PATH}\n      Dir: {PROJECT_DATA_PATH.removesuffix('projects.json')}"
        )

@check_project_exists
def handle_tree(args):
    """Prints the project tree."""
    log.info("Printing project tree...")
    project = search_project(args.name)
    if not project or not os.path.isdir(project.directory):
        log.err("Project directory not found")
        return

    ignore = []
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            ignore = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    if args.ignore:
        ignore.append(*args.ignore)
    ignore.append(".git")  # Always ignore

    print_project_structure(project.directory, max_depth=5, ignore=ignore)
