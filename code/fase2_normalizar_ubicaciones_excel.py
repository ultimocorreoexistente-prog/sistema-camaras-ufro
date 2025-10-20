#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FASE 2: Normalización de Ubicaciones en Planillas Excel
Tarea 11: Agregar columna ID Ubicación a todas las planillas
"""

import pandas as pd
import os

print("="*80)
print("FASE 2 - TAREA 11: NORMALIZAR UBICACIONES EN PLANILLAS EXCEL")
print("="*80)

# Leer planilla maestra de ubicaciones
print("\n[11.1] Cargando planilla maestra Ubicaciones.xlsx...")
ubicaciones_df = pd.read_excel('user_input_files/planillas-web/Ubicaciones.xlsx')
print(f"✓ Ubicaciones cargadas: {len(ubicaciones_df)} registros")
print(f"\nColumnas en Ubicaciones.xlsx:")
for col in ubicaciones_df.columns:
    print(f"  - {col}")

# Mostrar las ubicaciones
print(f"\nUbicaciones disponibles:")
for idx, row in ubicaciones_df.iterrows():
    print(f"  ID {row.iloc[0]}: {row.get('Campus', 'N/A')} - {row.get('Edificio', 'N/A')}")

# ==============================================================================
# Procesar cada planilla
# ==============================================================================

planillas_a_procesar = [
    ('Listadecámaras_modificada.xlsx', 'Sheet1'),
    ('Gabinetes.xlsx', 'Sheet1'),
    ('Switches.xlsx', 'Sheet1'),
    ('UPS.xlsx', 'UPS'),
    ('NVR_DVR.xlsx', 'NVR_DVR'),
    ('Fuentes_Poder.xlsx', 'Fuentes_Poder')
]

print(f"\n[11.2] Procesando {len(planillas_a_procesar)} planillas...\n")

for archivo, hoja in planillas_a_procesar:
    ruta = f'user_input_files/planillas-web/{archivo}'
    
    if not os.path.exists(ruta):
        print(f"⚠ SKIP: {archivo} no existe")
        continue
    
    print(f"Procesando: {archivo}")
    
    try:
        df = pd.read_excel(ruta, sheet_name=hoja)
        print(f"  Filas originales: {len(df)}")
        
        # Verificar si ya tiene columna ID Ubicación
        if 'ID Ubicación' not in df.columns:
            # Agregar columna vacía al principio (después de la primera columna ID)
            columnas = df.columns.tolist()
            # Insertar después de la primera columna si existe un ID
            if len(columnas) > 0:
                df.insert(1, 'ID Ubicación', None)
            else:
                df['ID Ubicación'] = None
            
            print(f"  ✓ Columna 'ID Ubicación' agregada")
        else:
            print(f"  • Ya tiene columna 'ID Ubicación'")
        
        # Intentar mapear ubicaciones automáticamente basado en Campus
        if 'Campus' in df.columns:
            for idx, row in df.iterrows():
                campus = row.get('Campus')
                if pd.notna(campus):
                    # Buscar en ubicaciones_df
                    ubicacion_match = ubicaciones_df[ubicaciones_df.iloc[:, 1].str.contains(str(campus), case=False, na=False)]
                    if len(ubicacion_match) > 0:
                        id_ubic = ubicacion_match.iloc[0, 0]  # Primera columna es el ID
                        df.at[idx, 'ID Ubicación'] = id_ubic
            
            ids_asignados = df['ID Ubicación'].notna().sum()
            print(f"  ✓ IDs de ubicación auto-asignados: {ids_asignados}/{len(df)}")
        
        # Guardar archivo actualizado
        ruta_salida = f'user_input_files/planillas-web/{archivo}'
        df.to_excel(ruta_salida, sheet_name=hoja, index=False)
        print(f"  ✓ Guardado: {archivo}\n")
        
    except Exception as e:
        print(f"  ✗ ERROR: {e}\n")

print("="*80)
print("✓ TAREA 11 COMPLETADA: Columna 'ID Ubicación' agregada a todas las planillas")
print("="*80)
print("\nNOTA: Los IDs se asignaron automáticamente donde fue posible.")
print("Revisa y completa manualmente los IDs faltantes basándote en Ubicaciones.xlsx")
