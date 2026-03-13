import os
import re
import shutil

# --- CONFIGURACIÓN ---
# 1. Ruta a tu carpeta CCNA
REPO_DIR = r"C:\Users\WINDOWS\Desktop\CCNA-Packet-Tracer-Labs"

# 2. Ruta a la carpeta PRINCIPAL de Obsidian
OBSIDIAN_IMG_DIR = r"C:\Obsidian\ZZZZZZZZZZZZZZZZZZZZZ" 
# ---------------------

def fix_obsidian_images():
    print("Escaneando todas las carpetas de Obsidian en busca de imágenes...")
    
    mapa_imagenes = {}
    for root, dirs, files in os.walk(OBSIDIAN_IMG_DIR):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                mapa_imagenes[file] = os.path.join(root, file)
                
    print(f"¡Se encontraron {len(mapa_imagenes)} imágenes en total!\n")

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
                    
                print(f"Procesando: {os.path.basename(root)}/README.md")
                new_content = content
                
                for raw_img_name in matches:
                    # Filtro que ignora el tamaño |697
                    img_name_puro = raw_img_name.split('|')[0] 
                    clean_name = img_name_puro.replace(" ", "-") 
                    
                    if img_name_puro in mapa_imagenes:
                        src_img_path = mapa_imagenes[img_name_puro]
                        dest_img_path = os.path.join(root, clean_name)
                        
                        if not os.path.exists(dest_img_path):
                            shutil.copy2(src_img_path, dest_img_path)
                            print(f"  [+] Copiada: {clean_name}")
                    else:
                        print(f"  [-] ERROR: No se encontró la imagen '{img_name_puro}' en ninguna subcarpeta.")
                    
                    old_tag = f"![[{raw_img_name}]]"
                    new_tag = f"![]({clean_name})"
                    new_content = new_content.replace(old_tag, new_tag)
                    
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                archivos_modificados += 1

    print(f"\n¡Listo! Se actualizaron {archivos_modificados} laboratorios.")

if __name__ == "__main__":
    fix_obsidian_images()