import os
import re
import shutil

# --- CONFIGURACIÓN ---
# 1. Pon aquí la ruta exacta a tu carpeta CCNA-Packet-Tracer-Labs
REPO_DIR = r"C:\Users\WINDOWS\Desktop\CCNA-Packet-Tracer-Labs"

# 2. Pon aquí la ruta exacta a la carpeta de Obsidian donde están tus fotos
OBSIDIAN_IMG_DIR = r"C:\Obsidian\ZZZZZZZZZZZZZZZZZZZZZ"
# ---------------------

def fix_obsidian_images():
    # Busca el patrón ![[cualquier_cosa.png]]
    pattern = re.compile(r'!\[\[(.*?)\]\]')
    archivos_modificados = 0

    for root, dirs, files in os.walk(REPO_DIR):
        for file in files:
            if file == "README.md":
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                matches = pattern.findall(content)
                if not matches:
                    continue
                    
                print(f"\nProcesando: {os.path.basename(root)}/README.md")
                new_content = content
                
                for img_name in matches:
                    clean_name = img_name.replace(" ", "-") # Cambia espacios por guiones
                    
                    src_img_path = os.path.join(OBSIDIAN_IMG_DIR, img_name)
                    dest_img_path = os.path.join(root, clean_name)
                    
                    # Copia la imagen
                    if os.path.exists(src_img_path):
                        shutil.copy2(src_img_path, dest_img_path)
                        print(f"  [+] Copiada: {clean_name}")
                    else:
                        print(f"  [-] ERROR: No se encontró {img_name} en Obsidian.")
                    
                    # Actualiza el texto
                    old_tag = f"![[{img_name}]]"
                    new_tag = f"![]({clean_name})"
                    new_content = new_content.replace(old_tag, new_tag)
                    
                # Guarda el archivo corregido
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                archivos_modificados += 1

    print(f"\n¡Listo! Se actualizaron {archivos_modificados} archivos README.")

if __name__ == "__main__":
    fix_obsidian_images()