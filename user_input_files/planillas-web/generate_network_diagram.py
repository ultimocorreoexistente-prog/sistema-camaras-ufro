import pandas as pd
import re

def clean_id(text):
    # Reemplazar caracteres no alfanuméricos con guiones bajos
    cleaned_text = re.sub(r'[^a-zA-Z0-9_]', '_', str(text))
    # Asegurarse de que el ID no comience con un número (Mermaid restriction)
    if cleaned_text and cleaned_text[0].isdigit():
        cleaned_text = 'ID_' + cleaned_text
    return cleaned_text

def generate_mermaid_diagram(cameras_df, gabinetes_df, switches_df, puertos_df, equipos_df):
    diagram = ["graph LR"]

    # 1. Nodos de Gabinetes
    for index, row in gabinetes_df.iterrows():
        gab_id = clean_id(row["ID Gabinete"])
        gab_name = str(row["Nombre de Gabinete"])
        gab_location = str(row["Ubicación Detallada"])
        diagram.append(f"  {gab_id}[\"{gab_name}\\n({gab_location})\"]")

    # 2. Nodos de Switches y NVRs, y sus conexiones a Gabinetes
    for index, row in switches_df.iterrows():
        sw_id = clean_id(row["ID Switch"])
        sw_name = str(row["Nombre/Modelo"])
        gab_assoc = clean_id(row["Gabinete Asociado"])
        diagram.append(f"  {sw_id}[\"{sw_name}\"]")
        if pd.notna(row["Gabinete Asociado"]):
            diagram.append(f"  {gab_assoc} -- \"Contiene\" --> {sw_id}")

    for index, row in equipos_df.iterrows():
        if row["Tipo de Equipo"] == "NVR":
            nvr_id = clean_id(row["ID Equipo"])
            nvr_name = str(row["Modelo"])
            gab_assoc = clean_id(row["Gabinete Asociado"])
            diagram.append(f"  {nvr_id}[\"NVR {nvr_name}\"]")
            if pd.notna(row["Gabinete Asociado"]):
                diagram.append(f"  {gab_assoc} -- \"Contiene\" --> {nvr_id}")

    # 3. Nodos de Cámaras y sus conexiones a Switches y NVRs
    for index, row in puertos_df.iterrows():
        sw_id = clean_id(row["ID Switch"])
        port_num = str(row["Número de Puerto"])
        device_connected = str(row["Dispositivo Conectado"])
        ip_device = str(row["IP Dispositivo"])
        nvr_assoc_port = clean_id(row["NVR Asociado (Puerto)"])
        port_nvr = str(row["Puerto NVR (Puerto)"])

        if pd.notna(device_connected) and "Cámara" in device_connected:
            cam_id = clean_id(device_connected)
            diagram.append(f"  {cam_id}[\"{device_connected}\\n({ip_device})\"]")
            diagram.append(f"  {sw_id} -- \"Puerto {port_num}\" --> {cam_id}")
            if pd.notna(row["NVR Asociado (Puerto)"]):
                diagram.append(f"  {cam_id} -- \"Envía a NVR {port_nvr}\" --> {nvr_assoc_port}")

    return "\n".join(diagram)

# Cargar los DataFrames
cameras_df = pd.read_excel("/home/ubuntu/upload/.recovery/Listadecámaras_modificada.xlsx")
gabinetes_df = pd.read_excel("/home/ubuntu/upload/.recovery/Gabinetes.xlsx")
switches_df = pd.read_excel("/home/ubuntu/upload/.recovery/Switches.xlsx")
puertos_df = pd.read_excel("/home/ubuntu/upload/.recovery/Puertos_Switch.xlsx")
equipos_df = pd.read_excel("/home/ubuntu/upload/.recovery/Equipos_Tecnicos.xlsx")

mermaid_code = generate_mermaid_diagram(cameras_df, gabinetes_df, switches_df, puertos_df, equipos_df)

with open("network_diagram.md", "w", encoding="utf-8") as f:
    f.write(f"```mermaid\n{mermaid_code}\n```")

print("Diagrama de red generado en network_diagram.md")

