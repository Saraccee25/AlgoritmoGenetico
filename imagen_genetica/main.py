import numpy as np
from io import BytesIO
import requests
import matplotlib.pyplot as plt
from PIL import Image

# 📌 Parámetros iniciales
porcentajeMuta = 70
iteraciones = 10
alpha = 0.5

# ✅ URL válida (imagen JPEG desde Wikipedia)
url = "https://lavaquita.co/cdn/shop/products/supermercados_la_vaquita_supervaquita_gaseosa_coca_cola_1.5l_nr_bebidas_liquidas.jpg?v=1620489417"

# 📌 Cargar la imagen desde la URL
try:
    rta = requests.get(url)
    rta.raise_for_status()  # Lanza excepción si falla
    imagen = Image.open(BytesIO(rta.content)).convert("RGB")
except Exception as e:
    print("❌ Error al cargar la imagen:", e)
    exit()

# 📌 Convertir imagen a array
imgArrayOriginal = np.array(imagen, dtype=np.uint8)

# 📌 Generar imagen con ruido
ruido = np.random.randint(-50, 50, imgArrayOriginal.shape, dtype=np.int16)
imgAleatoria = np.clip(imgArrayOriginal.astype(np.int16) + ruido, 0, 255).astype(np.uint8)

# 📌 Mutación
for p in range(iteraciones):
    for i in range(imgAleatoria.shape[0]):
        for j in range(imgAleatoria.shape[1]):
            for c in range(3):
                original_value = float(imgArrayOriginal[i, j, c])
                aleatorio_value = float(imgAleatoria[i, j, c])
                if original_value > 0:
                    error_relativo = abs(aleatorio_value - original_value) / max(original_value, 1)
                    if error_relativo > (1 - porcentajeMuta / 100):
                        imgAleatoria[i, j, c] = np.clip(
                            (1 - alpha) * aleatorio_value + alpha * original_value, 0, 255
                        ).astype(np.uint8)
                else:
                    imgAleatoria[i, j, c] = np.clip(
                        (1 - alpha) * aleatorio_value, 0, 255
                    ).astype(np.uint8)

# 📌 Mostrar imagen generada
plt.imshow(imgAleatoria)
plt.axis("off")
plt.show()
