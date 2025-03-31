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
    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        if not os.path.exists(cmd_args.directory):
            log.err("Directory does not exist")
            return
        return func(cmd_args, *args, **kwargs)

    return wrapper


def check_project_exists(func):
    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        project = search_project(cmd_args.name)
        if not project:
            log.err("Project not found")
            return
        return func(cmd_args, *args, **kwargs)

    return wrapper


def check_project_already_exists(func):
    def wrapper(cmd_args: argparse.Namespace, *args, **kwargs):
        project = search_project(cmd_args.name)
        if project:
            log.err("Project name already exists")
            return
        return func(cmd_args, *args, **kwargs)

    return wrapper
