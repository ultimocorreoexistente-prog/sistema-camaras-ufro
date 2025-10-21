#!/usr/bin/env python3
"""Script para analizar archivos Excel y reportar filas con datos incompletos"""

import pandas as pd
import os
from datetime import datetime

def safe_str(value):
    """Convierte valor a string manejando NaN"""
    if pd.isna(value):
        return None
    return str(value).strip() if str(value).strip() else None

def safe_int(value):
    """Convierte valor a int manejando NaN"""
    try:
        if pd.isna(value):
            return None
        return int(value)
    except:
        return None

def analizar_archivos():
    """Analiza todos los archivos Excel y genera reporte de problemas"""
    
    base_path = 'planillas/'
    reporte = []
    reporte.append("="*80)
    reporte.append("REPORTE DE DATOS INCOMPLETOS EN ARCHIVOS EXCEL")
    reporte.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    reporte.append("="*80)
    reporte.append("")
    
    total_problemas = 0
    
    # 1. EQUIPOS TÉCNICOS
    reporte.append("\n" + "="*80)
    reporte.append("1. EQUIPOS TÉCNICOS (Equipos_Tecnicos.xlsx)")
    reporte.append("   Campo requerido: Nombre")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Equipos_Tecnicos.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            nombre = safe_str(row.get('Nombre'))
            if not nombre:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Nombre vacío")
                reporte.append(f"      - Apellido: {safe_str(row.get('Apellido'))}")
                reporte.append(f"      - Especialidad: {safe_str(row.get('Especialidad'))}")
                reporte.append(f"      - Email: {safe_str(row.get('Email'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 2. CATÁLOGO TIPOS DE FALLAS
    reporte.append("\n" + "="*80)
    reporte.append("2. CATÁLOGO TIPOS DE FALLAS (Catalogo_Tipos_Fallas.xlsx)")
    reporte.append("   Campo requerido: Nombre")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Catalogo_Tipos_Fallas.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            nombre = safe_str(row.get('Nombre'))
            if not nombre:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Nombre vacío")
                reporte.append(f"      - Categoría: {safe_str(row.get('Categoria'))}")
                reporte.append(f"      - Gravedad: {safe_str(row.get('Gravedad'))}")
                reporte.append(f"      - Descripción: {safe_str(row.get('Descripcion'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 3. GABINETES
    reporte.append("\n" + "="*80)
    reporte.append("3. GABINETES (Gabinetes.xlsx)")
    reporte.append("   Campo requerido: Codigo")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Gabinetes.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            if not codigo:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Código vacío")
                reporte.append(f"      - Nombre: {safe_str(row.get('Nombre'))}")
                reporte.append(f"      - Ubicación ID: {safe_int(row.get('ID_Ubicacion'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 4. SWITCHES
    reporte.append("\n" + "="*80)
    reporte.append("4. SWITCHES (Switches.xlsx)")
    reporte.append("   Campo requerido: Codigo")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Switches.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            if not codigo:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Código vacío")
                reporte.append(f"      - Nombre: {safe_str(row.get('Nombre'))}")
                reporte.append(f"      - IP: {safe_str(row.get('IP'))}")
                reporte.append(f"      - Gabinete ID: {safe_int(row.get('ID_Gabinete'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 5. PUERTOS SWITCH
    reporte.append("\n" + "="*80)
    reporte.append("5. PUERTOS SWITCH (Puertos_Switch.xlsx)")
    reporte.append("   Campo requerido: ID_Switch")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Puertos_Switch.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            switch_id = safe_int(row.get('ID_Switch'))
            if not switch_id:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: ID_Switch vacío")
                reporte.append(f"      - Número Puerto: {safe_int(row.get('Numero_Puerto'))}")
                reporte.append(f"      - Cámara ID: {safe_int(row.get('ID_Camara'))}")
                reporte.append(f"      - Estado: {safe_str(row.get('Estado'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 6. UPS
    reporte.append("\n" + "="*80)
    reporte.append("6. UPS (UPS.xlsx)")
    reporte.append("   Campo requerido: Codigo")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}UPS.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            if not codigo:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Código vacío")
                reporte.append(f"      - Modelo: {safe_str(row.get('Modelo'))}")
                reporte.append(f"      - Marca: {safe_str(row.get('Marca'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 7. NVR/DVR
    reporte.append("\n" + "="*80)
    reporte.append("7. NVR/DVR (NVR_DVR.xlsx)")
    reporte.append("   Campo requerido: Codigo")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}NVR_DVR.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            if not codigo:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Código vacío")
                reporte.append(f"      - Tipo: {safe_str(row.get('Tipo'))}")
                reporte.append(f"      - Modelo: {safe_str(row.get('Modelo'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 8. FUENTES DE PODER
    reporte.append("\n" + "="*80)
    reporte.append("8. FUENTES DE PODER (Fuentes_Poder.xlsx)")
    reporte.append("   Campo requerido: Codigo")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Fuentes_Poder.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            if not codigo:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Código vacío")
                reporte.append(f"      - Modelo: {safe_str(row.get('Modelo'))}")
                reporte.append(f"      - Voltaje: {safe_str(row.get('Voltaje'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 9. CÁMARAS
    reporte.append("\n" + "="*80)
    reporte.append("9. CÁMARAS (Listadecámaras_modificada.xlsx)")
    reporte.append("   Campo requerido: Codigo")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Listadecámaras_modificada.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            if not codigo:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Código vacío")
                reporte.append(f"      - Nombre: {safe_str(row.get('Nombre'))}")
                reporte.append(f"      - IP: {safe_str(row.get('IP'))}")
                reporte.append(f"      - Modelo: {safe_str(row.get('Modelo'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # 10. MANTENIMIENTOS
    reporte.append("\n" + "="*80)
    reporte.append("10. MANTENIMIENTOS (Mantenimientos.xlsx)")
    reporte.append("    Campo requerido: Equipo_ID")
    reporte.append("="*80)
    try:
        df = pd.read_excel(f'{base_path}Mantenimientos.xlsx')
        problemas = 0
        for idx, row in df.iterrows():
            equipo_id = safe_int(row.get('Equipo_ID'))
            if not equipo_id:
                problemas += 1
                reporte.append(f"   ⚠ Fila {idx + 2}: Equipo_ID vacío")
                reporte.append(f"      - Tipo: {safe_str(row.get('Tipo'))}")
                reporte.append(f"      - Equipo Tipo: {safe_str(row.get('Equipo_Tipo'))}")
                reporte.append(f"      - Descripción: {safe_str(row.get('Descripcion'))}")
                reporte.append("")
        reporte.append(f"\n   Total problemas: {problemas}")
        total_problemas += problemas
    except Exception as e:
        reporte.append(f"   ❌ Error leyendo archivo: {e}")
    
    # RESUMEN FINAL
    reporte.append("\n\n" + "="*80)
    reporte.append("RESUMEN")
    reporte.append("="*80)
    reporte.append(f"Total de filas con datos incompletos: {total_problemas}")
    reporte.append("")
    reporte.append("ACCIÓN REQUERIDA:")
    reporte.append("1. Corregir los archivos Excel agregando los datos faltantes")
    reporte.append("2. O eliminar las filas que no son válidas")
    reporte.append("3. Guardar los archivos corregidos")
    reporte.append("4. Ejecutar nuevamente la migración")
    reporte.append("="*80)
    
    return "\n".join(reporte)

if __name__ == '__main__':
    os.chdir('/workspace/sistema-camaras-flask')
    reporte_texto = analizar_archivos()
    
    # Guardar en archivo
    with open('/workspace/docs/REPORTE_DATOS_INCOMPLETOS.txt', 'w', encoding='utf-8') as f:
        f.write(reporte_texto)
    
    # Mostrar en consola
    print(reporte_texto)
    print("\n✅ Reporte guardado en: docs/REPORTE_DATOS_INCOMPLETOS.txt")
