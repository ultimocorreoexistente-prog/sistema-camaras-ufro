#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar automáticamente filas vacías de archivos Excel
Sistema de Gestión de Cámaras UFRO - Railway Migration
Fecha: 2025-10-22
"""

import pandas as pd
import os
from datetime import datetime

# Directorios
PLANILLAS_DIR = 'planillas/'
BACKUP_DIR = 'planillas/backup_antes_limpieza/'

# Configuración de archivos y sus campos requeridos
ARCHIVOS_CONFIG = [
    {
        'nombre': 'Equipos_Tecnicos.xlsx',
        'campos_requeridos': ['Nombre'],
        'descripcion': 'Técnicos del equipo'
    },
    {
        'nombre': 'Catalogo_Tipos_Fallas.xlsx',
        'campos_requeridos': ['Nombre'],
        'descripcion': 'Catálogo de tipos de fallas'
    },
    {
        'nombre': 'Gabinetes.xlsx',
        'campos_requeridos': ['Codigo'],
        'descripcion': 'Gabinetes de red'
    },
    {
        'nombre': 'Switches.xlsx',
        'campos_requeridos': ['Codigo'],
        'descripcion': 'Switches de red'
    },
    {
        'nombre': 'Puertos_Switch.xlsx',
        'campos_requeridos': ['ID_Switch'],
        'descripcion': 'Puertos de switches'
    },
    {
        'nombre': 'UPS.xlsx',
        'campos_requeridos': ['Codigo'],
        'descripcion': 'Unidades UPS'
    },
    {
        'nombre': 'NVR_DVR.xlsx',
        'campos_requeridos': ['Codigo'],
        'descripcion': 'Grabadores NVR/DVR'
    },
    {
        'nombre': 'Fuentes_Poder.xlsx',
        'campos_requeridos': ['Codigo'],
        'descripcion': 'Fuentes de poder'
    },
    {
        'nombre': 'Listadecámaras_modificada.xlsx',
        'campos_requeridos': ['Codigo'],
        'descripcion': 'Lista de cámaras'
    },
    {
        'nombre': 'Mantenimientos.xlsx',
        'campos_requeridos': ['Equipo_ID'],
        'descripcion': 'Registro de mantenimientos'
    }
]

def crear_backup():
    """Crea un backup de todos los archivos antes de modificarlos"""
    print("\n📦 CREANDO BACKUP DE ARCHIVOS ORIGINALES...")
    print("=" * 60)
    
    # Crear directorio de backup si no existe
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✓ Directorio de backup creado: {BACKUP_DIR}")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivos_respaldados = 0
    
    for config in ARCHIVOS_CONFIG:
        archivo_original = os.path.join(PLANILLAS_DIR, config['nombre'])
        
        if os.path.exists(archivo_original):
            # Crear nombre de backup con timestamp
            nombre_base = os.path.splitext(config['nombre'])[0]
            extension = os.path.splitext(config['nombre'])[1]
            archivo_backup = os.path.join(BACKUP_DIR, f"{nombre_base}_backup_{timestamp}{extension}")
            
            # Copiar archivo
            import shutil
            shutil.copy2(archivo_original, archivo_backup)
            print(f"✓ Backup creado: {config['nombre']}")
            archivos_respaldados += 1
    
    print(f"\n✓ Total de archivos respaldados: {archivos_respaldados}")
    return True

def limpiar_archivo(config):
    """Limpia un archivo Excel eliminando filas con campos requeridos vacíos"""
    archivo_path = os.path.join(PLANILLAS_DIR, config['nombre'])
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo_path):
        return {
            'archivo': config['nombre'],
            'estado': 'NO ENCONTRADO',
            'filas_originales': 0,
            'filas_eliminadas': 0,
            'filas_finales': 0
        }
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo_path)
        filas_originales = len(df)
        
        # Crear copia para comparar
        df_limpio = df.copy()
        
        # Eliminar filas donde TODOS los campos requeridos están vacíos
        for campo in config['campos_requeridos']:
            if campo in df_limpio.columns:
                # Eliminar filas donde el campo requerido es NaN, None o cadena vacía
                df_limpio = df_limpio[
                    df_limpio[campo].notna() & 
                    (df_limpio[campo].astype(str).str.strip() != '')
                ]
        
        # También eliminar filas completamente vacías (todas las columnas NaN)
        df_limpio = df_limpio.dropna(how='all')
        
        filas_finales = len(df_limpio)
        filas_eliminadas = filas_originales - filas_finales
        
        # Guardar archivo limpio si hubo cambios
        if filas_eliminadas > 0:
            df_limpio.to_excel(archivo_path, index=False, engine='openpyxl')
            estado = '✓ LIMPIADO'
        else:
            estado = '✓ SIN CAMBIOS'
        
        return {
            'archivo': config['nombre'],
            'descripcion': config['descripcion'],
            'estado': estado,
            'filas_originales': filas_originales,
            'filas_eliminadas': filas_eliminadas,
            'filas_finales': filas_finales
        }
        
    except Exception as e:
        return {
            'archivo': config['nombre'],
            'estado': f'❌ ERROR: {str(e)}',
            'filas_originales': 0,
            'filas_eliminadas': 0,
            'filas_finales': 0
        }

def generar_reporte(resultados):
    """Genera un reporte detallado de la limpieza"""
    print("\n" + "=" * 60)
    print("📊 REPORTE DE LIMPIEZA DE ARCHIVOS EXCEL")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    total_filas_eliminadas = 0
    archivos_modificados = 0
    
    for resultado in resultados:
        print(f"\n📄 {resultado['archivo']}")
        print(f"   Descripción: {resultado.get('descripcion', 'N/A')}")
        print(f"   Estado: {resultado['estado']}")
        print(f"   Filas originales: {resultado['filas_originales']}")
        print(f"   Filas eliminadas: {resultado['filas_eliminadas']}")
        print(f"   Filas finales: {resultado['filas_finales']}")
        
        total_filas_eliminadas += resultado['filas_eliminadas']
        if resultado['filas_eliminadas'] > 0:
            archivos_modificados += 1
    
    print("\n" + "=" * 60)
    print("📈 RESUMEN GENERAL")
    print("=" * 60)
    print(f"Total de archivos procesados: {len(resultados)}")
    print(f"Archivos modificados: {archivos_modificados}")
    print(f"Total de filas eliminadas: {total_filas_eliminadas}")
    print("=" * 60)
    
    # Guardar reporte en archivo
    reporte_path = 'docs/REPORTE_LIMPIEZA_EXCEL.txt'
    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("REPORTE DE LIMPIEZA DE ARCHIVOS EXCEL\n")
        f.write("Sistema de Gestión de Cámaras UFRO\n")
        f.write("=" * 60 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for resultado in resultados:
            f.write(f"\nArchivo: {resultado['archivo']}\n")
            f.write(f"Descripción: {resultado.get('descripcion', 'N/A')}\n")
            f.write(f"Estado: {resultado['estado']}\n")
            f.write(f"Filas originales: {resultado['filas_originales']}\n")
            f.write(f"Filas eliminadas: {resultado['filas_eliminadas']}\n")
            f.write(f"Filas finales: {resultado['filas_finales']}\n")
            f.write("-" * 60 + "\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("RESUMEN GENERAL\n")
        f.write("=" * 60 + "\n")
        f.write(f"Total de archivos procesados: {len(resultados)}\n")
        f.write(f"Archivos modificados: {archivos_modificados}\n")
        f.write(f"Total de filas eliminadas: {total_filas_eliminadas}\n")
        f.write("=" * 60 + "\n")
    
    print(f"\n✓ Reporte guardado en: {reporte_path}")

def main():
    """Función principal"""
    print("\n" + "*" * 60)
    print("🧹 LIMPIEZA AUTOMÁTICA DE ARCHIVOS EXCEL")
    print("Sistema de Gestión de Cámaras UFRO")
    print("*" * 60)
    
    # Paso 1: Crear backup
    if not crear_backup():
        print("\n❌ ERROR: No se pudo crear el backup. Abortando operación.")
        return
    
    # Paso 2: Limpiar cada archivo
    print("\n🧹 LIMPIANDO ARCHIVOS...")
    print("=" * 60)
    
    resultados = []
    for config in ARCHIVOS_CONFIG:
        print(f"\nProcesando: {config['nombre']}...", end=" ")
        resultado = limpiar_archivo(config)
        resultados.append(resultado)
        print(resultado['estado'])
    
    # Paso 3: Generar reporte
    generar_reporte(resultados)
    
    print("\n" + "*" * 60)
    print("✅ PROCESO COMPLETADO")
    print("*" * 60)
    print("\n📌 PRÓXIMOS PASOS:")
    print("1. Revisar el reporte en: docs/REPORTE_LIMPIEZA_EXCEL.txt")
    print("2. Verificar los archivos limpios en: planillas/")
    print("3. Si todo está correcto, ejecutar migrate_data.py para migrar a Railway")
    print("4. Si necesitas restaurar, los backups están en: planillas/backup_antes_limpieza/")
    print()

if __name__ == '__main__':
    main()
