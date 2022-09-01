import os, sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def lang_to_dict(file: str):
    """
    Convert a lang file to a dict.
    """
    lines = {}

    for line in file.split("\n"):
        if line.startswith("#"):
            continue
        line = line.split("=", 1)
        if len(line) == 2:
            lines[line[0]] = line[1]

    return dict(lines)


def dict_to_lang(d: dict):
    """
    Convert a dict to a lang file.
    """
    lines = []
    for key, value in d.items():
        lines.append(f"{key}={value}")
    return "\n".join(lines)

def invert_dict(d: dict):
    """
    Invert a dict.
    """
    new_dict = {}
    for key, value in d.items():
        new_dict[value] = key
    return new_dict