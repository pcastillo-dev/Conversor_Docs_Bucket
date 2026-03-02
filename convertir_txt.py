import os

# La carpeta donde tienes tus archivos .md terminados
directorio = r"C:\Users\pcast\OneDrive\Desktop\bucket_limpio\Códigos_Civiles_Penales_ProcedimientosCiviles_ESTATALES\Zacatecas"

convertidos = 0

print("Iniciando cambio de formato de .md a .txt...")

for archivo in os.listdir(directorio):
    # Buscamos solo los archivos que terminen en .md
    if archivo.endswith(".md"):
        ruta_vieja = os.path.join(directorio, archivo)
        
        # Creamos el nuevo nombre reemplazando .md por .txt
        nuevo_nombre = archivo.replace(".md", ".txt")
        ruta_nueva = os.path.join(directorio, nuevo_nombre)
        
        # Renombramos el archivo
        os.rename(ruta_vieja, ruta_nueva)
        convertidos += 1

print(f"✅ ¡Magia completada! Se cambiaron {convertidos} archivos a .txt")