import os
import toml
import json
from appdirs import user_data_dir
from rproj import log, FILE_EXTENSION


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


class RProjFile:
    def load(path):
        with open(path, "r") as file:
            data_raw = file.read()
            if data_raw == "":
                raise ValueError("File is empty")

            data = toml.loads(data_raw)
            kwargs = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        kwargs[k] = v
                else:
                    kwargs[key] = value

            if kwargs == {}:
                raise ValueError("No valid data found")

            return RProjFile(**kwargs)

    def __init__(
        self,
        project_name: str,
        directory: str,
        description: str = "",
        github: str = "",
        **kwargs,
    ) -> None:
        self.project_name = project_name
        self.directory = os.path.abspath(directory)
        self.path = os.path.abspath(os.path.join(directory, FILE_EXTENSION))
        self.description = description
        self.github = github
        self.kwargs = kwargs

    def create(self):
        data = {
            "info": {
                "project_name": self.project_name,
                "description": self.description,
            },
            "file": {
                "directory": self.directory,
                "path": self.path,
            },
            "other": {
                "github": self.github,
            },
        }
        data["other"].update(self.kwargs)
        data_str = toml.dumps(data)

        with open(self.path, "w") as file:
            file.write(data_str)

        # update project data file
        with open(PROJECT_DATA_PATH, "r") as file:
            project_paths = json.loads(file.read()) or []
            project_paths.append(self.path)
            project_paths = list(set(project_paths))  # remove duplicates
        with open(PROJECT_DATA_PATH, "w") as file:
            file.write(json.dumps(project_paths))

        return True

    def delete(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        else:
            raise FileNotFoundError("File not found")

        # update project data file
        with open(PROJECT_DATA_PATH, "r") as file:
            project_paths: list = json.loads(file.read())
            project_paths.remove(self.path)
        with open(PROJECT_DATA_PATH, "w") as file:
            file.write(json.dumps(project_paths))

    def __str__(self) -> str:
        description = f" | `{self.description}`" if self.description else ""
        github = f" | `{self.github}`" if self.github else ""
        return f"{self.project_name} @ {self.directory}{description}{github}"

    def list_view(self, i: int = None):
        prefix = f"{i} - " if i is not None else " - "
        padding = " " * len(prefix)
        description = (
            f"\n{padding}[black]desc:[/] {self.description}" if self.description else ""
        )
        github = f"\n{padding}[black]github:[/] {self.github}" if self.github else ""
        return f"{prefix}{self.project_name} @ [yellow]{self.directory}[/]{description}{github}"


if __name__ == "__main__":
    # * run as `python -m utils.file`
    file = RProjFile("test", "testing/", "test", "test")
    file.create()

    file = RProjFile.load("testing/.rproj")
    print(file.project_name)
