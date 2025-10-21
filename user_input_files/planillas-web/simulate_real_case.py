import pandas as pd
from datetime import datetime

# --- Cargar planillas ---
gabinetes_df = pd.read_excel("/home/ubuntu/Gabinetes.xlsx")
switches_df = pd.read_excel("/home/ubuntu/Switches.xlsx")
puertos_df = pd.read_excel("/home/ubuntu/Puertos_Switch.xlsx")
cameras_df = pd.read_excel("/home/ubuntu/Listadecámaras_modificada.xlsx")
fallas_df = pd.read_excel("/home/ubuntu/Fallas_Actualizada.xlsx")

# --- 1. Definir Gabinete del Bicicletero Central ---
gabinete_bicicletero_id = "GAB-004"
gabinete_bicicletero_name = "Gabinete Bicicletero Central"

if gabinete_bicicletero_id not in gabinetes_df["ID Gabinete"].values:
    new_gab = {
        "ID Gabinete": gabinete_bicicletero_id,
        "Nombre de Gabinete": gabinete_bicicletero_name,
        "Tipo de Ubicación General": "Exterior",
        "Tipo de Ubicación Detallada": "Adosado a Construcción",
        "Campus/Edificio": "Campus Principal",
        "Piso/Nivel": None,
        "Ubicación Detallada": "Bicicletero Central",
        "Referencia de Ubicación": "Cercano a Edificio Odontología",
        "Estado": "Funcionando",
        "Fecha de Última Revisión": datetime.now().strftime("%d/%m/%Y"),
        "Tiene UPS": "No",
        "Tiene Switch": "Sí",
        "Tiene NVR/DVR": "No",
        "Conexión Fibra Óptica": "Sí",
        "Observaciones": "Gabinete en bicicletero, sin respaldo de UPS."
    }
    gabinetes_df = pd.concat([gabinetes_df, pd.DataFrame([new_gab])], ignore_index=True)
    print(f"Gabinete {gabinete_bicicletero_id} creado/actualizado.")

# --- 2. Definir Switch del Bicicletero Central ---
switch_bicicletero_id = "SW-004"
switch_bicicletero_name = "Switch Bicicletero Central"

if switch_bicicletero_id not in switches_df["ID Switch"].values:
    new_sw = {
        "ID Switch": switch_bicicletero_id,
        "Nombre/Modelo": switch_bicicletero_name,
        "Marca": "Genérica",
        "Número de Serie": "SN-SW004",
        "Gabinete Asociado": gabinete_bicicletero_id,
        "Número Total de Puertos": 8,
        "Puertos Usados": 4, # 3 cámaras + 1 fibra
        "Puertos Disponibles": 4,
        "Soporta PoE": "Sí",
        "Estado": "Funcionando",
        "Fecha de Instalación": "15/08/2024",
        "Fecha de Último Mantenimiento": None,
        "Observaciones": "Sin UPS. Enlace de fibra desde Odontología."
    }
    switches_df = pd.concat([switches_df, pd.DataFrame([new_sw])], ignore_index=True)
    print(f"Switch {switch_bicicletero_id} creado/actualizado.")

# --- 3. Definir Conexión de Fibra Óptica ---
# Asumimos que hay un switch en Odontología (SW-ODONTO) y un puerto para la fibra
switch_odontologia_id = "SW-ODONTO"

# Añadir el enlace de fibra en Puertos_Switch.xlsx para SW-004
if not ((puertos_df["ID Switch"] == switch_bicicletero_id) & (puertos_df["Dispositivo Conectado"] == f"Enlace Fibra Óptica a {switch_odontologia_id}")).any():
    new_fiber_port = {
        "ID Switch": switch_bicicletero_id,
        "Número de Puerto": 8, # Último puerto
        "Estado Puerto": "En uso",
        "Dispositivo Conectado": f"Enlace Fibra Óptica a {switch_odontologia_id}",
        "IP Dispositivo": None,
        "Tipo de Conexión": "Fibra Óptica",
        "NVR Asociado (Puerto)": None,
        "Puerto NVR (Puerto)": None,
        "Observaciones": "Conexión de fibra óptica desde Edificio Odontología."
    }
    puertos_df = pd.concat([puertos_df, pd.DataFrame([new_fiber_port])], ignore_index=True)
    print(f"Enlace de fibra óptica para {switch_bicicletero_id} añadido.")

# --- 4. Definir Cámaras del Bicicletero Central ---
cameras_bicicletero = [
    {"Nombre de Cámara": "Bicicletero Central 1", "IP de Cámara": "172.22.4.101"},
    {"Nombre de Cámara": "Bicicletero Central 2", "IP de Cámara": "172.22.4.102"},
    {"Nombre de Cámara": "Bicicletero Central 3", "IP de Cámara": "172.22.4.103"},
]

