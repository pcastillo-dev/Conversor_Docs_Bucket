#Este programa es para convertir de docx a jsonl (LEYES)
import os
import re
import json
from docx import Document

def extraer_texto_docx(ruta_docx):
    print(f" Leyendo Word: {os.path.basename(ruta_docx)}")
    texto_completo = ""
    try:
        doc = Document(ruta_docx)
        for para in doc.paragraphs:
            if para.text.strip():
                texto_completo += para.text + "\n"
    except Exception as e:
        print(f"Error leyendo DOCX {ruta_docx}: {e}")
    return texto_completo

def limpiar_texto_legal(texto):
    print(" Limpiando texto...")
    # Limpiar basuras comunes (puedes ajustar esto según lo que traiga el Word)
    texto = re.sub(r'\n+', '\n', texto)
    return texto.strip()

def extraer_articulos_universal(texto):
    print(" Buscando artículos (Modo Universal)...")
    articulos = []
    
    # El mismo patrón invencible que usamos ayer para Bis, Ter, etc.
    patron = r'(Artículo\s+\d+[o\.\-]*\s*(?:[A-Z]|Bis|Ter|Quáter|Quintus|Sextus)?)(.*?)(?=\nArtículo\s+\d+[o\.\-]*|$)'
    
    matches = list(re.finditer(patron, texto, re.IGNORECASE | re.DOTALL))
    print(f"     Encontrados {len(matches)} artículos probables")
    
    for match in matches:
        num_articulo = match.group(1).strip()
        contenido = match.group(2).strip()
        contenido = re.sub(r'\s+', ' ', contenido)
        
        if len(contenido) > 10:
            articulos.append({
                'numero': num_articulo,
                'texto': contenido
            })
    return articulos

def procesar_word(ruta_docx, ruta_salida):
    nombre_archivo = os.path.basename(ruta_docx)
    nombre_ley = os.path.splitext(nombre_archivo)[0]
    
    print(f"\n{'='*60}")
    print(f"PROCESANDO LEY EN WORD: {nombre_ley}")
    print(f"{'='*60}")
    
    texto = extraer_texto_docx(ruta_docx)
    if not texto: return
    
    texto_limpio = limpiar_texto_legal(texto)
    articulos = extraer_articulos_universal(texto_limpio)
    
    if not articulos:
        print(" No se encontraron artículos. Verifica que el documento tenga el formato 'Artículo X'.")
        return
        
    print(f" Guardando {len(articulos)} artículos en JSONL...")
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        for i, art in enumerate(articulos, 1):
            doc = {
                "id": f"{nombre_ley.replace(' ', '_')}_{i}",
                "ley": nombre_ley,
                "articulo": art['numero'],
                "contenido": f"{art['numero']} {art['texto']}"
            }
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
            
    print(f" Archivo guardado: {os.path.basename(ruta_salida)}")

def main():
    # Pon aquí la carpeta donde guardaste los códigos de BCS ya convertidos a .docx
    CARPETA_WORDS = r"C:\Users\pcast\OneDrive\Desktop\proyecto_leyes\pdfs_originales\Codigos_Civiles_Penales_ProcedimientosCiviles_ESTATALES\Baja_California_Sur"
    # Pon aquí donde quieres que salgan los .jsonl
    CARPETA_SALIDA = r"C:\Users\pcast\OneDrive\Desktop\proyecto_leyes\jsonl_salida\Codigos_Civiles_Penales_ProcedimientosCiviles_ESTATALES\Baja_California_Sur"
    
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
        
    archivos_docx = [f for f in os.listdir(CARPETA_WORDS) if f.lower().endswith('.docx')]
    
    for docx in archivos_docx:
        ruta_docx = os.path.join(CARPETA_WORDS, docx)
        ruta_salida = os.path.join(CARPETA_SALIDA, docx.replace('.docx', '.jsonl').replace('.DOCX', '.jsonl'))
        procesar_word(ruta_docx, ruta_salida)
        
    print("\n PROCESO COMPLETADO PARA TODOS LOS CÓDIGOS EN WORD")

if __name__ == "__main__":
    main()