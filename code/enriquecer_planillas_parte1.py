import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
import os

planillas_dir = 'user_input_files/planillas-web'

print("=== ENRIQUECIMIENTO DE PLANILLAS EXCEL ===")
print()

# ============================================================================
# 1. UBICACIONES - Añadir más ubicaciones
# ============================================================================
print("📍 Enriqueciendo Ubicaciones.xlsx...")

ubicaciones_path = os.path.join(planillas_dir, 'Ubicaciones.xlsx')
df_ubi = pd.read_excel(ubicaciones_path)

nuevas_ubicaciones = [
    {'ID Ubicación': 'UBI-004', 'Campus': 'Campus Principal', 'Edificio': 'Edificio L (Odontología)', 
     'Piso/Nivel': '2do Piso', 'Zona': 'Pasillo principal', 'Gabinetes en Ubicación': 'GAB-003', 
     'Cantidad de Cámaras': 8, 'Observaciones': 'Zona de tránsito alto'},
    
    {'ID Ubicación': 'UBI-005', 'Campus': 'Campus Principal', 'Edificio': 'Bunker', 
     'Piso/Nivel': 'Exterior', 'Zona': 'Acceso principal', 'Gabinetes en Ubicación': None, 
     'Cantidad de Cámaras': 2, 'Observaciones': 'Exposición a elementos'},
    
    {'ID Ubicación': 'UBI-006', 'Campus': 'Campus Pucón', 'Edificio': 'Edificio Principal', 
     'Piso/Nivel': '1er Piso', 'Zona': 'Recepción', 'Gabinetes en Ubicación': 'GAB-004', 
     'Cantidad de Cámaras': 5, 'Observaciones': 'Control de acceso'},
    
    {'ID Ubicación': 'UBI-007', 'Campus': 'Campus Angol', 'Edificio': 'CFT Prat', 
     'Piso/Nivel': '1er Piso', 'Zona': 'Sala servidores', 'Gabinetes en Ubicación': 'GAB-005', 
     'Cantidad de Cámaras': 13, 'Observaciones': 'Centro de red campus Angol'},
    
    {'ID Ubicación': 'UBI-008', 'Campus': 'Campus Principal', 'Edificio': 'Zona ZM', 
     'Piso/Nivel': 'Exterior', 'Zona': 'Ciclovía', 'Gabinetes en Ubicación': None, 
     'Cantidad de Cámaras': 3, 'Observaciones': 'Zona de transporte'},
]

df_ubi_nuevas = pd.DataFrame(nuevas_ubicaciones)
df_ubi_completa = pd.concat([df_ubi, df_ubi_nuevas], ignore_index=True)
df_ubi_completa.to_excel(ubicaciones_path, index=False)
print(f"  ✓ Ubicaciones: {len(df_ubi)} → {len(df_ubi_completa)} registros")

# ============================================================================
# 2. GABINETES - Añadir más gabinetes
# ============================================================================
print("📦 Enriqueciendo Gabinetes.xlsx...")

gabinetes_path = os.path.join(planillas_dir, 'Gabinetes.xlsx')
df_gab = pd.read_excel(gabinetes_path)

nuevos_gabinetes = [
    {'ID Gabinete': 'GAB-004', 'ID Ubicación': 'UBI-006', 'Tipo': 'Gabinete Exterior IP65', 
     'Dimensiones': '60x40x25 cm', 'Marca': 'Outdoor Tech', 'Material': 'Acero inoxidable', 
     'Capacidad Equipos': '8U', 'Switches Instalados': 1, 'UPS Instalados': 1, 
     'Fuentes Instaladas': 0, 'NVR/DVR Instalados': 1, 'Estado': 'Activo', 
     'Fecha Instalación': '2024-08-05', 'Fecha Última Revisión': '2025-10-01', 
     'Temperatura Promedio (°C)': 28.5, 'Observaciones': 'Requiere ventilación adicional'},
    
    {'ID Gabinete': 'GAB-005', 'ID Ubicación': 'UBI-007', 'Tipo': 'Rack 12U', 
     'Dimensiones': '60x60x60 cm', 'Marca': 'Panduit', 'Material': 'Acero', 
     'Capacidad Equipos': '12U', 'Switches Instalados': 2, 'UPS Instalados': 1, 
     'Fuentes Instaladas': 1, 'NVR/DVR Instalados': 1, 'Estado': 'Activo', 
     'Fecha Instalación': '2024-05-12', 'Fecha Última Revisión': '2025-09-18', 
     'Temperatura Promedio (°C)': 22.0, 'Observaciones': 'Gabinete central campus Angol'},
    
    {'ID Gabinete': 'GAB-006', 'ID Ubicación': 'UBI-004', 'Tipo': 'Gabinete Mural 6U', 
     'Dimensiones': '60x45x30 cm', 'Marca': 'APC', 'Material': 'Acero', 
     'Capacidad Equipos': '6U', 'Switches Instalados': 1, 'UPS Instalados': 0, 
     'Fuentes Instaladas': 1, 'NVR/DVR Instalados': 0, 'Estado': 'Activo', 
     'Fecha Instalación': '2024-06-20', 'Fecha Última Revisión': '2025-10-10', 
     'Temperatura Promedio (°C)': 24.8, 'Observaciones': 'Alimenta cámaras Edificio L'},
]

df_gab_nuevos = pd.DataFrame(nuevos_gabinetes)
df_gab_completa = pd.concat([df_gab, df_gab_nuevos], ignore_index=True)
df_gab_completa.to_excel(gabinetes_path, index=False)
print(f"  ✓ Gabinetes: {len(df_gab)} → {len(df_gab_completa)} registros")

