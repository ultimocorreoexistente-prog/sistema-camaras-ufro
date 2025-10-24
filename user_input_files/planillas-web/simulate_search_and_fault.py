import pandas as pd

# --- 1. Búsqueda de una cámara ---
print("\n--- Búsqueda de Cámara ---")
try:
    cameras_df = pd.read_excel("/home/ubuntu/Listadecámaras_modificada.xlsx")
    # Buscar una cámara por su nombre (ejemplo)
    camera_name_to_find = "2030_Acceso_1P"
    found_camera = cameras_df[cameras_df["Nombre de Cámara"] == camera_name_to_find]

    if not found_camera.empty:
        print(f"Cámara encontrada: {camera_name_to_find}")
        print(found_camera.iloc[0][["Nombre de Cámara", "IP de Cámara", "Campus/Edificio", "Switch Asociado", "Puerto Switch"]].to_string())
    else:
        print(f"Cámara {camera_name_to_find} no encontrada.")
except FileNotFoundError:
    print("Error: Listadecámaras_modificada.xlsx no encontrada.")
except Exception as e:
    print(f"Error al buscar cámara: {e}")

# --- 2. Ingreso de una falla ---
print("\n--- Ingreso de Falla ---")
try:
    fallas_df = pd.read_excel("/home/ubuntu/Fallas_Actualizada.xlsx")

    # Crear una nueva entrada de falla
    new_fault = {
        "ID Falla": f"F-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}",
        "Fecha de Reporte": pd.Timestamp.now().strftime("%d/%m/%Y"),
        "Reportado Por": "Central de Monitoreo",
        "Tipo de Falla": "Problemas de Conectividad",
        "Subtipo": "Sin señal",
        "Cámara Afectada": camera_name_to_find, # Usamos la cámara buscada
        "Nombre de Cámara": camera_name_to_find,
        "IP de Cámara": "172.22.3.9", # Asumiendo la IP de la cámara de ejemplo
        "Ubicación": "Edificio O - 1er Piso",
        "Gabinete Relacionado": "GAB-001",
        "Switch Relacionado": "SW-001",
        "Puerto Afectado": 1,
        "Descripción": "Cámara no presenta señal de video. Posible problema de red.",
        "Impacto en Visibilidad": "Alto",
        "Afecta Visión Nocturna": "Sí",
        "Estado": "Reportada",
        "Prioridad": "Alta",
        "Técnico Asignado": "Técnico Propio",
        "Fecha de Resolución": None,
        "Solución Aplicada": None,
        "Materiales Utilizados": None,
        "Observaciones": "Se requiere revisión en sitio."
    }

    # Convertir la nueva falla a DataFrame y concatenar
    new_fault_df = pd.DataFrame([new_fault])
    updated_fallas_df = pd.concat([fallas_df, new_fault_df], ignore_index=True)

    # Guardar la planilla de fallas actualizada
    updated_fallas_df.to_excel("/home/ubuntu/Fallas_Actualizada.xlsx", index=False)
    print("Falla ingresada exitosamente en Fallas_Actualizada.xlsx")
    print("\nÚltima falla ingresada:")
    print(updated_fallas_df.tail(1).to_string())

except FileNotFoundError:
    print("Error: Fallas_Actualizada.xlsx no encontrada.")
except Exception as e:
    print(f"Error al ingresar falla: {e}")

