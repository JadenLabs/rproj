import os
import toml
from rproj import FILE_EXTENSION
from rproj.projects import add_project_to_projects, remove_project_from_projects


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

        if "path" in kwargs:
            del kwargs["path"]

    def create(self):
        # Structure data and load into toml
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

        # Write to project file
        with open(self.path, "w") as file:
            file.write(data_str)

        add_project_to_projects(self)  # update projects.json

        return True

    def update_field(self, field: str, value):
        if hasattr(self, field):
            setattr(self, field, value)
            # Update the project file
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

            return True
        else:
            raise AttributeError(f"{field} is not a valid attribute")

    def delete(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        else:
            raise FileNotFoundError("File not found")
        remove_project_from_projects(self)  # update projects.json

    def __str__(self) -> str:
        description = f" | `{self.description}`" if self.description else ""
        github = f" | `{self.github}`" if self.github else ""
        return f"{self.project_name} @ {self.directory}{description}{github}"

    def list_view(self, i: int = None):
        prefix = f"{i}. " if i is not None else "- "
        empty_prefix = " " * len(prefix)

        details = []
        if self.description:
            details.append(f"- [dim]{self.description}[/]")
        if self.github:
            details.append(f"\n{empty_prefix}[dim]github:[/] {self.github}")
        details_str = "".join(details)

        return f"{prefix}[bright_blue]{self.project_name}[/] @ [yellow]{self.directory}[/] {details_str}".strip()
