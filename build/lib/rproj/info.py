import json
from rich import print
from rproj.file import RProjFile, PROJECT_DATA_PATH

def load_projects():
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
    projects = load_projects()
    for i, project in enumerate(projects):
        print(project.list_view(i))


def search_project(name: str = None):
    if not name:
        raise ValueError("Please provide a name to search for")

    projects = load_projects()
    for project in projects:
        if name == project.project_name:
            return project

    return False


if __name__ == "__main__":
    list_projects()
