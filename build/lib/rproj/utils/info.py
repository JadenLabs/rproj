import json
from rich import print
from rproj.utils.file import RProjFile
from rproj.utils.projects import PROJECT_DATA_PATH


def load_projects():
    """Load all projects from the projects.json file"""
    with open(PROJECT_DATA_PATH, "r") as file:
        project_paths = json.loads(file.read())

    projects: list[RProjFile] = []
    for path in project_paths:
        try:
            project = RProjFile.load(path)
            projects.append(project)
        except Exception as e:
            continue

    return projects


def list_projects():
    """List all projects in the projects.json file"""
    projects = load_projects()
    for i, project in enumerate(projects):
        print(project.list_view(i))


def search_project(name: str = None):
    """Search for a project by name"""
    if not name:
        raise ValueError("Please provide a name to search for")

    projects = load_projects()
    for project in projects:
        if name == project.project_name:
            return project

    return False
