import os, sys, shutil, json, zipfile
from distutils.dir_util import copy_tree


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
    lines = file.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line and not line.startswith("#")]
    lines = [line.split("=", 1) for line in lines]
    lines = [(line[0], line[1]) for line in lines]
    return dict(lines)


def dict_to_lang(d: dict):
    """
    Convert a dict to a lang file.
    """
    lines = []
    for key, value in d.items():
        lines.append(f"{key}={value}")
    return "\n".join(lines)


def convert(path: str, invert: bool = False):
    """
    Convert a pack file to a new format.
    :param path: The path to the pack file.
    :param invert: Whether to invert the colors.
    """

    if not os.path.isdir(path):
        print(f"{path} is not a directory.")
        return


    copy_tree(path, path + "-blood")
    path = path + "-blood"
    

    required_dirs = ["lang", "textures/items", "textures/blocks", "textures/models/armor"]

    for dir in required_dirs:
        full_dir = os.path.join(path, "assets/minecraft", dir)
        if not os.path.isdir(full_dir):
            os.mkdir(full_dir)




    # Convert lang files.
    
    for pala, mc in lang_path.items():

        pala_lang_file = os.path.join(path, pala)
        mc_lang_file = os.path.join(path, mc)

        if os.path.isfile(pala_lang_file):

            with open(pala_lang_file, "r") as f:
                lang_dict = lang_to_dict(f.read())


            if os.path.isfile(mc_lang_file):
                with open(mc_lang_file, "r") as f:
                    new_lang_dict = lang_to_dict(f.read())

            else:
                new_lang_dict = {}
    
            

            for key, item in lang_dict.items():
                if key in items.keys():
                    new_lang_dict[items[key]] = item

            with open(mc_lang_file, "w+") as f:
                f.write(dict_to_lang(new_lang_dict))


    # Convert the textures.

    for pala_asset, blood_asset in assets.items():

        for ext in [".png", ".mcmeta", ".properties"]:
            pala_asset_file = os.path.join(path, "assets", pala_asset + ext)
            print(pala_asset_file)
            blood_asset_file = os.path.join(path, "assets", blood_asset + ext)

            if os.path.isfile(pala_asset_file):
                print(1)
                shutil.copyfile(pala_asset_file, blood_asset_file)



with open(resource_path("assets.json"), "r") as f:
    assets: dict = json.load(f)

with open(resource_path("items.json"), "r") as f:
    items: dict = json.load(f)

lang_path = {
    "assets/palamod/lang/en_US.lang": "assets/minecraft/lang/en_US.lang",
    "assets/palamod/lang/fr_FR.lang": "assets/minecraft/lang/fr_FR.lang",
}