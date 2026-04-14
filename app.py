import streamlit as st
import pandas as pd
import zipfile
import io
import os

st.set_page_config(page_title="Extractor de Fotos", layout="centered")

st.title("📸 Extractor Dinámico de Fotos")
st.markdown("Sube tus archivos para realizar el filtrado sin rutas fijas.")

# --- SECCIÓN DE CARGA DE ARCHIVOS ---
# Esto reemplaza las rutas fijas y permite subir archivos desde tu PC
archivo_zip = st.file_uploader("1. Selecciona el archivo ZIP con las fotos", type=["zip"])
archivo_excel = st.file_uploader("2. Selecciona el archivo Excel con los IDs", type=["xlsx", "xls"])

if archivo_zip and archivo_excel:
    try:
        # Leemos el Excel que acabas de subir
        df = pd.read_excel(archivo_excel)
        
        # Permitimos elegir la columna dinámicamente
        columna_id = st.selectbox("Selecciona la columna con los nombres de las fotos:", df.columns)
        
        # Procesamos la lista de nombres
        lista_nombres = df[columna_id].astype(str).unique().tolist()
        fotos_a_buscar = {f if f.lower().endswith('.jpg') else f"{f}.jpg" for f in lista_nombres}

        if st.button("🚀 Iniciar Extracción"):
            buffer_zip_nuevo = io.BytesIO()
            barrita = st.progress(0)
            
            with zipfile.ZipFile(archivo_zip, 'r') as z_in:
                nombres_en_zip = z_in.namelist()
                # Mapa para encontrar archivos aunque estén en subcarpetas dentro del ZIP
                mapa_archivos = {os.path.basename(f): f for f in nombres_en_zip}
                
                with zipfile.ZipFile(buffer_zip_nuevo, 'w') as z_out:
                    encontrados = 0
                    total = len(fotos_buscadas)
                    
                    for i, foto in enumerate(fotos_buscadas):
                        if foto in mapa_archivos:
                            ruta_interna = mapa_archivos[foto]
                            z_out.writestr(foto, z_in.read(ruta_interna))
                            encontrados += 1
                        
                        # Actualizar progreso
                        barrita.progress((i + 1) / total)
            
            st.success(f"✅ Proceso terminado. Se encontraron {encontrados} de {len(fotos_buscadas)} fotos.")
            
            # Botón para descargar el resultado
            st.download_button(
                label="📥 Descargar Fotos Filtradas",
                data=buffer_zip_nuevo.getvalue(),
                file_name="fotos_extraidas.zip",
                mime="application/zip"
            )

    except Exception as e:
        st.error(f"Error al procesar los archivos: {e}")

else:
    st.info("Esperando que subas el ZIP y el Excel...")
