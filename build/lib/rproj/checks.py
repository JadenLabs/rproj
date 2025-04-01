import os
import argparse
from rproj import log
from rproj.info import search_project


# Not needed for now because argparse will handle this - I hope
# def check_args_exist(req_args: list):
#     def d(func):
#         def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
#             missing_args = [arg for arg in req_args if not getattr(cmd_args, arg)]
#             if missing_args:
#                 log.err(f"Missing arguments: {', '.join(missing_args)}")
#                 return
#             return func(cmd_args, *args, **kwargs)
#         return wrapper
#     return d


def check_directory_exists(func):
    """
    A decorator that checks if the directory specified in the `directory` attribute
    of the `argparse.Namespace` object exists.\n
    ---
    If the directory does not exist,
    logs an error message and prevents the wrapped function from being executed.
    Args:
        func (Callable): The function to be wrapped by the decorator.
    Returns:
        Callable: The wrapped function that includes the directory existence check.
    Example:
        ```
        @check_directory_exists
        def some_function(cmd_args: argparse.Namespace):
            # Function implementation
        ```
    """

    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        if not os.path.exists(cmd_args.directory):
            log.err("Directory does not exist")
            return
        return func(cmd_args, *args, **kwargs)

    return wrapper


def check_project_exists(func):
    """
    Decorator to check if a project exists.\n
    ---
    This decorator takes a function and ensures that the project specified in the
    command-line arguments exists. If the project does not exist, it logs an error
    message and prevents the wrapped function from being executed.
    Args:
        func (Callable): The function to be wrapped by the decorator.
    Returns:
        Callable: The wrapped function that includes the project existence check.
    Example:
        ```
        @check_project_exists
        def some_function(cmd_args):
            # Function logic here
        ```
    """

    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        project = search_project(cmd_args.name)
        if not project:
            log.err("Project not found")
            return
        return func(cmd_args, *args, **kwargs)

    return wrapper


def check_project_already_exists(func):
    """
    Decorator to check if a project with the given name already exists.\n
    ---
    This decorator wraps a function and ensures that a project with the specified
    name does not already exist before proceeding. If a project with the same name
    is found, an error message is logged, and the wrapped function is not executed.
    Args:
        func (Callable): The function to be wrapped by the decorator.
    Returns:
        Callable: The wrapped function. If a project with the same name exists,
                  the wrapped function is not executed and `None` is returned.
    Example:
        ```
        @check_project_already_exists
        def some_function(cmd_args):
            # Function logic here
        ```
    """

    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        project = search_project(cmd_args.name)
        if project:
            log.err("Project name already exists")
            return
        return func(cmd_args, *args, **kwargs)

    return wrapper
