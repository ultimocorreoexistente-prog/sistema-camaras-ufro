import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

planillas_dir = 'user_input_files/planillas-web'

print("=== ENRIQUECIMIENTO PARTE 2: NVR/DVR, Fuentes, Mantenimientos ===")
print()

# ============================================================================
# 1. NVR/DVR - Añadir más equipos
# ============================================================================
print("📹 Enriqueciendo NVR_DVR.xlsx...")

nvr_path = os.path.join(planillas_dir, 'NVR_DVR.xlsx')
df_nvr = pd.read_excel(nvr_path)

nuevos_nvr = [
    {'ID NVR/DVR': 'NVR-004', 'ID Ubicación': 'UBI-006', 'Tipo': 'NVR', 
     'Modelo': 'DS-7608NI-K2', 'Marca': 'Hikvision', 'Capacidad Canales': 8, 
     'Canales Usados': 5, 'Capacidad Almacenamiento (TB)': 2, 'Disco Duro Instalado': '2TB WD Purple', 
     'Gabinete Asociado': 'GAB-004', 'IP': '192.168.5.20', 'Estado': 'Activo', 
     'Fecha Instalación': '2024-08-05', 'Último Mantenimiento': None, 
     'Observaciones': 'NVR campus Pucón'},
    
    {'ID NVR/DVR': 'NVR-005', 'ID Ubicación': 'UBI-007', 'Tipo': 'NVR', 
     'Modelo': 'DS-7616NI-K2', 'Marca': 'Hikvision', 'Capacidad Canales': 16, 
     'Canales Usados': 13, 'Capacidad Almacenamiento (TB)': 4, 'Disco Duro Instalado': '2x 2TB WD Purple (RAID)', 
     'Gabinete Asociado': 'GAB-005', 'IP': '192.168.6.10', 'Estado': 'Activo', 
     'Fecha Instalación': '2024-05-12', 'Último Mantenimiento': '2025-09-18', 
     'Observaciones': 'NVR principal CFT Prat - RAID 1'},
    
    {'ID NVR/DVR': 'DVR-001', 'ID Ubicación': 'UBI-004', 'Tipo': 'DVR', 
     'Modelo': 'XVR5108HS-4KL', 'Marca': 'Dahua', 'Capacidad Canales': 8, 
     'Canales Usados': 8, 'Capacidad Almacenamiento (TB)': 1, 'Disco Duro Instalado': '1TB Seagate', 
     'Gabinete Asociado': 'GAB-006', 'IP': '192.168.1.35', 'Estado': 'Activo', 
     'Fecha Instalación': '2024-06-20', 'Último Mantenimiento': '2025-10-10', 
     'Observaciones': 'Sistema híbrido - AHD + IP'},
]

df_nvr_nuevos = pd.DataFrame(nuevos_nvr)
df_nvr_completa = pd.concat([df_nvr, df_nvr_nuevos], ignore_index=True)
df_nvr_completa.to_excel(nvr_path, index=False)
print(f"  ✓ NVR/DVR: {len(df_nvr)} → {len(df_nvr_completa)} registros")

# ============================================================================
# 2. FUENTES DE PODER - Añadir más
# ============================================================================
print("🔋 Enriqueciendo Fuentes_Poder.xlsx...")

fuentes_path = os.path.join(planillas_dir, 'Fuentes_Poder.xlsx')
df_fuentes = pd.read_excel(fuentes_path)

nuevas_fuentes = [
    {'ID Fuente': 'FP-004', 'ID Ubicación': 'UBI-006', 'Tipo': 'Fuente 12V 5A', 
     'Modelo': 'PS-1205', 'Marca': 'PowerTech', 'Voltaje Salida (V)': 12, 
     'Amperaje (A)': 5, 'Potencia (W)': 60, 'Gabinete Asociado': 'GAB-004', 
     'Equipos que Alimenta': '3 cámaras bullet', 'Estado': 'Activo', 
     'Fecha Instalación': '2024-08-05', 'Observaciones': 'Fuente externa gabinete Pucón'},
    
    {'ID Fuente': 'FP-005', 'ID Ubicación': 'UBI-007', 'Tipo': 'Fuente 12V 10A', 
     'Modelo': 'PS-1210-R', 'Marca': 'Altronix', 'Voltaje Salida (V)': 12, 
     'Amperaje (A)': 10, 'Potencia (W)': 120, 'Gabinete Asociado': 'GAB-005', 
     'Equipos que Alimenta': 'Respaldo para cámaras no-PoE', 'Estado': 'Activo', 
     'Fecha Instalación': '2024-05-12', 'Observaciones': 'Fuente redundante CFT Prat'},
    
    {'ID Fuente': 'FP-006', 'ID Ubicación': 'UBI-004', 'Tipo': 'Fuente 12V 3A', 
     'Modelo': 'PS-1203', 'Marca': 'Generic', 'Voltaje Salida (V)': 12, 
     'Amperaje (A)': 3, 'Potencia (W)': 36, 'Gabinete Asociado': 'GAB-006', 
     'Equipos que Alimenta': '2 cámaras AHD', 'Estado': 'Activo', 
     'Fecha Instalación': '2024-06-20', 'Observaciones': 'Alimentación cámaras analógicas'},
]