# ============================================================================
# 3. UPS - Añadir más unidades
# ============================================================================
print("⚡ Enriqueciendo UPS.xlsx...")

ups_path = os.path.join(planillas_dir, 'UPS.xlsx')
df_ups = pd.read_excel(ups_path)

nuevos_ups = [
    {'ID UPS': 'UPS-002', 'ID Ubicación': 'UBI-006', 'Modelo': 'Smart-UPS 1000', 
     'Marca': 'APC', 'Capacidad (VA)': 1000, 'Número de Baterías': 1, 
     'Gabinete Asociado': 'GAB-004', 'Ubicación': 'Campus Pucón - Recepción', 
     'Campus': 'Campus Pucón', 'Estado': 'Activo', 'Fecha Instalación': '2024-08-05', 
     'Equipos que Alimenta': '1 Switch + 5 cámaras', 'Última Mantención': '2025-08-05', 
     'Costo Última Mantención': 25000, 'Observaciones': 'Protección básica'},
    
    {'ID UPS': 'UPS-003', 'ID Ubicación': 'UBI-007', 'Modelo': 'Smart-UPS 2200', 
     'Marca': 'APC', 'Capacidad (VA)': 2200, 'Número de Baterías': 2, 
     'Gabinete Asociado': 'GAB-005', 'Ubicación': 'CFT Prat - Sala servidores', 
     'Campus': 'Campus Angol', 'Estado': 'Activo', 'Fecha Instalación': '2024-05-12', 
     'Equipos que Alimenta': '2 Switches + 1 NVR + 13 cámaras', 'Última Mantención': '2025-05-12', 
     'Costo Última Mantención': 65000, 'Observaciones': 'Punto crítico - UPS redundante'},
    
    {'ID UPS': 'UPS-004', 'ID Ubicación': 'UBI-004', 'Modelo': 'Back-UPS 700', 
     'Marca': 'Tripp Lite', 'Capacidad (VA)': 700, 'Número de Baterías': 1, 
     'Gabinete Asociado': 'GAB-006', 'Ubicación': 'Edificio L - 2do Piso', 
     'Campus': 'Campus Principal', 'Estado': 'Activo', 'Fecha Instalación': '2024-06-20', 
     'Equipos que Alimenta': '1 Switch + 8 cámaras', 'Última Mantención': None, 
     'Costo Última Mantención': None, 'Observaciones': 'Pendiente primera mantención'},
]

df_ups_nuevos = pd.DataFrame(nuevos_ups)
df_ups_completa = pd.concat([df_ups, df_ups_nuevos], ignore_index=True)
df_ups_completa.to_excel(ups_path, index=False)
print(f"  ✓ UPS: {len(df_ups)} → {len(df_ups_completa)} registros")

# ============================================================================
# 4. SWITCHES - Añadir más switches
# ============================================================================
print("🔌 Enriqueciendo Switches.xlsx...")

switches_path = os.path.join(planillas_dir, 'Switches.xlsx')
df_sw = pd.read_excel(switches_path)

nuevos_switches = [
    {'ID Switch': 'SW-004', 'ID Ubicación': 'UBI-006', 'Tipo': 'Switch PoE 8 puertos', 
     'Marca': 'TP-Link', 'Modelo': 'TL-SG1008P', 'Número Serie': 'SN-SW004', 
     'Gabinete': 'GAB-004', 'Total Puertos': 8, 'Puertos Usados': 5, 
     'Puertos Disponibles': 3, 'PoE': 'Sí', 'Estado': 'Funcionando', 
     'Fecha Instalación': '2024-08-05', 'Fecha Último Mantenimiento': None, 
     'Observaciones': 'Switch campus Pucón'},
    
    {'ID Switch': 'SW-005', 'ID Ubicación': 'UBI-007', 'Tipo': 'Switch PoE 24 puertos', 
     'Marca': 'Cisco', 'Modelo': 'SG350-28P', 'Número Serie': 'SN-SW005', 
     'Gabinete': 'GAB-005', 'Total Puertos': 24, 'Puertos Usados': 15, 
     'Puertos Disponibles': 9, 'PoE': 'Sí', 'Estado': 'Funcionando', 
     'Fecha Instalación': '2024-05-12', 'Fecha Último Mantenimiento': '2025-09-18', 
     'Observaciones': 'Switch principal CFT Prat'},
    
    {'ID Switch': 'SW-006', 'ID Ubicación': 'UBI-004', 'Tipo': 'Switch PoE 8 puertos', 
     'Marca': 'Ubiquiti', 'Modelo': 'US-8-150W', 'Número Serie': 'SN-SW006', 
     'Gabinete': 'GAB-006', 'Total Puertos': 8, 'Puertos Usados': 8, 
     'Puertos Disponibles': 0, 'PoE': 'Sí', 'Estado': 'Funcionando', 
     'Fecha Instalación': '2024-06-20', 'Fecha Último Mantenimiento': '2025-10-10', 
     'Observaciones': 'Sin puertos disponibles - considerar ampliación'},
]

df_sw_nuevos = pd.DataFrame(nuevos_switches)
df_sw_completa = pd.concat([df_sw, df_sw_nuevos], ignore_index=True)
df_sw_completa.to_excel(switches_path, index=False)
print(f"  ✓ Switches: {len(df_sw)} → {len(df_sw_completa)} registros")

print("\n✓ Enriquecimiento de planillas completado")
print("\n=== RESUMEN ===")
print(f"  - Ubicaciones: {len(df_ubi)} → {len(df_ubi_completa)}")
print(f"  - Gabinetes: {len(df_gab)} → {len(df_gab_completa)}")
print(f"  - UPS: {len(df_ups)} → {len(df_ups_completa)}")
print(f"  - Switches: {len(df_sw)} → {len(df_sw_completa)}")
