import numpy as np
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as ptch

def quantifier_image(image_array, niveaux):

    step = 255 / (niveaux - 1)
    image_quantified = (np.round(image_array / step) * step).astype(np.uint8)

    print("Pas de quantification :")
    print(step)
    valeurs_possibles = [(np.round(np.round(i*step) / step) * step).astype(np.uint8) for i in range(niveaux)]
    print("Valeurs possibles :")
    print(valeurs_possibles)

    return image_quantified

chemin = Path(__file__).resolve().parent
chemin_image = chemin /  "image_004.png"  # Remplace par le nom de ton image
niveaux_de_gris = [8, 4, 2] # Valeur des différents niveaux de gris à afficher
erreur = int(True)  # 'True' pour afficher l'erreur
adaptive = False    # 'True' pour de la quantification adaptative

# Groupe de pixels à inspecter
block_size = 5
y_min, y_max, x_min, x_max = 750, 750+block_size, 450, 450+block_size
épaisseur = 1
couleur = 'blue'

# Affichage des images originales
plt.figure(figsize=(10, 5))
mng = plt.get_current_fig_manager()
mng.window.showMaximized()

# Chargement de l'image
image = Image.open(chemin_image).convert('L')  # Convertir en niveaux de gris

# Conversion en tableau numpy
image_array = np.array(image, dtype=np.float32) #Redimensionnée en fonction de la taille de l'image

# Extraction des valeurs des pixels du groupe
groupe_pixels = image_array[y_min:y_max, x_min:x_max]
print("Valeurs des pixels du groupe sélectionné :")
print(groupe_pixels)

ax0 = plt.subplot(erreur+1, len(niveaux_de_gris)+1, 1)
# Ajouter un rectangle rouge autour du groupe de pixels
rect = ptch.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=épaisseur, edgecolor=couleur, facecolor='none')
ax0.add_patch(rect)
plt.title("Image Originale (256 niveaux)")
plt.imshow(image_array, cmap="gray")
plt.axis("off")

if erreur != 0 :
    ax0 = plt.subplot(erreur+1, len(niveaux_de_gris)+1, erreur*(len(niveaux_de_gris)+1)+1)
    plt.title("Erreur (256 niveaux)")
    plt.imshow(image_array-image_array, cmap="gray")
    plt.axis("off")


image_quantifiee = []
# Quantification
for j in range(len(niveaux_de_gris)) :
    image_quantifiee = quantifier_image(image_array, niveaux_de_gris[j])
    
    # Extraction des valeurs des pixels du groupe
    groupe_pixels = image_quantifiee[y_min:y_max, x_min:x_max]
    print("Valeurs des pixels du groupe sélectionné :")
    print(groupe_pixels)

    # Affichage des images quantifiées
    ax1 = plt.subplot(erreur+1, len(niveaux_de_gris)+1, j+2)
    # Ajouter un rectangle autour du groupe de pixels
    rect = ptch.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=épaisseur, edgecolor=couleur, facecolor='none')
    ax1.add_patch(rect)
    plt.title(f"Image Quantifiée ({niveaux_de_gris[j]} niveaux)")
    plt.imshow(image_quantifiee, cmap="gray")
    plt.axis("off")

    # Affichage de l'erreur
    if erreur != 0:
        ax1 = plt.subplot(erreur+1, len(niveaux_de_gris)+1, j+2+erreur*(len(niveaux_de_gris)+1))
        plt.title(f"Erreur ({niveaux_de_gris[j]} niveaux)")
        plt.imshow(image_array-image_quantifiee, cmap="gray")
        plt.axis("off")
        print("erreu_max :", np.max(image_array-image_quantifiee))

plt.tight_layout()
plt.show()

def adaptive_quantization(image, num_levels, block_size):
    # Initialisation de l'image quantifiée
    quantized_image = np.zeros_like(image, dtype=np.uint8)

    var = []
    # Diviser l'image en blocs
    height, width = image.shape
    # Recherche de la variance maximale
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Extraire le bloc courant
            block = image[i:i+block_size, j:j+block_size]

            # Calculer la variance locale
            variance = np.var(block)
            var.append(variance)
    var_max = np.max(var)
    level = []
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Extraire le bloc courant
            block = image[i:i+block_size, j:j+block_size]

            # Calculer la variance locale
            variance = np.var(block)

            # Ajuster le nombre de niveaux en fonction de la variance
            local_levels = max(2, int(num_levels * (variance / var_max)))
            level.append(local_levels)

            # Calculer les seuils pour ce bloc
            min_val, max_val = np.min(block), np.max(block)
            thresholds = np.linspace(min_val, max_val, local_levels, endpoint=False)

            quantized_block = np.digitize(block, thresholds) - 1
            quantized_block = (quantized_block * (255 // (local_levels - 1))).astype(np.uint8)

            # Placer le bloc quantifié dans l'image finale
            quantized_image[i:i+block_size, j:j+block_size] = quantized_block

    level = np.mean(level)
    print("Niveau moyen :", level)

    return quantized_image, level


if adaptive :
    # Appliquer la quantification adaptative
    quantized_image, level = adaptive_quantization(image_array, num_levels=16, block_size=block_size*5)

    # Afficher les résultats
    plt.figure(figsize=(10, 5))
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.subplot(1, 3, 1)
    plt.title("Originale")
    plt.imshow(image_array, cmap='gray')
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title(f"Image Quantifiée Uniforme (2 niveaux)")
    plt.imshow(image_quantifiee, cmap='gray')
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title(f"Image Quantifiée Non-uniforme ({np.round(np.mean(level), 3)} niveaux)")
    plt.imshow(quantized_image, cmap='gray')
    plt.axis("off")

    plt.show()