# Este programa es para convertir de .doc a .docx
import os
import win32com.client

def convertir_doc_a_docx(directorio):
    print("Iniciando conversión masiva de .doc a .docx...")
    
    # Abrimos Microsoft Word en modo invisible
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    convertidos = 0

    for archivo in os.listdir(directorio):
        # Buscamos específicamente los archivos .doc antiguos
        if archivo.lower().endswith(".doc"):
            ruta_doc = os.path.abspath(os.path.join(directorio, archivo))
            ruta_docx = ruta_doc + "x"  # Le agregamos la 'x' para que sea .docx
            
            # Si el .docx ya existe, lo saltamos para no duplicar trabajo
            if os.path.exists(ruta_docx):
                continue
                
            print(f"🔄 Convirtiendo: {archivo} ...")
            try:
                # Abrimos el doc y lo guardamos como docx (FileFormat=16)
                documento = word.Documents.Open(ruta_doc)
                documento.SaveAs2(ruta_docx, FileFormat=16)
                documento.Close()
                convertidos += 1
            except Exception as e:
                print(f"❌ Error con {archivo}: {e}")

    word.Quit()
    print(f"✅ ¡Listo! Se convirtieron {convertidos} archivos al formato moderno.")

# Pon la ruta de tu carpeta
ruta_archivos = r"C:\Users\pcast\OneDrive\Desktop\proyecto_leyes\pdfs_originales\Codigos_Civiles_Penales_ProcedimientosCiviles_ESTATALES\Baja_California_Sur"
convertir_doc_a_docx(ruta_archivos)