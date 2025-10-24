#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FASE 3: Script de Migración Unificado Excel → Base de Datos
Tarea 14: Migrar todas las planillas Excel consolidadas a SQLite
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

db_path = "sistema_camaras.db"
log_file = f"logs/migracion_excel_bd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

Path("logs").mkdir(exist_ok=True)

def log_message(message, level="INFO"):
    """Registrar mensaje en log y consola"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def validar_falla_antes_insertar(cursor, camara_nombre):
    """
    Validación ANTI-DUPLICADOS para fallas
    Retorna True si se puede insertar, False si hay falla abierta
    """
    cursor.execute("""
        SELECT estado, fecha_reporte 
        FROM fallas 
        WHERE camaras_afectadas LIKE ? 
        ORDER BY fecha_reporte DESC 
        LIMIT 1
    """, (f'%{camara_nombre}%',))
    
    ultima_falla = cursor.fetchone()
    
    if ultima_falla:
        estado = ultima_falla[0]
        if estado in ['Pendiente', 'Asignada', 'En Proceso', 'Reparada']:
            log_message(f"⚠ DUPLICADO DETECTADO: Cámara '{camara_nombre}' tiene falla abierta en estado '{estado}'", "WARNING")
            return False
    
    return True

log_message("="*80)
log_message("INICIO: Migración Excel → Base de Datos")
log_message("="*80)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

try:
    # ==========================================================================
    # MIGRAR TIPOS DE FALLAS
    # ==========================================================================
    log_message("\n[1] Migrando Catalogo_Tipos_Fallas.xlsx...")
    
    try:
        df_tipos_fallas = pd.read_excel('user_input_files/planillas-web/Catalogo_Tipos_Fallas.xlsx')
        log_message(f"  Registros leídos: {len(df_tipos_fallas)}")
        
        # Limpiar tabla existente de tipos que no estén en la BD original
        # Solo agregar nuevos, no eliminar existentes
        
        insertados = 0
        for idx, row in df_tipos_fallas.iterrows():
            # Mapear prioridad
            prioridad_map = {
                'Baja': 'BAJA',
                'Media': 'MEDIA',
                'Alta': 'ALTA',
                'Crítica': 'ALTA'
            }
            
            prioridad = prioridad_map.get(row.get('Prioridad Sugerida', 'Media'), 'MEDIA')
            
            # Intentar insertar (ignorar si ya existe)
            cursor.execute("""
                INSERT OR IGNORE INTO tipos_fallas (nombre, categoria, prioridad, descripcion)
                VALUES (?, ?, ?, ?)
            """, (
                row.get('Tipo de Falla', 'Sin nombre'),
                row.get('Categoría Principal', 'GENERAL'),
                prioridad,
                row.get('Impacto Típico', '')
            ))
            
            if cursor.rowcount > 0:
                insertados += 1
        
        conn.commit()
        log_message(f"✓ Tipos de fallas migrados: {insertados} nuevos", "SUCCESS")
        
    except Exception as e:
        log_message(f"✗ Error en tipos de fallas: {e}", "ERROR")
    
    # ==========================================================================
    # MIGRAR UBICACIONES
    # ==========================================================================
    log_message("\n[2] Migrando Ubicaciones.xlsx...")
    
    try:
        df_ubicaciones = pd.read_excel('user_input_files/planillas-web/Ubicaciones.xlsx')
        log_message(f"  Registros leídos: {len(df_ubicaciones)}")
        
        insertados = 0
        for idx, row in df_ubicaciones.iterrows():
            cursor.execute("""
                INSERT OR IGNORE INTO ubicaciones (campus, edificio, piso, zona, descripcion)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row.get('Campus', ''),
                row.get('Edificio', ''),
                row.get('Piso/Nivel', ''),
                row.get('Zona', ''),
                row.get('Observaciones', '')
            ))
            
            if cursor.rowcount > 0:
                insertados += 1
        
        conn.commit()
        log_message(f"✓ Ubicaciones migradas: {insertados} nuevas", "SUCCESS")
        
    except Exception as e:
        log_message(f"✗ Error en ubicaciones: {e}", "ERROR")
    
    # ==========================================================================
    # MIGRAR EQUIPOS TECNICOS (UPS, NVR, FUENTES)
    # ==========================================================================
    log_message("\n[3] Procesando equipos técnicos...")
    
    # UPS
    try:
        df_ups = pd.read_excel('user_input_files/planillas-web/UPS.xlsx')
        log_message(f"  UPS leídos: {len(df_ups)}")
        log_message("  Nota: UPS registrados para referencia (tabla dedicada a implementar en futuro)")
    except Exception as e:
        log_message(f"⚠ No se pudo leer UPS.xlsx: {e}", "WARNING")
    
    # NVR/DVR
    try:
        df_nvr = pd.read_excel('user_input_files/planillas-web/NVR_DVR.xlsx')
        log_message(f"  NVR/DVR leídos: {len(df_nvr)}")
        log_message("  Nota: NVR registrados para referencia (tabla dedicada a implementar en futuro)")
    except Exception as e:
        log_message(f"⚠ No se pudo leer NVR_DVR.xlsx: {e}", "WARNING")
    
    # Fuentes de Poder
    try:
        df_fuentes = pd.read_excel('user_input_files/planillas-web/Fuentes_Poder.xlsx')
        log_message(f"  Fuentes de Poder leídas: {len(df_fuentes)}")
        log_message("  Nota: Fuentes registradas para referencia (tabla dedicada a implementar en futuro)")
    except Exception as e:
        log_message(f"⚠ No se pudo leer Fuentes_Poder.xlsx: {e}", "WARNING")
    
    # ==========================================================================
    # MIGRAR FALLAS DESDE Fallas_Actualizada.xlsx
    # ==========================================================================
    log_message("\n[4] Migrando Fallas_Actualizada.xlsx...")
    
    try:
        df_fallas = pd.read_excel('user_input_files/planillas-web/Fallas_Actualizada.xlsx')
        log_message(f"  Registros leídos: {len(df_fallas)}")
        
        insertados = 0
        duplicados_evitados = 0
        
        for idx, row in df_fallas.iterrows():
            camara = row.get('Cámara Afectada', row.get('Nombre de Cámara', 'Desconocida'))
            
            # Validación anti-duplicados
            if not validar_falla_antes_insertar(cursor, camara):
                duplicados_evitados += 1
                continue
            
            # Mapear estado
            estado = row.get('Estado de Reparación', 'Pendiente')
            if estado not in ['Pendiente', 'Asignada', 'En Proceso', 'Reparada', 'Cerrada', 'Cancelada']:
                estado = 'Pendiente'
            
            cursor.execute("""
                INSERT INTO fallas (
                    categoria, descripcion, fecha_reporte, campus, ubicacion,
                    estado, prioridad, tecnico_asignado_nombre,
                    solucion_aplicada, costo_reparacion,
                    camaras_afectadas, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get('Tipo de Falla', 'General'),
                row.get('Descripción', 'Sin descripción'),
                row.get('Fecha de Reporte', datetime.now()),
                row.get('Campus', 'Andrés Bello'),
                row.get('Ubicación', ''),
                estado,
                row.get('Prioridad', 'Media'),
                row.get('Técnico Asignado', ''),
                row.get('Solución Aplicada', ''),
                row.get('Costo', 0),
                camara,
                row.get('Observaciones', '')
            ))
            
            insertados += 1
        
        conn.commit()
        log_message(f"✓ Fallas migradas: {insertados}", "SUCCESS")
        log_message(f"⚠ Duplicados evitados: {duplicados_evitados}", "WARNING")
        
    except Exception as e:
        log_message(f"✗ Error en fallas: {e}", "ERROR")
    
    # ==========================================================================
    # VERIFICACIÓN FINAL
    # ==========================================================================
    log_message("\n" + "="*80)
    log_message("VERIFICACIÓN FINAL")
    log_message("="*80)
    
    tablas = ['tipos_fallas', 'ubicaciones', 'fallas', 'tecnicos', 'mantenimientos_realizados']
    
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) as count FROM {tabla}")
        count = cursor.fetchone()[0]
        log_message(f"  {tabla:30} : {count:5} registros")
    
    log_message("\n" + "="*80)
    log_message("✓ MIGRACIÓN EXCEL → BD COMPLETADA CON ÉXITO")
    log_message("="*80)
    log_message(f"\nLog guardado en: {log_file}")
    
except Exception as e:
    conn.rollback()
    log_message(f"\n✗ ERROR CRÍTICO: {e}", "ERROR")
    import traceback
    log_message(traceback.format_exc(), "ERROR")
    
finally:
    conn.close()
    log_message("\nConexión cerrada.")
