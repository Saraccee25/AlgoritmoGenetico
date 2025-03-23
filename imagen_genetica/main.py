import numpy as np
from io import BytesIO
import requests
import matplotlib.pyplot as plt
from PIL import Image
import random as rd

# 📌 Parámetros iniciales
porcentajeMuta = 70  # Porcentaje de mutación (cuanto mayor, más cambios permitidos)
iteraciones = 1
url = "https://lh3.googleusercontent.com/StND2cg3sSbR6l-AHr3VdxKziIhEP4kYHQiTppD-aKc6gwn7PVdht1YqzjWSmwf5JLWf=w200-rwa"

# 📌 Cargar la imagen original desde la URL
rta = requests.get(url)
imagen = Image.open(BytesIO(rta.content)).convert("RGB")  # Asegurar que la imagen sea RGB
imgArrayOriginal = np.array(imagen, dtype=np.uint8)

# 📌 Generar una imagen aleatoria
imgAleatoria = np.random.randint(0, 256, imgArrayOriginal.shape, dtype=np.uint8)

# 📌 Mutación basada en error relativo
for p in range(iteraciones):
    for i in range(imgAleatoria.shape[0]):  # Filas
        for j in range(imgAleatoria.shape[1]):  # Columnas
            for c in range(3):  # Canales (R, G, B)
                original_value = imgArrayOriginal[i, j, c]
                aleatorio_value = imgAleatoria[i, j, c]

                if original_value != 0:
                    error_relativo = abs(aleatorio_value - original_value) / original_value
                    if error_relativo > (1 - porcentajeMuta / 100):
                        ajuste = abs((aleatorio_value - original_value) / 2)
                        imgAleatoria[i, j, c] = np.clip(aleatorio_value - ajuste, 0, 255).astype(np.uint8)
                else:
                    imgAleatoria[i, j, c] = np.clip(aleatorio_value / 2, 0, 255).astype(np.uint8)

# 📌 Mostrar la imagen generada
plt.imshow(imgAleatoria)
plt.axis("off")  # Quitar ejes para mejor visualización
plt.show()
