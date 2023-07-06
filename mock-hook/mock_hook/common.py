import os
import sys
import json
import importlib


def read_data(file_path: str = None) -> dict:
    """
    read JSON data file.
    """
    if file_path is None:
        return {}

    with open(file_path, "r+", encoding="utf-8") as json_file:
        req_data = json.load(json_file)
        return req_data


def loader(func_name: str = "response_hook", file_name: str = "confrun.py", *args, **kwargs):
    """
    Execute the hook function dynamically.
    :param func_name: function name
    :param file_name: hook file name
    """
    # By default, confrun.py files are searched in the current directory
    file_dir = os.getcwd()
    sys.path.insert(0, file_dir)
    all_hook_files = list(filter(lambda x: x.endswith(file_name), os.listdir(file_dir)))
    all_hook_module = list(map(lambda x: x.replace(".py", ""), all_hook_files))

    hooks = []
    for module_name in all_hook_module:
        hooks.append(importlib.import_module(module_name))

    # Execute the function according to the  name
    for per_hook in hooks:
        try:
            func = getattr(per_hook, func_name)
            return func(*args, **kwargs)
        except AttributeError:
            return None

