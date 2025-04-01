import os
from rproj.file import RProjFile
from rproj.info import search_project
from rproj import log, FILE_EXTENSION
from rproj.projects import add_project_to_projects, PROJECT_DATA_PATH
from rproj.launching import launch_vsc, launch_file_explorer, launch_terminal
from rproj.checks import check_project_exists, check_directory_exists, check_project_already_exists

@check_project_already_exists
def handle_create(args):
    log.info("Creating project...")
    description = " ".join(args.description) if args.description else ""
    RProjFile(args.name, args.directory, description).create()

@check_project_exists
def handle_update(args):
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

    add_project_to_projects(project)

@check_project_exists
def handle_delete(args):
    log.info("Deleting project...")
    search_project(args.name).delete()

@check_project_exists
def handle_search(args):
    log.info("Searching project...")
    search_project(args.name).print_details()

@check_project_exists
def handle_code(args):
    log.info("Opening project in VSC...")
    launch_vsc(search_project(args.name).directory)

@check_project_exists
def handle_file_explorer(args):
    log.info("Opening project in file explorer...")
    launch_file_explorer(search_project(args.name).directory)

@check_project_exists
def handle_dir(args):
    # Prints the directory of the project
    # ex: cd "$(python ./src dir ...)"
    project = search_project(args.name)
    if project and os.path.isdir(project.directory):
        print(project.directory)

@check_project_exists
def handle_terminal(args):
    log.info("Opening project in terminal...")
    terminal_type = args.type or args.t or "ps"
    launch_terminal(search_project(args.name).directory, terminal_type)

def handle_debug(args):
    if args.operation == "projects":
        log.info(f"Project data at {PROJECT_DATA_PATH}\n      Dir: {PROJECT_DATA_PATH.removesuffix('projects.json')}")