for cam_data in cameras_bicicletero:
    cam_name = cam_data["Nombre de Cámara"]
    if cam_name not in cameras_df["Nombre de Cámara"].values:
        new_cam = {
            "Nombre de Cámara": cam_name,
            "IP de Cámara": cam_data["IP de Cámara"],
            "Ubicación Específica": "Bicicletero Central",
            "Campus/Edificio": "Campus Principal",
            "Gabinete Asociado": gabinete_bicicletero_id,
            "Switch Asociado": switch_bicicletero_id,
            "Puerto Switch": None, # Se asignará en puertos_df
            "NVR Asociado (Cámara)": "NVR-001", # Asumiendo que reportan al NVR principal
            "Puerto NVR (Cámara)": None,
            "Tipo de Cámara": "Bullet",
            "Requiere POE Adicional": "No",
            "Tipo de Conexión": "PoE",
            "Estado de Funcionamiento": "Fallando",
            "Instalador": "Técnico Propio",
            "Fecha de Instalación": "15/08/2024",
            "NVR/DVR Asociado (Original)": "NVR-001",
            "Observaciones": "Cámara en Bicicletero Central."
        }
        cameras_df = pd.concat([cameras_df, pd.DataFrame([new_cam])], ignore_index=True)
        print(f"Cámara {cam_name} creada/actualizada.")

# Asignar puertos a las cámaras del bicicletero
for i, cam_data in enumerate(cameras_bicicletero):
    cam_name = cam_data["Nombre de Cámara"]
    port_num = i + 1  # Puertos 1, 2, 3
    if not ((puertos_df["ID Switch"] == switch_bicicletero_id) & (puertos_df["Dispositivo Conectado"] == cam_name)).any():
        new_cam_port = {
            "ID Switch": switch_bicicletero_id,
            "Número de Puerto": port_num,
            "Estado Puerto": "En uso",
            "Dispositivo Conectado": cam_name,
            "IP Dispositivo": cam_data["IP de Cámara"],
            "Tipo de Conexión": "PoE",
            "NVR Asociado (Puerto)": "NVR-001",
            "Puerto NVR (Puerto)": None,
            "Observaciones": "Conectada al switch del bicicletero."
        }
        puertos_df = pd.concat([puertos_df, pd.DataFrame([new_cam_port])], ignore_index=True)
        print(f"Puerto {port_num} del {switch_bicicletero_id} asignado a {cam_name}.")

# --- 5. Registrar la Falla ---
for cam_data in cameras_bicicletero:
    cam_name = cam_data["Nombre de Cámara"]
    new_fault_entry = {
        "ID Falla": f"F-{datetime.now().strftime('%Y%m%d%H%M%S')}-{cam_name.replace(' ', '_')}",
        "Fecha de Reporte": datetime.now().strftime("%d/%m/%Y"),
        "Reportado Por": "Central de Monitoreo",
        "Tipo de Falla": "Problemas de Alimentación",
        "Subtipo": "Falla de Energía",
        "Cámara Afectada": cam_name,
        "Nombre de Cámara": cam_name,
        "IP de Cámara": cam_data["IP de Cámara"],
        "Ubicación": "Bicicletero Central",
        "Gabinete Relacionado": gabinete_bicicletero_id,
        "Switch Relacionado": switch_bicicletero_id,
        "Puerto Afectado": None, # Se puede inferir del cam_name si se desea
        "Descripción": f"Cámara sin señal debido a la falta de energía en el switch del gabinete ({switch_bicicletero_id}) por ausencia de UPS.",
        "Impacto en Visibilidad": "Alto",
        "Afecta Visión Nocturna": "Sí",
        "Estado": "Reportada",
        "Prioridad": "Crítica",
        "Técnico Asignado": "Técnico Propio",
        "Fecha de Resolución": None,
        "Solución Aplicada": None,
        "Materiales Utilizados": None,
        "Observaciones": "Se requiere instalación de UPS o solución de energía para el switch."
    }
    fallas_df = pd.concat([fallas_df, pd.DataFrame([new_fault_entry])], ignore_index=True)
    print(f"Falla para {cam_name} registrada.")

# --- Guardar planillas actualizadas ---
gabinetes_df.to_excel("/home/ubuntu/Gabinetes.xlsx", index=False)
switches_df.to_excel("/home/ubuntu/Switches.xlsx", index=False)
puertos_df.to_excel("/home/ubuntu/Puertos_Switch.xlsx", index=False)
cameras_df.to_excel("/home/ubuntu/Listadecámaras_modificada.xlsx", index=False)
fallas_df.to_excel("/home/ubuntu/Fallas_Actualizada.xlsx", index=False)

print("\nPlanillas actualizadas con el caso real del Bicicletero Central.")

