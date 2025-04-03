import os
import toml
from rich import print
from rproj import FILE_EXTENSION
from rproj.utils.projects import add_project_to_projects, remove_project_from_projects


class RProjFile:
    """
    RProjFile is a class for managing project files in a structured format. It provides
    methods for creating, loading, updating, and deleting project files, as well as
    utility methods for displaying project details.
    Attributes:
        project_name (str): The name of the project.
        directory (str): The directory where the project is located.
        description (str): A brief description of the project (optional).
        github (str): The GitHub repository URL for the project (optional).
        run_cmd (str): The command to run the project (optional).
        kwargs (dict): Additional key-value pairs for custom attributes.
    """

    def load(path: str) -> "RProjFile":
        """Loads a project file from the specified path and returns an RProjFile object.

        Args:
            path (str): The path to the project file.

        Raises:
            ValueError: If the file does not exist.
            ValueError: If the file is empty or contains no valid data.

        Returns:
            RRprojFile: An instance of the RProjFile class with the loaded data.
        """
        with open(path, "r") as file:
            # Check if the file exists and is not empty
            if not os.path.exists(path):
                raise ValueError("File does not exist")
            data_raw = file.read()
            if data_raw == "":
                raise ValueError("File is empty")

            # Parse the TOML data and load it into a dictionary of kwargs
            data = toml.loads(data_raw)
            kwargs = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        kwargs[k] = v
                elif isinstance(value, list):
                    kwargs[key] = value
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
        run_cmd: str = "",
        notes: list[str] = [],
        **kwargs,
    ) -> None:
        self.project_name = project_name
        self.directory = os.path.abspath(directory)
        self.path = os.path.abspath(os.path.join(directory, FILE_EXTENSION))
        self.description = description
        self.github = github
        self.run_cmd = run_cmd
        self.notes = notes
        self.kwargs = kwargs

        # Remove "path" from kwargs if it exists
        # This is to prevent overwriting the path attribute
        if "path" in kwargs:
            del kwargs["path"]

    def create(self):
        """Creates a new project file with the specified attributes."""
        # Load data into TOML format
        data_str = toml.dumps(self.as_dict())

        # Write to project file
        with open(self.path, "w") as file:
            file.write(data_str)

        add_project_to_projects(self)  # update projects.json

        return True

    def update_field(self, field: str, value):
        """
        Updates the value of a specified field in the object and writes the changes.

        Args:
            field (str): The name of the attribute to update.
            value: The new value to assign to the specified attribute.
        Raises:
            AttributeError: If the specified field does not exist in the object.
        Returns:
            bool: True if the field was successfully updated.
        """

        if hasattr(self, field):
            setattr(self, field, value)
            # Update the project file
            data_str = toml.dumps(self.as_dict())

            with open(self.path, "w") as file:
                file.write(data_str)

            return True
        else:
            raise AttributeError(f"{field} is not a valid attribute")

    def delete(self):
        """Deletes the project file and removes it from the projects list."""
        # Remove the project file
        if os.path.exists(self.path):
            os.remove(self.path)
        else:
            raise FileNotFoundError("File not found")
        remove_project_from_projects(self)  # update projects.json

    def print_details(self):
        """Prints formatted details of the project."""
        lines = [
            f"[bright_blue]Project Name:[/] {self.project_name}",
            (
                f"[bright_blue]Description:[/] [bright_black]{self.description}[/]"
                if self.description
                else ""
            ),
            f"[bright_blue]Directory:[/] [yellow]{self.directory}[/]",
            f"[bright_blue]Path:[/] [yellow]{self.path}[/]",
            f"[bright_blue]GitHub:[/] {self.github}" if self.github else "",
            f"[bright_blue]Run Command:[/] {self.run_cmd}" if self.run_cmd else "",
        ]
        print("\n".join(line for line in lines if line))

    def list_view(self, i: int = None):
        """Returns a formatted string for listing the projects."""
        prefix = f"{i}. " if i is not None else "- "
        empty_prefix = " " * len(prefix)

        details = []
        if self.description:
            details.append(f"- [dim]{self.description}[/]")
        if self.github:
            details.append(f"\n{empty_prefix}[dim]github:[/] {self.github}")
        details_str = "".join(details)

        return f"{prefix}[bright_blue]{self.project_name}[/] @ [yellow]{self.directory}[/] {details_str}".strip()

    def as_dict(self):
        """Converts the object attributes into a dictionary format."""
        data = {
            "info": {
                "project_name": self.project_name,
                "description": self.description,
                "directory": self.directory,
            },
            "other": {
                "github": self.github,
                "run_cmd": self.run_cmd,
                "notes": self.notes,
            },
        }
        data["other"].update(self.kwargs)

        return data

    def __str__(self) -> str:
        description = f" | `{self.description}`" if self.description else ""
        github = f" | `{self.github}`" if self.github else ""
        return f"{self.project_name} @ {self.directory}{description}{github}"
