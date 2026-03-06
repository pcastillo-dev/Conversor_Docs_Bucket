# Este programa es para convertir de pdf a jsonl (LEYES)
import os
import re
import json
import pdfplumber

def extraer_texto_de_pdf(ruta_pdf):
    print(f"  📖 Leyendo PDF: {os.path.basename(ruta_pdf)}")
    texto_completo = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        total_paginas = len(pdf.pages)
        for i, pagina in enumerate(pdf.pages, 1):
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"
    return texto_completo

def limpiar_texto_legal(texto):
    print("  🧹 Limpiando texto...")
    marcadores_final = ["EVIDENCIA CRIPTOGRÁFICA", "Evidencia Criptográfica", "Firma Electrónica"]
    for marcador in marcadores_final:
        if marcador in texto:
            texto = texto.split(marcador)[0]
    texto = re.sub(r'\d{2}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}', '', texto)
    texto = re.sub(r'[0-9\.]{30,}', '', texto)
    ruido = ["PJF - Versión Pública", "FORMA B-1", "PODER JUDICIAL DE LA FEDERACIÓN"]
    for palabra in ruido:
        texto = texto.replace(palabra, "")
    return texto.strip()

def extraer_articulos_universal(texto):
    print("Buscando artículos (Modo Universal Mejorado)...")
    articulos = []
    
    # NUEVO PATRÓN: Ahora captura números, letras (A, B) y sufijos (Bis, Ter, Quáter, Quintus, Sextus)
    # y se detiene correctamente antes del SIGUIENTE artículo.
    patron = r'(Artículo\s+\d+[o\.\-]*\s*(?:[A-Z]|Bis|Ter|Quáter|Quintus|Sextus)?)(.*?)(?=\nArtículo\s+\d+[o\.\-]*|$)'
    
    matches = list(re.finditer(patron, texto, re.IGNORECASE | re.DOTALL))
    print(f"     Encontrados {len(matches)} artículos probables")
    
    for match in matches:
        num_articulo = match.group(1).strip()
        contenido = match.group(2).strip()
        
        # Limpiar saltos de línea y espacios dobles
        contenido = re.sub(r'\s+', ' ', contenido)
        
        if len(contenido) > 10:
            articulos.append({
                'numero': num_articulo,
                'texto': contenido
            })
    return articulos

def procesar_pdf(ruta_pdf, ruta_salida):
    nombre_archivo = os.path.basename(ruta_pdf)
    nombre_ley = os.path.splitext(nombre_archivo)[0]
    
    print(f"\n{'='*60}")
    print(f"PROCESANDO: {nombre_ley}")
    print(f"{'='*60}")
    
    texto = extraer_texto_de_pdf(ruta_pdf)
    if not texto: return
    
    texto_limpio = limpiar_texto_legal(texto)
    articulos = extraer_articulos_universal(texto_limpio)
    
    if not articulos:
        print("  ⚠️  No se encontraron artículos con el patrón estándar.")
        return
        
    print(f"Guardando {len(articulos)} artículos en JSONL plano...")
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        for i, art in enumerate(articulos, 1):
            
            # EL JSONL PLANO Y PERFECTO PARA VERTEX
            doc = {
                "id": f"{nombre_ley.replace(' ', '_')}_{i}",
                "ley": nombre_ley,
                "articulo": art['numero'],
                "contenido": f"{art['numero']} {art['texto']}"
            }
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
            
    print(f"Archivo guardado: {os.path.basename(ruta_salida)}")

def main():
    CARPETA_PDFS = r"C:\Users\pcast\OneDrive\Desktop\proyecto_leyes\pdfs_originales"
    CARPETA_SALIDA = r"C:\Users\pcast\OneDrive\Desktop\proyecto_leyes\jsonl_salida"
    
    print(f"Iniciando escaneo masivo en: {CARPETA_PDFS}\n")

    for raiz, directorios, archivos in os.walk(CARPETA_PDFS):
        # Filtramos para ver si en esta carpeta en específico hay PDFs
        pdfs_en_carpeta = [f for f in archivos if f.lower().endswith('.pdf')]
        
        if pdfs_en_carpeta:
            # ¡ESTO ES LO NUEVO! Te avisa en qué carpeta entró
            nombre_carpeta_actual = os.path.basename(raiz)
            if not nombre_carpeta_actual or nombre_carpeta_actual == "pdfs_originales":
                nombre_carpeta_actual = "Carpeta Principal (Federales sueltos)"
                
            print(f"\n{'*'*70}")
            print(f"📂 ENTRANDO A CARPETA: {nombre_carpeta_actual.upper()}")
            print(f"   Se encontraron {len(pdfs_en_carpeta)} PDFs aquí. Procesando...")
            print(f"{'*'*70}")
            
            for archivo in pdfs_en_carpeta:
                ruta_pdf = os.path.join(raiz, archivo)
                ruta_relativa = os.path.relpath(raiz, CARPETA_PDFS)
                carpeta_destino = os.path.join(CARPETA_SALIDA, ruta_relativa)
                
                if not os.path.exists(carpeta_destino):
                    os.makedirs(carpeta_destino)
                
                nombre_jsonl = archivo.replace('.pdf', '.jsonl').replace('.PDF', '.jsonl')
                ruta_salida = os.path.join(carpeta_destino, nombre_jsonl)
                
                procesar_pdf(ruta_pdf, ruta_salida)
                
    print("\n✅ PROCESO MASIVO COMPLETADO PARA TODAS LAS CARPETAS Y SUBCARPETAS")

if __name__ == "__main__":
    main()