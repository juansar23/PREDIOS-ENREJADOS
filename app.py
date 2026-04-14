import streamlit as st
import pandas as pd
import zipfile
import io
import os

st.set_page_config(page_title="Extractor ITA - Pro", page_icon="🏗️")

st.title("📸 Extractor de Fotos Pesadas (ZIP)")
st.markdown("Optimizado para archivos de más de 500MB.")

# --- CARGA DINÁMICA ---
with st.sidebar:
    st.header("Archivos")
    # Aumentamos el límite de carga (aunque Streamlit Cloud suele permitir hasta 1GB por archivo)
    archivo_zip = st.file_uploader("1. Sube el ZIP (Máx 1GB)", type=["zip"])
    archivo_excel = st.file_uploader("2. Sube el Excel de IDs", type=["xlsx", "xls"])

if archivo_zip and archivo_excel:
    try:
        # Leer Excel
        df = pd.read_excel(archivo_excel)
        columna_id = st.selectbox("Selecciona la columna de IDs:", df.columns)
        
        # Limpiar IDs y convertirlos en un set (es mucho más rápido para buscar)
        ids_raw = df[columna_id].astype(str).unique().tolist()
        fotos_a_buscar = {f if f.lower().endswith('.jpg') else f"{f}.jpg" for f in ids_raw}
        
        st.info(f"🔍 Buscando {len(fotos_a_buscar)} fotos dentro del ZIP de 550MB...")

        if st.button("🚀 Iniciar Extracción"):
            buffer_salida = io.BytesIO()
            barrita = st.progress(0)
            status = st.empty()
            
            # Abrimos el ZIP original
            with zipfile.ZipFile(archivo_zip, 'r') as z_in:
                nombres_en_zip = z_in.namelist()
                # Mapa de nombres para no importar las carpetas internas
                mapa_archivos = {os.path.basename(f): f for f in nombres_en_zip if not f.endswith('/')}
                
                # Creamos el nuevo ZIP
                with zipfile.ZipFile(buffer_salida, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
                    encontrados = 0
                    total = len(fotos_a_buscar)
                    
                    for i, foto in enumerate(fotos_a_buscar):
                        if foto in mapa_archivos:
                            ruta_interna = mapa_archivos[foto]
                            # Leemos solo el pedazo de archivo necesario
                            with z_in.open(ruta_interna) as f_in:
                                z_out.writestr(foto, f_in.read())
                            encontrados += 1
                        
                        # Actualizar progreso cada 10 fotos para no saturar la web
                        if i % 10 == 0 or i == total - 1:
                            barrita.progress((i + 1) / total)
                            status.text(f"Procesado: {i+1}/{total}")

            status.success(f"✅ ¡Listo! Encontradas {encontrados} fotos.")
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar ZIP Filtrado",
                data=buffer_salida.getvalue(),
                file_name="fotos_ita_filtradas.zip",
                mime="application/zip"
            )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("👈 Por favor, carga los archivos en el menú lateral.")
