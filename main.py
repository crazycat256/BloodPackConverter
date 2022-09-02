import traceback
from convert import convert
from functions import *
from tkinter import *
from typing_extensions import Literal
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.font import Font
from distutils.dir_util import copy_tree
import webbrowser, shutil, tempfile

status_dic = {
    "blood": "Paladium vers Bloodshed",
    "pala": "Bloodshed vers Paladium",
}

class ToggleButton(Button):
    def __init__(self):
        Button.__init__(self, mode_frame, command=self.toggle, text=status_dic["blood"])
        self.status = "blood"

    def toggle(self):
        self.status = "blood" if self.status == "pala" else "pala"
        self.config(text=status_dic[self.status])


def open_url(url):
    webbrowser.open(url)

def select_file():
    path_entry.delete(0, END)
    path_entry.insert(0, askopenfilename(filetypes=(("Archive zip", "*.zip"),)))

def select_folder():
    path_entry.delete(0, END)
    path_entry.insert(0, askdirectory())


def run(path: str, status: Literal["pala", "blood"]):
    
    error_label.pack_forget()
    success_label.pack_forget()

    if (not os.path.isfile(path) and not path.endswith(".zip")) and (not os.path.isdir(path)):
        error_label.config(text="Le pack doit être sous forme de dossier ou d'archive ZIP")
        error_label.pack()
        return

    new_path = path.removesuffix(".zip") + "-converted"

    if os.path.exists(new_path) or os.path.exists(new_path + ".zip"):
        error_label.config(text="Il y a déjà un pack à la destination de sortie")
        error_label.pack()
        return

    with tempfile.TemporaryDirectory() as tempdir:

        temp_path = os.path.join(tempdir, "temp-pack")


        if os.path.isfile(path):
            zipped = True
            try:
                shutil.unpack_archive(path, temp_path)
            except:
                error_label.config(text="Erreur lors de l'extraction de l'archive zip")
                error_label.pack()
                return

        else:
            zipped = False
            copy_tree(path, temp_path)


        required_files = ["pack.png", "pack.mcmeta", "assets"]
        for file in required_files:
            if not os.path.exists(os.path.join(temp_path, file)):
                error_label.config(text="Le pack est invalide")
                error_label.pack()
                shutil.rmtree(temp_path)
                return
        

        try:
            convert(temp_path, status)

            if zipped:
                shutil.make_archive(new_path, 'zip', temp_path)
            else:
                copy_tree(temp_path, new_path)
            shutil.rmtree(temp_path)

            success_label.config(text="Pack converti\n" + os.path.abspath(new_path))
            success_label.pack()
        except:
            traceback.print_exc()
            error_label.config(text="Une erreur inattendue est survenue")
            error_label.pack()

    




root = Tk()
root.title("BloodPackConverter")
root.geometry("500x300")
root.wm_maxsize(1000, 600)
root.wm_minsize(500, 300)
root.iconbitmap(resource_path("src/icon.ico")) # https://www.flaticon.com/fr/icones-gratuites/convertir

title = Label(root, text="BloodPackConverter", font=("Arial", 20))
title.pack()

subtitle = Label(root, text="By crazycat256", font=("Helveticabold", 10), fg="blue", cursor="hand2")
subtitle.bind("<Button-1>", lambda e: open_url("https://github.com/crazycat256/BloodPackConverter"))
subtitle.pack()


path_frame = Frame(root)

path_entry = Entry(path_frame, width=60)
path_entry.pack(side=LEFT)

zip_file_image = PhotoImage(file=resource_path("src/zip.png")).subsample(32) # https://www.flaticon.com/free-icons/zip
folder_image = PhotoImage(file=resource_path("src/folder.png")).subsample(32) # https://www.flaticon.com/free-icons/zip

browse_zip_button = Button(path_frame, image=zip_file_image,command=select_file)
browse_zip_button.pack(side=LEFT)
browse_folder_button = Button(path_frame, image=folder_image, command=select_folder)
browse_folder_button.pack(side=LEFT)

path_frame.pack(pady=20)


mode_frame = Frame(root)

mode_label = Label(mode_frame, text="Mode de conversion : ")
mode_label.pack(side=LEFT)

mode_button = ToggleButton()
mode_button.pack(side=LEFT)

mode_frame.pack()


convert_button_font = Font(family="Helveticabold", size=12)

convert_button = Button(root, text="Convertir", command=lambda: run(path_entry.get(), mode_button.status), width=20, height=2, font=convert_button_font)
convert_button.pack(pady=30)

success_label = Label(root, font=("Helveticabold", 10), fg="green")
error_label = Label(root, text="Une erreur inattendue est survenue", font=("Helveticabold", 10), fg="red")



root.mainloop()

