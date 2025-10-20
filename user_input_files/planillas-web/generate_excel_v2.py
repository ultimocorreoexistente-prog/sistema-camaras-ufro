import pandas as pd
from datetime import datetime

def modify_cameras_excel(input_file, output_file):
    """Modifica la planilla de cámaras agregando campos relacionales y procesando datos reales."""
    df = pd.read_excel(input_file)

    # Renombrar columnas existentes para facilitar el manejo
    df = df.rename(columns={
        "Nombre de cámara": "Nombre de Cámara",
        "Dirección IP del dispositivo": "IP de Cámara",
        "Nombre de dispositivo": "NVR/DVR Asociado (Original)",
        "N.º de serie del dispositivo.": "Número de Serie NVR/DVR (Original)",
        "N.º de versión del dispositivo": "Versión Firmware NVR/DVR (Original)",
        "Estado en línea": "Estado de Conexión",
        "Configuración del horario de grabación": "Horario de Grabación",
        "Ajustes de almacenamiento de imágenes": "Almacenamiento",
        "Área": "Campus/Edificio",
        "Fabricante": "Fabricante NVR/DVR (Original)"
    })

    # Asegurarse de que las columnas clave existan para evitar errores
    required_cols = ["Nombre de Cámara", "IP de Cámara", "Campus/Edificio"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # Agregar nuevas columnas relacionales si no existen
    new_cols = {
        "Ubicación Específica": "",
        "Gabinete Asociado": "",
        "Switch Asociado": "",
        "Puerto Switch": "",
        "Tipo de Cámara": "",
        "Requiere POE Adicional": "No",
        "Tipo de Conexión": "",
        "Estado de Funcionamiento": "Funcionando",
        "Instalador": "",
        "Fecha de Instalación": "",
        "Observaciones": "",
        "NVR Asociado (Cámara)": "",
        "Puerto NVR (Cámara)": ""
    }
    for col, default_val in new_cols.items():
        if col not in df.columns:
            df[col] = default_val

    # Lógica para procesar el campo 'Campus/Edificio' y asignar 'Tipo de Cámara'
    for index, row in df.iterrows():
        area = str(row["Campus/Edificio"]).strip().upper()
        nombre_camara = str(row["Nombre de Cámara"]).strip().upper()

        if "PTZ" in nombre_camara or "PTZ" in area:
            df.loc[index, "Tipo de Cámara"] = "PTZ"
            # Intentar inferir ubicación si el área es genérica como 'CAM-PTZ'
            if area == "CAM-PTZ" or area == "PTZ":
                # Aquí se necesitaría una lógica más avanzada o una tabla de mapeo
                # Por ahora, se dejarán los campos de ubicación y conectividad en blanco
                # para que el usuario los complete o se infieran de otras fuentes.
                df.loc[index, "Campus/Edificio"] = ""
                df.loc[index, "Ubicación Específica"] = ""
                df.loc[index, "Gabinete Asociado"] = ""
                df.loc[index, "Switch Asociado"] = ""
                df.loc[index, "Puerto Switch"] = ""
                df.loc[index, "NVR Asociado (Cámara)"] = ""
                df.loc[index, "Puerto NVR (Cámara)"] = ""
        elif "DOMO" in nombre_camara:
            df.loc[index, "Tipo de Cámara"] = "Domo"
        elif "BULLET" in nombre_camara:
            df.loc[index, "Tipo de Cámara"] = "Bullet"
        # Puedes añadir más tipos de cámaras aquí

        # Si el campo Campus/Edificio es un NVR (ej. NVR-AM), se asume que la cámara está en ese NVR
        if area.startswith("NVR-"):
            df.loc[index, "NVR Asociado (Cámara)"] = area
            # Se podría intentar inferir el puerto del NVR si hay un patrón en el nombre de la cámara
            # Por ejemplo, si el nombre es 'CAMARA_NVR-AM_PUERTO01', se extraería '01'

    # Reordenar columnas
    column_order = [
        "Nombre de Cámara", "IP de Cámara", "Ubicación Específica", 
        "Campus/Edificio", "Gabinete Asociado", "Switch Asociado", "Puerto Switch",
        "NVR Asociado (Cámara)", "Puerto NVR (Cámara)",
        "Tipo de Cámara", "Requiere POE Adicional", "Tipo de Conexión",
        "Estado de Funcionamiento", "Instalador", "Fecha de Instalación",
        "NVR/DVR Asociado (Original)", "Número de Serie NVR/DVR (Original)", "Versión Firmware NVR/DVR (Original)",
        "Fabricante NVR/DVR (Original)", "Estado de Conexión", "Horario de Grabación",
        "Almacenamiento", "Configurar el nombre del servidor de transmisión",
        "Configurar la dirección del servidor de transmisión", "Observaciones"
    ]
    df = df[column_order]

    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de cámaras modificado: {output_file}")
    return df

def create_gabinetes_excel(output_file):
    """Crea planilla de gabinetes/racks"""
    df = pd.DataFrame({
        "ID Gabinete": ["GAB-001", "GAB-002", "GAB-003"],
        "Nombre de Gabinete": ["Rack Edificio O - 3P", "Gabinete Subterráneo Francisco Salazar", "Gabinete Poste Principal"],
        "Tipo de Ubicación General": ["Interior", "Subterráneo", "Exterior"],
        "Tipo de Ubicación Detallada": ["Dentro de Edificio (Piso)", "Cámara Subterránea", "En Poste"],
        "Campus/Edificio": ["Edificio O", "Francisco Salazar", "Acceso Principal"],
        "Piso/Nivel": ["3er Piso", "N/A", "N/A"],
        "Ubicación Detallada": ["Sala técnica 3er piso", "Cámara subterránea acceso norte, cercano a estacionamiento", "Poste de luz principal, cercano a garita de seguridad"],
        "Referencia de Ubicación": ["Junto a sala de servidores", "A 5 metros de la entrada del estacionamiento", "Frente a la garita de seguridad"],
        "Estado": ["Funcionando", "Funcionando", "Funcionando"],
        "Fecha de Última Revisión": ["13/10/2025", "", ""],
        "Tiene UPS": ["Sí", "No", "No"],
        "Tiene Switch": ["Sí", "Sí", "Sí"],
        "Tiene NVR/DVR": ["No", "No", "No"],
        "Conexión Fibra Óptica": ["Sí", "Sí", "No"],
        "Observaciones": ["Cambio de batería UPS 13/10/2025", "Requiere revisión de humedad", "Alimenta cámaras perimetrales"]
    })
    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de gabinetes creado: {output_file}")

def create_switches_excel(output_file):
    """Crea planilla de switches con información de puertos"""
    df = pd.DataFrame({
        "ID Switch": ["SW-001", "SW-002", "SW-003"],
        "Nombre/Modelo": ["Switch PoE 24 puertos", "Switch PoE 8 puertos", "Switch PoE 4 puertos"],
        "Marca": ["Cisco", "TP-Link", "Ubiquiti"],
        "Número de Serie": ["SN-SW001", "SN-SW002", "SN-SW003"],
        "Gabinete Asociado": ["GAB-001", "GAB-002", "GAB-003"],
        "Número Total de Puertos": [24, 8, 4],
        "Puertos Usados": [12, 2, 3],
        "Puertos Disponibles": [12, 6, 1],
        "Soporta PoE": ["Sí", "Sí", "Sí"],
        "Estado": ["Funcionando", "Funcionando", "Funcionando"],
        "Fecha de Instalación": ["2023-01-15", "2024-03-10", "2024-07-20"],
        "Fecha de Último Mantenimiento": ["2025-09-01", "", ""],
        "Observaciones": ["Conecta 10 cámaras domo + 1 PTZ + enlace fibra", "Conecta 1 cámara PTZ + POE adicional", "Alimenta 3 cámaras bullet"]
    })
    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de switches creado: {output_file}")

def create_puertos_switch_excel(output_file):
    """Crea planilla detallada de puertos de switch"""
    df = pd.DataFrame({
        "ID Switch": ["SW-001", "SW-001", "SW-001", "SW-002", "SW-003", "SW-003"],
        "Número de Puerto": [1, 2, 3, 1, 1, 2],
        "Estado Puerto": ["En uso", "En uso", "En uso", "En uso", "En uso", "En uso"],
        "Dispositivo Conectado": ["Cámara Domo 1P-01", "Cámara Domo 1P-02", "Cámara Domo 1P-03", "Cámara PTZ Francisco Salazar", "Cámara Bullet Perimetral 1", "Cámara Bullet Perimetral 2"],
        "IP Dispositivo": ["192.168.1.101", "192.168.1.102", "192.168.1.103", "192.168.2.101", "192.168.3.101", "192.168.3.102"],
        "Tipo de Conexión": ["PoE", "PoE", "PoE", "PoE", "PoE", "PoE"],
        "NVR Asociado (Puerto)": ["NVR-001", "NVR-001", "NVR-001", "NVR-002", "NVR-001", "NVR-001"], # NVR al que la cámara conectada a este puerto envía señal
        "Puerto NVR (Puerto)": ["1", "2", "3", "1", "4", "5"], # Puerto específico del NVR
        "Observaciones": ["", "", "", "Requiere POE adicional externo", "", ""]
    })
    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de puertos de switch creado: {output_file}")

def create_equipos_excel(output_file):
    """Crea planilla de equipos técnicos (UPS, POE, Fuentes, NVR/DVR)"""
    df = pd.DataFrame({
        "ID Equipo": ["UPS-001", "POE-001", "NVR-001", "NVR-002"],
        "Tipo de Equipo": ["UPS", "POE Externo", "NVR", "NVR"],
        "Marca": ["APC", "Ubiquiti", "Hikvision", "Dahua"],
        "Modelo": ["Smart-UPS 1500", "POE-48-24W", "DS-7616NI-I2/16P", "DHI-NVR4108HS-8P-4KS2"],
        "Número de Serie": ["UPS-SN001", "POE-SN001", "NVR-SN001", "NVR-SN002"],
        "Capacidad (VA/W/Canales)": ["1500 VA", "24W", "16 Canales", "8 Canales"],
        "Número de Baterías": [1, 0, 0, 0],
        "Gabinete Asociado": ["GAB-001", "GAB-002", "GAB-001", "GAB-002"],
        "Alimenta a": ["Switch SW-001, NVR-001", "Cámara PTZ Francisco Salazar", "Cámaras conectadas a SW-001 y SW-003", "Cámaras conectadas a SW-002"],
        "Estado": ["Funcionando", "Funcionando", "Funcionando", "Funcionando"],
        "Fecha de Instalación": ["2023-01-15", "2024-03-10", "2023-01-15", "2024-03-10"],
        "Fecha de Último Mantenimiento": ["2025-10-13", "", "", ""],
        "Tipo de Mantenimiento": ["Cambio de batería", "", "", ""],
        "Observaciones": ["Batería cambiada el 13/10/2025", "", "NVR principal del Edificio O", "NVR para cámaras de Francisco Salazar"]
    })
    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de equipos técnicos creado: {output_file}")

def create_fallas_excel(output_file):
    """Crea planilla de fallas"""
    df = pd.DataFrame({
        "ID Falla": [],
        "Fecha de Reporte": [],
        "Tipo de Falla": [],  # Cable roto, Cámara quemada, Vandalismo, Switch quemado, Fuente quemada, POE averiado, UPS averiado, NVR averiado, Poste dañado
        "Equipo/Cámara Afectado": [],
        "Gabinete Relacionado": [],
        "Switch Relacionado": [],
        "Puerto Afectado": [],
        "Descripción": [],
        "Impacto": [],  # Cámaras afectadas, servicios interrumpidos
        "Estado": [],  # Reportada, En proceso, Resuelta, Cerrada
        "Técnico Asignado": [], 
        "Fecha de Resolución": [],
        "Solución Aplicada": [],
        "Observaciones": []
    })
    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de fallas creado: {output_file}")

def create_mantenimientos_excel(output_file):
    """Crea planilla de mantenimientos"""
    df = pd.DataFrame({
        "ID Mantenimiento": ["MNT-001"],
        "Fecha Programada": ["13/10/2025"],
        "Fecha de Realización": ["13/10/2025"],
        "Tipo de Mantenimiento": ["Correctivo"],
        "Categoría": ["Cambio de batería"],
        "Equipo/Gabinete": ["UPS-001 / GAB-001"],
        "Ubicación": ["Edificio O - 3er Piso"],
        "Descripción del Trabajo": ["Cambio de 1 batería de UPS"],
        "Estado": ["Completado"],
        "Técnico Responsable": ["Técnico Propio"], 
        "Materiales Utilizados": ["1 Batería 12V 9Ah"],
        "Costo Aproximado": [""],
        "Equipos/Cámaras Afectadas": ["10 cámaras domo + 1 PTZ temporalmente sin respaldo"],
        "Tiempo de Ejecución": ["30 minutos"],
        "Observaciones": ["Mantenimiento exitoso, sistema operando normalmente"]
    })
    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de mantenimientos creado: {output_file}")

def create_ubicaciones_excel(output_file):
    """Crea planilla de ubicaciones para referencia"""
    df = pd.DataFrame({
        "ID Ubicación": ["UBI-001", "UBI-002", "UBI-003"],
        "Campus": ["Campus Principal", "Campus Principal", "Campus Principal"],
        "Edificio": ["Edificio O", "Edificio O", "Francisco Salazar"],
        "Piso/Nivel": ["1er Piso", "3er Piso", "Subterráneo"],
        "Zona": ["Pasillo principal", "Sala técnica", "Acceso norte"],
        "Gabinetes en Ubicación": ["", "GAB-001", "GAB-002"],
        "Cantidad de Cámaras": [3, 11, 1],
        "Observaciones": ["", "Punto central de distribución", "Acceso restringido"]
    })
    df.to_excel(output_file, index=False)
    print(f"✓ Archivo de ubicaciones creado: {output_file}")

def create_documentation(output_file):
    """Crea archivo de documentación explicando las relaciones"""
    doc = """# DOCUMENTACIÓN DEL SISTEMA DE GESTIÓN DE CÁMARAS - UFRO

## CAMBIOS REALIZADOS EN LA PLANILLA ORIGINAL

### Archivo: Listadecámaras_modificada.xlsx

**Columnas agregadas:**
1. Ubicación Específica - Detalle exacto de dónde está la cámara
2. Gabinete Asociado - ID del gabinete/rack al que se conecta
3. Switch Asociado - ID del switch que la conecta
4. Puerto Switch - Número de boca/puerto del switch
5. NVR Asociado (Cámara) - NVR al que la cámara envía señal
6. Puerto NVR (Cámara) - Puerto del NVR al que la cámara está conectada
7. Tipo de Cámara - Domo, PTZ, Bullet, etc.
8. Requiere POE Adicional - Para cámaras PTZ que necesitan POE externo
9. Tipo de Conexión - Directa, Fibra Óptica, etc.
10. Estado de Funcionamiento - Funcionando, Averiada, etc.
11. Instalador - Técnico propio o empresa subcontratista
12. Fecha de Instalación
13. Observaciones

**Columnas renombradas para mayor claridad:**
- "Nombre de cámara" → "Nombre de Cámara"
- "Dirección IP del dispositivo" → "IP de Cámara" (DATO MUY IMPORTANTE)
- "Nombre de dispositivo" → "NVR/DVR Asociado (Original)" (para evitar conflicto con el nuevo campo de NVR asociado a la cámara)
- Otras columnas técnicas renombradas para consistencia

**Manejo de Cámaras PTZ con 'Área' genérica:**
- Para cámaras donde el campo 'Área' original es genérico (ej. "CAM-PTZ"), se ha implementado una lógica para intentar inferir el `Tipo de Cámara` (PTZ). Los campos de ubicación y conectividad (`Ubicación Específica`, `Gabinete Asociado`, `Switch Asociado`, `Puerto Switch`, `NVR Asociado (Cámara)`, `Puerto NVR (Cámara)`) se dejarán en blanco si no se pueden inferir de forma fiable, para que puedan ser completados manualmente con la información precisa.
- Se prioriza el uso de `Ubicación Específica`, `Gabinete Asociado`, `Switch Asociado` y `Puerto Switch` para la localización y conectividad detallada.

## PLANILLAS NUEVAS CREADAS

### 1. Gabinetes.xlsx
Registra todos los gabinetes/racks del sistema con:
- **Tipo de Ubicación General:** Interior, Subterráneo, Exterior
- **Tipo de Ubicación Detallada:** Dentro de Edificio (Piso), Cámara Subterránea, En Poste, Adosado a Construcción
- Ubicación física detallada (Ej: Sala técnica 3er piso, Cámara subterránea acceso norte, Poste de luz principal)
- Referencia de Ubicación (Ej: Cercano a estacionamiento, Junto a sala de servidores)
- Equipamiento que contiene (UPS, Switch, NVR/DVR)
- Estado y fecha de última revisión
- Conexiones de fibra óptica

### 2. Switches.xlsx
Información de todos los switches con:
- Modelo, marca, número de serie
- **Gabinete donde está instalado**
- Cantidad de puertos (total, usados, disponibles)
- Capacidad PoE
- Fecha de mantenimiento

### 3. Puertos_Switch.xlsx
Detalle de cada puerto de cada switch:
- Qué dispositivo está conectado en cada puerto
- IP del dispositivo conectado
- Estado del puerto (En uso, Disponible, Averiado)
- Tipo de conexión (PoE, Fibra, etc.)
- **NVR Asociado (Puerto):** NVR al que la cámara conectada a este puerto envía señal
- **Puerto NVR (Puerto):** Puerto específico del NVR al que la cámara está conectada

### 4. Equipos_Tecnicos.xlsx
Registro de UPS, POE externos, Fuentes de poder, **NVR/DVRs**:
- Marca, modelo, capacidad (o canales para NVR)
- Número de baterías (para UPS)
- Gabinete asociado
- Qué equipos alimenta
- Historial de mantenimiento

### 5. Fallas.xlsx
Sistema de registro de fallas con:
- Tipos: Cables rotos, Cámaras quemadas, Vandalismo, Switches quemados, 
  Fuentes quemadas, POE averiado, UPS averiado, NVR averiado, Postes dañados
- Relación con gabinete, switch y puerto afectado
- Impacto en el sistema
- Seguimiento de resolución
- **Técnicos Asignables:** Técnico Propio, Oliver Carrasco, Marco Altamirano, Empresa Subcontratista (ej. ConectaSur)

### 6. Mantenimientos.xlsx
Historial de mantenimientos con:
- Tipo: Preventivo, Correctivo, Predictivo
- Equipo/gabinete intervenido
- Materiales utilizados
- Equipos/cámaras afectadas durante el mantenimiento
- Tiempo de ejecución y costo
- **Técnicos Responsables:** Técnico Propio, Oliver Carrasco, Marco Altamirano, Empresa Subcontratista (ej. ConectaSur)

### 7. Ubicaciones.xlsx
Catálogo de ubicaciones físicas:
- Campus, Edificio, Piso
- Gabinetes presentes
- Cantidad de cámaras por ubicación

## RELACIONES ENTRE PLANILLAS

```
UBICACIONES
    ↓
GABINETES (contienen)
    ↓
EQUIPOS TÉCNICOS (UPS, Switch, NVR/DVR)
    ↓
SWITCHES (tienen)
    ↓
PUERTOS SWITCH (conectan)
    ↓
CÁMARAS (con IP específica)
    ↓
NVRs (reciben señal de cámaras conectadas a puertos específicos)
```

## EJEMPLO DE CASO REAL (13/10/2025)

**Mantenimiento en Edificio O:**
- Ubicación: Edificio O - 3er Piso (Sala técnica)
- Gabinete: GAB-001 (Rack Edificio O - 3P)
- Equipo: UPS-001 (APC Smart-UPS 1500)
- Acción: Cambio de 1 batería
- Switch: SW-001 (24 puertos)
- Cámaras afectadas: 10 domo + 1 PTZ
- Conexión adicional: Enlace por fibra óptica a gabinete subterráneo (Cámara PTZ Francisco Salazar)

**Conexión de Cámara PTZ Francisco Salazar:**
- Ubicación: Subterráneo Francisco Salazar
- Gabinete: GAB-002
- Switch: SW-002 (8 puertos)
- Puerto: 1
- POE adicional: Sí (POE-001)
- Conexión: Fibra óptica desde GAB-001
- NVR Asociado: NVR-002
- Puerto NVR: 1

## DATOS IMPORTANTES

- **IP de Cámara**: Campo crítico para identificación y acceso
- **Puerto Switch**: Esencial para troubleshooting de conectividad
- **Gabinete Asociado**: Permite ubicar físicamente el problema
- **Fecha de Mantenimiento**: Control de historial de equipos
- **NVR Asociado (Cámara) y Puerto NVR (Cámara)**: Crucial para el seguimiento de grabaciones y visualización.

## USO DEL SISTEMA WEB

El sitio web integra todas estas planillas permitiendo:
- Visualización de relaciones entre componentes
- Búsqueda por IP, ubicación, gabinete o switch
- Registro rápido de fallas y mantenimientos
- Exportación de reportes
- Dashboard con estado general del sistema
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f"✓ Documentación creada: {output_file}")

if __name__ == "__main__":
    print("\n=== GENERANDO PLANILLAS DEL SISTEMA DE GESTIÓN DE CÁMARAS UFRO ===\n")
    
    # Modificar planilla original
    modify_cameras_excel("Listadecámaras.xlsx", "Listadecámaras_modificada.xlsx")
    
    # Crear nuevas planillas
    create_gabinetes_excel("Gabinetes.xlsx")
    create_switches_excel("Switches.xlsx")
    create_puertos_switch_excel("Puertos_Switch.xlsx")
    create_equipos_excel("Equipos_Tecnicos.xlsx")
    create_fallas_excel("Fallas.xlsx")
    create_mantenimientos_excel("Mantenimientos.xlsx")
    create_ubicaciones_excel("Ubicaciones.xlsx")
    
    # Crear documentación
    create_documentation("DOCUMENTACION_CAMBIOS.md")
    
    print("\n=== ✓ TODAS LAS PLANILLAS GENERADAS EXITOSAMENTE ===\n")

