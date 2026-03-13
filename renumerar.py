import os
import re

carpeta = os.path.dirname(os.path.abspath(__file__))

# obtener solo carpetas que empiezan con numero
carpetas = []

for nombre in os.listdir(carpeta):
    ruta = os.path.join(carpeta, nombre)

    if os.path.isdir(ruta):
        match = re.match(r"(\d+)\s-\s(.+)", nombre)
        if match:
            carpetas.append((int(match.group(1)), nombre))

# ordenar por numero actual
carpetas.sort()

contador = 1

for _, nombre in carpetas:

    ruta_vieja = os.path.join(carpeta, nombre)

    match = re.match(r"(\d+)\s-\s(.+)", nombre)
    resto = match.group(2)

    nuevo_num = f"{contador:02d}"
    nuevo_nombre = f"{nuevo_num} - {resto}"

    ruta_nueva = os.path.join(carpeta, nuevo_nombre)

    os.rename(ruta_vieja, ruta_nueva)

    print(f"Carpeta: {nombre} -> {nuevo_nombre}")

    # renombrar pkt dentro
    for archivo in os.listdir(ruta_nueva):

        if archivo.endswith(".pkt"):

            match_pkt = re.match(r"(\d+)\s-\s(.+)", archivo)

            if match_pkt:
                resto_pkt = match_pkt.group(2)
                nuevo_pkt = f"{nuevo_num} - {resto_pkt}"

                os.rename(
                    os.path.join(ruta_nueva, archivo),
                    os.path.join(ruta_nueva, nuevo_pkt)
                )

                print(f"   Archivo: {archivo} -> {nuevo_pkt}")

    contador += 1

print("Renumeración completa.")