df_fuentes_nuevas = pd.DataFrame(nuevas_fuentes)
df_fuentes_completa = pd.concat([df_fuentes, df_fuentes_nuevas], ignore_index=True)
df_fuentes_completa.to_excel(fuentes_path, index=False)
print(f"  ✓ Fuentes de Poder: {len(df_fuentes)} → {len(df_fuentes_completa)} registros")

# ============================================================================
# 3. MANTENIMIENTOS - Añadir más registros
# ============================================================================
print("🔧 Enriqueciendo Mantenimientos.xlsx...")

mant_path = os.path.join(planillas_dir, 'Mantenimientos.xlsx')
df_mant = pd.read_excel(mant_path)

nuevos_mantenimientos = [
    {'ID Mantenimiento': 'MANT-002', 'Fecha': '2024-09-15', 'Tipo': 'Preventivo', 
     'Componente Tipo': 'Cámara', 'Componente ID': 'Edificio-L-Pasillo-Dome-01', 
     'Descripción Trabajo': 'Limpieza preventiva de cámaras domo - remoción de polvo y verificación mecánica', 
     'Materiales Utilizados': 'Paño microfibra, alcohol isopropílico', 
     'Técnico Responsable': 'Personal interno', 'Duración (horas)': 3.0, 
     'Costo Total': 0, 'Resultado': 'Exitoso', 
     'Próximo Mantenimiento': '2025-03-15', 'Prioridad': 'Media', 
     'Observaciones': 'Mantenimiento trimestral programado'},
    
    {'ID Mantenimiento': 'MANT-003', 'Fecha': '2024-11-20', 'Tipo': 'Correctivo', 
     'Componente Tipo': 'Switch', 'Componente ID': 'SW-005', 
     'Descripción Trabajo': 'Reemplazo de ventilador defectuoso en switch principal CFT Prat', 
     'Materiales Utilizados': 'Ventilador 40mm 12V', 
     'Técnico Responsable': 'Técnico externo', 'Duración (horas)': 1.5, 
     'Costo Total': 15000, 'Resultado': 'Exitoso', 
     'Próximo Mantenimiento': None, 'Prioridad': 'Alta', 
     'Observaciones': 'Switch presentaba sobrecalentamiento'},
    
    {'ID Mantenimiento': 'MANT-004', 'Fecha': '2025-01-10', 'Tipo': 'Preventivo', 
     'Componente Tipo': 'NVR', 'Componente ID': 'NVR-005', 
     'Descripción Trabajo': 'Verificación de discos RAID y limpieza de sistema de almacenamiento', 
     'Materiales Utilizados': 'Aire comprimido, software diagnóstico', 
     'Técnico Responsable': 'Personal interno', 'Duración (horas)': 2.0, 
     'Costo Total': 0, 'Resultado': 'Exitoso', 
     'Próximo Mantenimiento': '2025-07-10', 'Prioridad': 'Alta', 
     'Observaciones': 'RAID 1 operando correctamente'},
    
    {'ID Mantenimiento': 'MANT-005', 'Fecha': '2025-02-28', 'Tipo': 'Correctivo', 
     'Componente Tipo': 'Fuente Poder', 'Componente ID': 'FP-003', 
     'Descripción Trabajo': 'Reemplazo de fuente de poder defectuosa', 
     'Materiales Utilizados': 'Fuente 12V 5A nueva', 
     'Técnico Responsable': 'Personal interno', 'Duración (horas)': 0.5, 
     'Costo Total': 12000, 'Resultado': 'Exitoso', 
     'Próximo Mantenimiento': None, 'Prioridad': 'Media', 
     'Observaciones': 'Fuente presentó falla total - reemplazada'},
    
    {'ID Mantenimiento': 'MANT-006', 'Fecha': '2025-05-15', 'Tipo': 'Preventivo', 
     'Componente Tipo': 'UPS', 'Componente ID': 'UPS-003', 
     'Descripción Trabajo': 'Cambio preventivo de baterías UPS CFT Prat', 
     'Materiales Utilizados': '2x Batería RBC7 - 12V 17Ah', 
     'Técnico Responsable': 'Técnico especializado UPS', 'Duración (horas)': 3.0, 
     'Costo Total': 85000, 'Resultado': 'Exitoso', 
     'Próximo Mantenimiento': '2026-05-15', 'Prioridad': 'Alta', 
     'Observaciones': 'Baterías con 1 año de uso - cambio preventivo'},
]

df_mant_nuevos = pd.DataFrame(nuevos_mantenimientos)
df_mant_completa = pd.concat([df_mant, df_mant_nuevos], ignore_index=True)
df_mant_completa.to_excel(mant_path, index=False)
print(f"  ✓ Mantenimientos: {len(df_mant)} → {len(df_mant_completa)} registros")

print("\n✓ Enriquecimiento parte 2 completado")
print("\n=== RESUMEN ===")
print(f"  - NVR/DVR: {len(df_nvr)} → {len(df_nvr_completa)}")
print(f"  - Fuentes de Poder: {len(df_fuentes)} → {len(df_fuentes_completa)}")
print(f"  - Mantenimientos: {len(df_mant)} → {len(df_mant_completa)}")
