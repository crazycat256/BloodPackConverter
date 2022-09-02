import traceback
from convert import convert
from functions import *
from tkinter import *
from typing_extensions import Literal
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
import webbrowser, shutil, tempfile

status_dic = {
    "blood": "Paladium vers Bloodshed",
    "pala": "Bloodshed vers Paladium",
}

class ToggleButton(Button):
    def __init__(self):
        Button.__init__(self, command=self.toggle, text=status_dic["blood"])
        self.status = "blood"

    def toggle(self):
        self.status = "blood" if self.status == "pala" else "pala"
        self.config(text=status_dic[self.status])


def open_url(url):
    webbrowser.open(url)

def select_file():
    path_entry.delete(0, END)
    path_entry.insert(0, askopenfilename(filetypes=(("Archive zip", "*.zip"),)))


def run(path: str, status: Literal["pala", "blood"]):
    
    error_label.pack_forget()
    success_label.pack_forget()

    if not os.path.isfile(path) and not path.endswith(".zip"):
        error_label.config(text="Le pack doit être sous d'archive zip")
        error_label.pack()
        return

    new_path = path.removesuffix(".zip") + "-converted"

    if os.path.isfile(new_path):
        error_label.config(text="Il y a déjà un pack à la destination de sortie")
        error_label.pack()
        return

    with tempfile.TemporaryDirectory() as tempdir:

        temp_path = os.path.join(tempdir, "temp-pack")

        try:
            shutil.unpack_archive(path, temp_path)
        except:
            error_label.config(text="Erreur lors de l'extraction de l'archive zip")
            error_label.pack()
            return
        

        try:
            convert(temp_path, status)

            shutil.make_archive(new_path, 'zip', temp_path)
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


frame = Frame(root)

path_entry = Entry(frame, width=50)
path_entry.pack(side=LEFT)

browse_button = Button(frame, text="Rechercher", command=select_file)
browse_button.pack(side=LEFT)

frame.pack(pady=20)


mode_button = ToggleButton()
mode_button.pack()

convert_button_font = Font(family="Helveticabold", size=12)

convert_button = Button(root, text="Convertir", command=lambda: run(path_entry.get(), mode_button.status), width=20, height=2, font=convert_button_font)
convert_button.pack(pady=30)

success_label = Label(root, font=("Helveticabold", 10), fg="green")
error_label = Label(root, text="Une erreur inattendue est survenue", font=("Helveticabold", 10), fg="red")



root.mainloop()

