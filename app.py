import os
import shutil
import pandas as pd

# Configuración
ruta_fotos = './todas_mis_fotos'     # Carpeta donde están los originales
ruta_destino = './fotos_seleccionadas' 
excel_lista = 'lista_a_extraer.xlsx' # Tu archivo Excel
columna_id = 'CUENTA'                   # Nombre de la columna con los números

# Crear carpeta de destino
os.makedirs(ruta_destino, exist_ok=True)

# Leer IDs y buscar
df = pd.read_excel(excel_lista)
fotos_a_buscar = df[columna_id].astype(str).tolist()

for nombre in fotos_a_buscar:
    # Asegurar extensión .jpg
    archivo = nombre if nombre.endswith('.jpg') else f"{nombre}.jpg"
    origen = os.path.join(ruta_fotos, archivo)
    
    if os.path.exists(origen):
        shutil.copy(origen, os.path.join(ruta_destino, archivo))
        print(f"Copiado: {archivo}")
    else:
        print(f"No encontrado: {archivo}")
