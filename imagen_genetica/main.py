import numpy as np
from io import BytesIO
import requests
import matplotlib.pyplot as plt
from PIL import Image
import random as rd

# 📌 Parámetros iniciales
porcentajeMuta = 70  # Cuanto mayor, más diferencia se permite
iteraciones = 10  # Aumentamos iteraciones para una mejor convergencia
alpha = 0.5  # Factor de ajuste para mutaciones más suaves (0 = sin cambios, 1 = cambio total)
url = "https://lh3.googleusercontent.com/StND2cg3sSbR6l-AHr3VdxKziIhEP4kYHQiTppD-aKc6gwn7PVdht1YqzjWSmwf5JLWf=w200-rwa"

# 📌 Cargar la imagen original desde la URL
rta = requests.get(url)
imagen = Image.open(BytesIO(rta.content)).convert("RGB")  # Asegurar que la imagen sea RGB
imgArrayOriginal = np.array(imagen, dtype=np.uint8)

# 📌 Generar una imagen inicial cercana a la original con ruido en lugar de completamente aleatoria
ruido = np.random.randint(-50, 50, imgArrayOriginal.shape, dtype=np.int16)  # Ruido pequeño
imgAleatoria = np.clip(imgArrayOriginal.astype(np.int16) + ruido, 0, 255).astype(np.uint8)

# 📌 Mutación basada en interpolación y error relativo
for p in range(iteraciones):
    for i in range(imgAleatoria.shape[0]):  # Filas
        for j in range(imgAleatoria.shape[1]):  # Columnas
            for c in range(3):  # Canales (R, G, B)
                original_value = imgArrayOriginal[i, j, c]
                aleatorio_value = imgAleatoria[i, j, c]

                if original_value != 0:
                    error_relativo = abs(aleatorio_value - original_value) / original_value
                    if error_relativo > (1 - porcentajeMuta / 100):
                        # 🔥 Corrección: interpolamos en lugar de solo dividir el ajuste
                        imgAleatoria[i, j, c] = np.clip((1 - alpha) * aleatorio_value + alpha * original_value, 0, 255).astype(np.uint8)
                else:
                    imgAleatoria[i, j, c] = np.clip((1 - alpha) * aleatorio_value, 0, 255).astype(np.uint8)

# 📌 Mostrar la imagen generada
plt.imshow(imgAleatoria)
plt.axis("off")  # Quitar ejes para mejor visualización
plt.show()
