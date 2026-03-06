#Este programa es para convertir de pdf o docx a jsonl. Ideal para documentos legales largos y complejos.
import os
import re
import json
import pdfplumber
from docx import Document

def extraer_texto_pdf(ruta_pdf):
    texto_completo = ""
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_completo += texto + "\n"
    except Exception as e:
        print(f"Error leyendo PDF {ruta_pdf}: {e}")
    return texto_completo

def extraer_texto_docx(ruta_docx):
    texto_completo = ""
    try:
        doc = Document(ruta_docx)
        for para in doc.paragraphs:
            if para.text.strip():
                texto_completo += para.text + "\n"
    except Exception as e:
        print(f"Error leyendo DOCX {ruta_docx}: {e}")
    return texto_completo

def limpiar_texto(texto):
    # Quitamos dobles espacios y saltos de línea excesivos
    texto = re.sub(r'\n+', '\n', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def fragmentar_en_chunks(texto, palabras_por_chunk=200):
    """
    Divide el texto continuo en bloques (chunks) de tamaño aproximado.
    200-300 palabras es el tamaño ideal para que Vertex AI y Gemini lo entiendan.
    """
    palabras = texto.split(' ')
    chunks = []
    
    # Vamos cortando la lista de palabras de 200 en 200
    for i in range(0, len(palabras), palabras_por_chunk):
        bloque = " ".join(palabras[i:i + palabras_por_chunk])
        if len(bloque.strip()) > 20: # Ignorar bloques vacíos
            chunks.append(bloque)
            
    return chunks

def procesar_archivo_no_estructurado(ruta_archivo, ruta_salida):
    nombre_archivo = os.path.basename(ruta_archivo)
    nombre_base, extension = os.path.splitext(nombre_archivo)
    extension = extension.lower()
    
    print(f"\nProcesando documento: {nombre_archivo}")
    
    # 1. Extraer texto dependiendo si es PDF o Word
    texto = ""
    if extension == '.pdf':
        texto = extraer_texto_pdf(ruta_archivo)
    elif extension in ['.doc', '.docx']:
        texto = extraer_texto_docx(ruta_archivo)
    else:
        print("Formato no soportado.")
        return
        
    if not texto:
        print("⚠️ Documento vacío o ilegible.")
        return
        
    # 2. Limpiar y Fragmentar
    texto_limpio = limpiar_texto(texto)
    chunks = fragmentar_en_chunks(texto_limpio, palabras_por_chunk=250)
    
    # 3. Guardar en JSONL
    print(f"  💾 Guardando en {len(chunks)} fragmentos...")
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks, 1):
            doc = {
                "id": f"{nombre_base.replace(' ', '_')}_chunk_{i}",
                "ley": nombre_base, # Usamos el nombre del archivo como 'título/ley'
                "articulo": f"Fragmento {i}", # Falso artículo para mantener compatibilidad
                "contenido": chunk
            }
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')

def main():
    # Cambia estas rutas a tus carpetas reales
    CARPETA_ENTRADA = r"C:\Users\pcast\OneDrive\Desktop\proyecto_leyes\pdfs_originales\Mercantil"
    CARPETA_SALIDA = r"C:\Users\pcast\OneDrive\Desktop\proyecto_leyes\jsonl_salida\Mercantil"
    
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
        
    for archivo in os.listdir(CARPETA_ENTRADA):
        if archivo.lower().endswith(('.pdf', '.docx', '.doc')):
            ruta_archivo = os.path.join(CARPETA_ENTRADA, archivo)
            ruta_salida = os.path.join(CARPETA_SALIDA, archivo.rsplit('.', 1)[0] + '.jsonl')
            procesar_archivo_no_estructurado(ruta_archivo, ruta_salida)
            
    print("\n✅ TODOS LOS FORMATOS CONVERTIDOS A JSONL")

if __name__ == "__main__":
    main()