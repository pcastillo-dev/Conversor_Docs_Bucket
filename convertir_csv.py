#Este programa es para convertir de csv a jsonl
import csv
import json

def csv_a_jsonl():
    ruta_csv = "Hoja_deRita.csv"
    ruta_jsonl = "Hoja_deRita.jsonl"

    print("🔄 Convirtiendo la Hoja de Rita a JSONL...")
    
    with open(ruta_csv, mode='r', encoding='utf-8-sig') as archivo_csv, \
        open(ruta_jsonl, mode='w', encoding='utf-8') as archivo_jsonl:
        
        lector = csv.DictReader(archivo_csv)
        
        for fila in lector:
            # Nos saltamos las filas vacías
            if not fila.get('Directriz (Regla)'):
                continue
                
            # Armamos un "contenido" rico en texto para que la IA lo entienda perfecto
            texto_contenido = (
                f"Directriz: {fila.get('Directriz (Regla)', '')}. "
                f"Fundamento Legal: {fila.get('Fundamento Legal', '')}. "
                f"Rubro: {fila.get('Rubro', '')}. "
                f"Comando de IA (System Prompt): {fila.get('System Prompt (Comando para la IA)', '')}. "
                f"Instrucciones para Desarrollador: {fila.get('Instrucciones para Desarrollador', '')}."
            )

            # Lo metemos en nuestro molde oficial
            documento = {
                "id": f"Directriz_Rita_{fila.get('ID', 'X')}",
                "ley": "Directrices Operativas de JUXA (Hoja de Rita)",
                "articulo": f"Regla {fila.get('ID', '')} - {fila.get('Directriz (Regla)', '')}",
                "contenido": texto_contenido
            }
            
            archivo_jsonl.write(json.dumps(documento, ensure_ascii=False) + '\n')
            
    print("✅ ¡Listo! Tu archivo Hoja_deRita.jsonl ha sido creado y está listo para la nube.")

if __name__ == "__main__":
    csv_a_jsonl()