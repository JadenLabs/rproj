import os
import json
from appdirs import user_data_dir
from rproj import log


def get_project_data_path():
    """Get the path to the project data file using appdirs."""
    data_dir = user_data_dir(appname="rproj", appauthor="JadenLabs")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "projects.json")


PROJECT_DATA_PATH = get_project_data_path()


def reset_project_data_file():
    with open(PROJECT_DATA_PATH, "w") as file:
        log.warn("Resetting project data file")
        file.write(json.dumps([]))
        return True


def validate_project_data_file():
    if not os.path.exists(PROJECT_DATA_PATH):
        log.warn("Project data file not found")
        reset_project_data_file()
        return True
    elif os.path.getsize(PROJECT_DATA_PATH) == 0:
        log.warn("No project data found")
        reset_project_data_file()
        return True

    with open(PROJECT_DATA_PATH, "r") as file:
        file = file.read()
        if file != "[]":
            try:
                json.loads(file)
            except json.JSONDecodeError:
                log.warn("Could not read project data file")
                reset_project_data_file()
                return True
            else:
                return False


def add_project_to_projects(project):
    # Get a list of all project paths
    with open(PROJECT_DATA_PATH, "r") as file:
        project_paths = json.loads(file.read()) or []

    # Add the new project path to the list
    project_paths.append(project.path)
    project_paths = list(set(project_paths))

    # Update the project data file
    with open(PROJECT_DATA_PATH, "w") as file:
        file.write(json.dumps(project_paths))

    log.info(f"Added project {project.project_name} to projects")


def remove_project_from_projects(project):
    # Get a list of all project paths
    with open(PROJECT_DATA_PATH, "r") as file:
        project_paths: list = json.loads(file.read())
        project_paths.remove(project.path)

    # Update the project data file
    with open(PROJECT_DATA_PATH, "w") as file:
        file.write(json.dumps(project_paths))

    log.info(f"Removed project {project.project_name} from projects")
