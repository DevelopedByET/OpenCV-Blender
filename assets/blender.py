import cv2
import os


class Blender:
    def __init__(self, img1_path: str, img2_path: str, opacity: float, blend_img_path: str = None):
        """
        :param img1_path: Chemin de la première image
        :param img2_path: Chemin de la second image
        :param alpha_overlay: Opacité de l'overlay (compris dans ]0; 1[)
        :param blend_img_path: (Optionnel) Chemin de l'image combinée
        """
        self.img1_path = img1_path
        self.overlay_path = img2_path
        self.alpha_overlay = opacity
        self.out_name = blend_img_path
        self.error_alpha = "Valeur de 'alpha_overlay' incorrect: elle doit être comprise dans ]0; 1[ "


    def blend(self, save_name):
        """
        Combine deux image en une seule

        :param save_name: Nom de l'image lors de la sauvegarde
        :return: Chemin du l'image obtenue et savegarde le résultat dans le dossier 'out_img'
        """
        if 1 > self.alpha_overlay > 0:
            img1 = cv2.imread(self.img1_path)
            img2 = cv2.imread(self.overlay_path)
            out = cv2.addWeighted(img1, self.alpha_overlay, img2, (1 - self.alpha_overlay), 0)
            out_name = f"out_img/{save_name}"
            # Supprime la photo qui a le même nom que celle créée
            if os.path.exists(out_name):
                os.remove(out_name)
            cv2.imwrite(out_name, out)
            self.out_name = out_name
            return out_name
        else:
            print(self.error_alpha)


    def unblend(self, get_img1: bool, save_name: str):
        """
        Recréé l'image de base avec l'image combinée

        :param get_img1: 'True' pour recupérer l'image n°1 et 'False' pour récupérer l'image n°2
        :param save_name: Nom de l'image lors de la sauvegarde
        :return: Chemin du l'image obtenue et savegarde le résultat dans le dossier 'out_img'
        """
        self.alpha_overlay = self.alpha_overlay if get_img1 else 1 - self.alpha_overlay
        if 1 > self.alpha_overlay > 0:
            if self.out_name == None:
                print("Il faut faire la fonction 'blend' avant")
                return
            blend_img = cv2.imread(self.out_name)
            overlay_img = cv2.imread(self.overlay_path) if get_img1 else cv2.imread(self.img1_path)
            """
            Explication de ma démarche:
            On combine 2 image de façon linéaire

            Donc:
                combin = a * image_original + (1 - a) * overlay (dans notre cas a = 0.7 et correspond à l'opacité)
            
            D'où:
                image_original = (combin - (1 - a) * overlay) / a
                            = 1 / a * combin + (1 - 1 / a) * overlay
            
            Traduction en code:
                cv2.addWeighted(combin, (1 / a), overlay, (1 - 1 / a), 0)
            """
            original_img = cv2.addWeighted(blend_img, (1 / self.alpha_overlay), overlay_img, (1 - 1 / self.alpha_overlay), 0)
            out_name = f"out_img/{save_name}.png"
            # Supprime la photo qui a le même nom que celle créée
            if os.path.exists(out_name):
                os.remove(out_name)
            cv2.imwrite(out_name, original_img)
            return out_name
        else:
            print(self.error_alpha)