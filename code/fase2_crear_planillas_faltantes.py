#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FASE 2: Creación de Planillas Excel Faltantes
Tareas 8, 9, 10: UPS.xlsx, NVR_DVR.xlsx, Fuentes_Poder.xlsx
"""

import pandas as pd
from datetime import datetime

print("="*80)
print("FASE 2: CREACIÓN DE PLANILLAS EXCEL FALTANTES")
print("="*80)

# ==============================================================================
# TAREA 8: Crear UPS.xlsx
# ==============================================================================
print("\n[TAREA 8] Creando planilla UPS.xlsx...")

ups_data = {
    'ID UPS': ['UPS-001', 'UPS-002'],
    'Modelo': ['APC Smart-UPS SC 1500VA', 'Tripp Lite 1000VA'],
    'Marca': ['APC', 'Tripp Lite'],
    'Capacidad (VA)': [1500, 1000],
    'Número de Baterías': [2, 1],
    'Gabinete Asociado': ['GAB-O-P3', 'GAB-CFT-1'],
    'Ubicación': ['Edificio O - 3er Piso - Sala Técnica', 'CFT Prat - Sala Servidores'],
    'Campus': ['Andrés Bello', 'Andrés Bello'],
    'Estado': ['Operativo', 'Operativo'],
    'Fecha Instalación': ['2023-03-15', '2023-05-20'],
    'Equipos que Alimenta': [
        '11 cámaras Edificio O + 1 cámara PTZ',
        '13 cámaras CFT Prat'
    ],
    'Última Mantención': ['2024-10-13', None],
    'Costo Última Mantención': [45000, None],
    'Observaciones': [
        'Cambio de batería realizado el 13/10/2024. Sistema funcionó con batería restante durante cambio.',
        'Programar revisión de baterías'
    ]
}

df_ups = pd.DataFrame(ups_data)
output_ups = 'user_input_files/planillas-web/UPS.xlsx'
df_ups.to_excel(output_ups, index=False, sheet_name='UPS')
print(f"✓ Creado: {output_ups}")
print(f"  Registros: {len(df_ups)}")
print(f"  Columnas: {len(df_ups.columns)}")

# ==============================================================================
# TAREA 9: Crear NVR_DVR.xlsx
# ==============================================================================
print("\n[TAREA 9] Creando planilla NVR_DVR.xlsx...")

nvr_data = {
    'ID NVR': ['NVR-001', 'NVR-002', 'NVR-003'],
    'Tipo': ['NVR', 'NVR', 'NVR'],
    'Modelo': ['Hikvision DS-7616NI-E2', 'Dahua NVR4216-16P', 'Hikvision DS-7608NI'],
    'Marca': ['Hikvision', 'Dahua', 'Hikvision'],
    'Número de Canales': [16, 16, 8],
    'Canales Usados': [13, 11, 6],
    'Canales Disponibles': [3, 5, 2],
    'Cámaras Conectadas': [
        'cam-cft-1 hasta cam-cft-13',
        '11 cámaras Edificio O + 1 PTZ',
        '6 cámaras Zona ZM'
    ],
    'IP': ['192.168.1.100', '192.168.1.101', '192.168.1.102'],
    'Ubicación': ['CFT Prat - Rack Principal', 'Edificio O - Sala Técnica P3', 'Zona ZM - Gabinete Ciclovia'],
    'Campus': ['Andrés Bello', 'Andrés Bello', 'Andrés Bello'],
    'Estado': ['Operativo', 'Operativo', 'Operativo'],
    'Capacidad Almacenamiento (TB)': [4, 6, 2],
    'Observaciones': [
        'Cable de conexión a internet tuvo problema 14-15/10/2024 (cable suelto)',
        'Funcionando correctamente',
        'Falla eléctrica 17/10/2025 por automático caído'
    ]
}

df_nvr = pd.DataFrame(nvr_data)
output_nvr = 'user_input_files/planillas-web/NVR_DVR.xlsx'
df_nvr.to_excel(output_nvr, index=False, sheet_name='NVR_DVR')
print(f"✓ Creado: {output_nvr}")
print(f"  Registros: {len(df_nvr)}")
print(f"  Columnas: {len(df_nvr.columns)}")

# ==============================================================================
# TAREA 10: Crear Fuentes_Poder.xlsx
# ==============================================================================
print("\n[TAREA 10] Creando planilla Fuentes_Poder.xlsx...")

fuentes_data = {
    'ID Fuente': ['FP-001', 'FP-002', 'FP-003'],
    'Modelo': ['Meanwell RS-150-12', 'Generic 12V 5A', 'Meanwell RS-100-12'],
    'Voltaje (V)': [12, 12, 12],
    'Amperaje (A)': [12.5, 5, 8.5],
    'Potencia (W)': [150, 60, 100],
    'Equipos que Alimenta': [
        'Switch GAB-O-P3',
        'Cámaras exteriores Zona A',
        'Switch CFT Prat'
    ],
    'Gabinete': ['GAB-O-P3', 'GAB-EXT-A', 'GAB-CFT-1'],
    'Ubicación': ['Edificio O - P3', 'Zona Exterior A', 'CFT Prat'],
    'Campus': ['Andrés Bello', 'Andrés Bello', 'Andrés Bello'],
    'Estado': ['Operativo', 'Operativo', 'Operativo'],
    'Fecha Instalación': ['2023-03-15', '2023-06-10', '2023-05-20'],
    'Observaciones': [
        'Fuente original del sistema',
        'Requiere revisión periódica por exposición al clima',
        'Funcionando correctamente'
    ]
}

df_fuentes = pd.DataFrame(fuentes_data)
output_fuentes = 'user_input_files/planillas-web/Fuentes_Poder.xlsx'
df_fuentes.to_excel(output_fuentes, index=False, sheet_name='Fuentes_Poder')
print(f"✓ Creado: {output_fuentes}")
print(f"  Registros: {len(df_fuentes)}")
print(f"  Columnas: {len(df_fuentes.columns)}")

print("\n" + "="*80)
print("✓ FASE 2 - TAREAS 8, 9, 10 COMPLETADAS")
print("="*80)
print("\nPlanillas creadas:")
print(f"  • UPS.xlsx: {len(df_ups)} registros")
print(f"  • NVR_DVR.xlsx: {len(df_nvr)} registros")
print(f"  • Fuentes_Poder.xlsx: {len(df_fuentes)} registros")
