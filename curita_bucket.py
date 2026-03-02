# Este programa es para convertir de pdf a md o txt
import os
import re
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter

def limpiar_texto_legal(texto):
    # 1. Cortar el documento donde empieza la evidencia criptográfica o firmas
    marcadores_final = ["EVIDENCIA CRIPTOGRÁFICA", "Evidencia Criptográfica", "Firma Electrónica"]
    for marcador in marcadores_final:
        if marcador in texto:
            texto = texto.split(marcador)[0] # Nos quedamos solo con lo de arriba
            
    # 2. Borrar sellos de tiempo de los márgenes (Ej. 03/03/24 21:45:18)
    texto = re.sub(r'\d{2}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}', '', texto)
    
    # 3. Borrar números de serie largos (Ej. 70.4.66.20.63.64.56...)
    texto = re.sub(r'[0-9\.]{30,}', '', texto)
    
    # 4. Borrar ruido común del Poder Judicial
    ruido = ["PJF - Versión Pública", "FORMA B-1", "PODER JUDICIAL DE LA FEDERACIÓN"]
    for palabra in ruido:
        texto = texto.replace(palabra, "")
        
    return texto.strip()

def curar_biblioteca_legal(directorio_entrada, directorio_salida):
    # Verificamos que tu nueva carpeta exista
    if not os.path.exists(directorio_entrada):
        print(f"❌ Error: No se encontró la carpeta {directorio_entrada}")
        return
        
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    # Configuración de cortes para Leyes Mexicanas
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        # Añadimos "Artículo" y "ARTÍCULO" para que no corte ideas a la mitad
        separators=["\nArtículo", "\nARTÍCULO", "\nLibro", "\nTítulo", "\n\n"],
        is_separator_regex=False
    )

    for archivo in os.listdir(directorio_entrada):
        ruta_archivo = os.path.join(directorio_entrada, archivo)
        
        # --- LA SOLUCIÓN ESTÁ AQUÍ ---
        # Convertimos el nombre a minúsculas para que no importe si dice .PDF o .pdf
        archivo_minusculas = archivo.lower()
        
        # Evaluamos si es PDF
        if archivo_minusculas.endswith(".pdf"):
            print(f"⏳ Procesando PDF: {archivo}...")
            loader = PyPDFLoader(ruta_archivo)
            
        # Evaluamos si es Word
        elif archivo_minusculas.endswith(".docx"):
            print(f"⏳ Procesando WORD: {archivo}...")
            loader = Docx2txtLoader(ruta_archivo)
            
        # Si no es ni PDF ni Word, lo saltamos
        else:
            continue
            
        # A partir de aquí, el proceso es idéntico para ambos formatos
        docs = loader.load()
        
        # Aplicamos la limpieza
        for doc in docs:
            doc.page_content = limpiar_texto_legal(doc.page_content)
            
        chunks = text_splitter.split_documents(docs)

        # Preparamos el archivo Markdown de salida
        nombre_base = os.path.splitext(archivo)[0]
        ruta_txt = os.path.join(directorio_salida, f"{nombre_base}_curado.md")
        
        with open(ruta_txt, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks):
                header = f"--- FUENTE: {nombre_base} | FRAGMENTO: {i+1} ---\n"
                f.write(header + chunk.page_content + "\n\n")

    print(f"✅ ¡Proceso terminado exitosamente! Tus archivos curados están en: {directorio_salida}")

# RUTAS EXACTAS DE TU ESCRITORIO
ruta_entrada = r"C:\Users\pcast\OneDrive\Desktop\docs_legales_bucket"
ruta_salida = r"C:\Users\pcast\OneDrive\Desktop\bucket_limpio"

# Ejecutamos la función
curar_biblioteca_legal(ruta_entrada, ruta_salida)