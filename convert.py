from functions import *
from typing_extensions import Literal
import os, shutil, json


def convert(path: str, to: Literal["pala", "blood"]):
    """
    Convert a pack file to a new format.
    :param path: The path to the pack file.
    :param invert: Whether to invert the colors.
    """

    with open(resource_path("src/assets.json"), "r") as f:
        assets: dict = json.load(f)
        if to == "pala":
            assets = invert_dict(assets)

    with open(resource_path("src/items.json"), "r") as f:
        items: dict = json.load(f)
        if to == "pala":
            items = invert_dict(items)


    lang_path = {
        "assets/palamod/lang/en_US.lang": "assets/minecraft/lang/en_US.lang",
        "assets/palamod/lang/fr_FR.lang": "assets/minecraft/lang/fr_FR.lang",
    }
    if to == "pala":
        lang_path = invert_dict(lang_path)

    

    if to == "blood":

        required_dirs = ["lang", "textures/items", "textures/blocks", "textures/models/armor"]

        for dir in required_dirs:
            full_dir = os.path.join(path, "assets/minecraft", dir)
            if not os.path.isdir(full_dir):
                os.makedirs(full_dir)

    else:

        required_dirs = ["lang", "textures/items/weapons", "textures/blocks", "textures/models"]

        for dir in required_dirs:
            full_dir = os.path.join(path, "assets/palamod", dir)
            if not os.path.isdir(full_dir):
                os.makedirs(full_dir)




    # Convert lang files.
    
    for lang_file, new_lang_file in lang_path.items():

        pala_lang_file = os.path.join(path, lang_file)
        mc_lang_file = os.path.join(path, new_lang_file)

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

    for asset, new_asset in assets.items():

        for ext in [".png", ".png.mcmeta", ".properties"]:
            asset_file = os.path.join(path, "assets", asset + ext)
            new_asset_file = os.path.join(path, "assets", new_asset + ext)

            if os.path.isfile(asset_file):
                if os.path.isfile(new_asset_file):
                    os.remove(new_asset_file)
                shutil.copyfile(asset_file, new_asset_file)


    credits_file = os.path.join(path, "credits.txt")
    credit = "Pack converti par BloodPackConverter, https://github.com/crazycat256/BloodPackConverter"

    if not os.path.isfile(credits_file):
        with open(credits_file, "w+") as f:
            f.write(credit)

    else:
        with open(credits_file, "r") as f:
            credits = f.read()

        if credit not in credits:
            with open(credits_file, "a") as f:
                f.write(credit)
