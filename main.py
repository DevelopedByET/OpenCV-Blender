"""
Programme fait par Edgar Tourneur TG3

### Note Importante ###
Si votre éditeur de code / texte ne supporte pas les input() (ex: Sublime Text) il faut 
lancer le script via le CMD / Powershell / Shell / Batch / Interface de ligne de commandes.
Si vous tenez à utiliser tout de même votre éditeur il vous suffit de mettre vous-même la
valeur de 'alpha' à la ligne n°40 par un nombre compris dans ]0; 1[.

Enfin si quand vous lancez le script, aucune fenêtre apparait apres avoir rentré l'opacité,
essayez de relancer le script, si vous avez toujour rien supprimez la ligne n°37 qui contient:
'root.withdraw()' et tout devrait fonctionner.
"""

import os
import tkinter as tk
from tkinter import filedialog as fdg

from assets.blender import Blender


def filename_from_path(path: str):
    """
    Return le substring contenant le nom du fichier

    :param path: Chemin contenant le nom du fichier
    :return: str du nom du fichier sans extension
    """
    p = os.path.abspath(path)
    last_slash_idx = [x for x in range(len(p)) if p[x] == "\\"][-1]
    last_dot_idx = [x for x in range(len(p)) if p[x] == "."][-1]
    return p[last_slash_idx + 1:last_dot_idx]


# Création d'un fenêtre Tkinter que l'on cache (utile pour demander les images)
root = tk.Tk()
root.withdraw()

# Définition de l'opacité
alpha = None
while not isinstance(alpha, float):
    try:
        tmp = float(input("\nChoisir l'opacité (compris dans ]0; 1[): "))
        if 1 >= tmp >= 0:
            alpha = tmp
        else:
            raise ValueError
    except:
        print("Valeur entrée incorrect. Veuillez en choisir une autre")

# Demande des images
print("\nChoisir la première image:")
image1 = fdg.askopenfile(filetypes=[("JPG Files", "jpg"), ("PNG Files", "png"), ("JPEG Files", "jepg")])
if image1:
    image1 = image1.name
    print(f"    Image choisi: {os.path.abspath(image1)}\n\nChoisir la second image:")
    image2 = fdg.askopenfile(filetypes=[("JPG Files", "jpg"), ("PNG Files", "png"), ("JPEG Files", "jepg")])
    if image2:
        root.destroy()
        image2 = image2.name
        print(f"    Image choisi: {os.path.abspath(image2)}")

        # On créé le dossier 'out_img' qui stock les résultats si il n'existe pas
        if not os.path.exists("out_img"):
            os.mkdir("out_img")

        # On instancie la class Blender (de 'blender.py' dans le dossier 'assets') qui gere les opérations sur les images
        blender = Blender(image1, image2, alpha)

        # Combine les images
        out_img_combin = blender.blend(save_name=f"blend_{filename_from_path(image1)}_{filename_from_path(image2)}.png")
        print(f"\nImage combinée créée et sauvegardée: \n    {os.path.abspath(out_img_combin)}")

        # Récupère l'image n°1
        out_img1 = blender.unblend(get_img1=True, save_name=f"original_{filename_from_path(image1)}")
        print(f"\nImage n°1 recupérée et sauvegardée: \n    {os.path.abspath(out_img1)}")

        # Récupère l'image n°2
        out_img2 = blender.unblend(get_img1=False, save_name=f"original_{filename_from_path(image2)}") 
        print(f"\nImage n°2 recupérée et sauvegardée: \n    {os.path.abspath(out_img2)}")
