import pandas as pd

def modify_cameras_excel(input_file, output_file):
    df = pd.read_excel(input_file)

    # Add new columns based on the requirements from pasted_content.txt
    # Initialize with default or placeholder values
    df["Ubicación"] = ""
    df["Tipo de Conexión"] = ""
    df["Asociación con Gabinetes"] = ""
    df["Estado de Funcionamiento"] = "Funcionando"
    df["Tipo de Cámara"] = ""
    df["POE"] = "No"
    df["Instalador"] = ""
    df["Modelo de Cámara"] = ""
    df["Número de Serie de Cámara"] = ""
    df["Marca de Cámara"] = ""

    # Rename existing columns for clarity and consistency
    df = df.rename(columns={
        "Nombre de cámara": "Nombre de Cámara",
        "Dirección IP del dispositivo": "IP de Cámara",
        "Nombre de dispositivo": "NVR/DVR Asociado",
        "N.º de serie del dispositivo.": "Número de Serie NVR/DVR",
        "N.º de versión del dispositivo": "Versión Firmware NVR/DVR",
        "Estado en línea": "Estado de Conexión",
        "Configuración del horario de grabación": "Horario de Grabación",
        "Ajustes de almacenamiento de imágenes": "Almacenamiento de Imágenes",
        "Área": "Campus/Edificio",
        "Fabricante": "Fabricante NVR/DVR"
    })

    # Reorder columns for better readability
    column_order = [
        "Nombre de Cámara", "IP de Cámara", "Ubicación", "Tipo de Conexión",
        "Asociación con Gabinetes", "Estado de Funcionamiento", "Tipo de Cámara", "POE",
        "Instalador", "Marca de Cámara", "Modelo de Cámara", "Número de Serie de Cámara",
        "NVR/DVR Asociado", "Número de Serie NVR/DVR", "Versión Firmware NVR/DVR",
        "Estado de Conexión", "Horario de Grabación", "Almacenamiento de Imágenes",
        "Campus/Edificio", "Fabricante NVR/DVR", "Configurar el nombre del servidor de transmisión",
        "Configurar la dirección del servidor de transmisión"
    ]
    df = df[column_order]

    df.to_excel(output_file, index=False)
    print(f"Archivo de cámaras modificado y guardado como {output_file}")

def create_new_excels(output_dir="./"):
    # Gabinetes
    df_gabinetes = pd.DataFrame({
        "Nombre de Gabinete": [],
        "Ubicación": [], # Subterráneo, Interior dependencia, Exterior dependencia, Poste
        "Campus/Edificio": [],
        "Estado": [], # Funcionando, Averiado, En mantenimiento, Fuera de servicio
        "Fecha de Última Revisión": [],
        "Equipamiento (UPS)": [],
        "Equipamiento (Switch)": [],
        "Equipamiento (NVR/DVR)": [],
        "Observaciones": []
    })
    df_gabinetes.to_excel(f"{output_dir}Gabinetes.xlsx", index=False)
    print(f"Archivo Gabinetes.xlsx creado en {output_dir}")

    # Equipos Técnicos (UPS, Switch, NVR/DVR, Fuentes de Poder)
    df_equipos = pd.DataFrame({
        "Tipo de Equipo": [], # UPS, Switch, NVR/DVR, Fuente de Poder
        "Marca": [],
        "Modelo": [],
        "Número de Serie": [],
        "Asociado a Gabinete": [],
        "Estado": [], # Funcionando, Averiado, En mantenimiento, Fuera de servicio
        "Capacidad (UPS)": [],
        "Número de Baterías (UPS)": [],
        "Fecha de Último Mantenimiento": [],
        "Observaciones": []
    })
    df_equipos.to_excel(f"{output_dir}Equipos_Tecnicos.xlsx", index=False)
    print(f"Archivo Equipos_Tecnicos.xlsx creado en {output_dir}")

    # Fallas
    df_fallas = pd.DataFrame({
        "ID de Falla": [],
        "Tipo de Falla": [], # Cables rotos, Cámaras que se queman, Cámaras vandalizadas, Cámaras que dejan de funcionar, Fuentes que se queman, Switches que se queman, Postes que se dañan, UPS averiados, NVR averiados
        "Equipo/Cámara Afectado": [],
        "Fecha de Reporte": [],
        "Estado": [], # Reportada, En proceso, Resuelta, Cerrada
        "Descripción": [],
        "Técnico Asignado": [],
        "Fecha de Resolución": []
    })
    df_fallas.to_excel(f"{output_dir}Fallas.xlsx", index=False)
    print(f"Archivo Fallas.xlsx creado en {output_dir}")

    # Mantenimientos
    df_mantenimientos = pd.DataFrame({
        "ID de Mantenimiento": [],
        "Tipo de Mantenimiento": [], # Preventivo, Correctivo, Predictivo
        "Equipo/Cámara/Gabinete": [],
        "Fecha Programada": [],
        "Fecha de Realización": [],
        "Estado": [], # Programado, En proceso, Completado, Cancelado
        "Descripción del Trabajo": [],
        "Técnico Responsable": [],
        "Materiales Utilizados": [],
        "Observaciones": []
    })
    df_mantenimientos.to_excel(f"{output_dir}Mantenimientos.xlsx", index=False)
    print(f"Archivo Mantenimientos.xlsx creado en {output_dir}")

if __name__ == "__main__":
    modify_cameras_excel("Listadecámaras.xlsx", "Listadecámaras_modificada.xlsx")
    create_new_excels()

