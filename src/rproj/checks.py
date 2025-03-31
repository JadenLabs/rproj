import os
import argparse
from rproj import log
from rproj.info import search_project


def check_directory_exists(func):
    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        if not cmd_args.directory:
            log.err("Please provide a directory for the project")
            return
        if not os.path.exists(cmd_args.directory):
            log.err("Directory does not exist")
            return
        return func(cmd_args, *args, **kwargs)

    return wrapper


def check_project_exists(func):
    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        if not cmd_args.name:
            raise ValueError("Project name not found in kwargs")
        project = search_project(cmd_args.name)
        if not project:
            raise ValueError("Project not found")
        return func(cmd_args, *args, **kwargs)

    return wrapper
