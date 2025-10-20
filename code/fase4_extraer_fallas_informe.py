#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FASE 4: Extraer y agregar fallas desde INFORME DE CAMARAS.docx
Tarea 16: Procesar el informe y agregar fallas a la tabla consolidada
"""

import sqlite3
import re
from datetime import datetime
from pathlib import Path

db_path = "sistema_camaras.db"
informe_path = "docs/INFORME_DE_CAMARAS.md"
log_file = f"logs/extraccion_fallas_informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

Path("logs").mkdir(exist_ok=True)

def log_message(message, level="INFO"):
    """Registrar mensaje en log y consola"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def extraer_fallas_de_observacion(observacion, zona):
    """
    Extrae fallas individuales de una observación
    Retorna lista de dict con cámara y tipo de falla
    """
    fallas = []
    
    # Patrones de fallas comunes
    patrones = [
        (r'([\w\-_]+)\s*\(Telas de araña\)', 'Telas de araña'),
        (r'([\w\-_]+)\s*\(Borrosa\)', 'Imagen borrosa'),
        (r'([\w\-_]+)\s*\(mica rallada\)', 'Mica rallada'),
        (r'([\w\-_]+)\s*\(DESCONECTADA\)', 'Desconectada'),
        (r'([\w\-_]+)\s*\(mancha en el lente\)', 'Mancha en lente'),
        (r'([\w\-_]+)\s*\(empañada\)', 'Empañada'),
        (r'([\w\-_]+).*?sin conexión', 'Sin conexión'),
        (r'([\w\-_]+).*?intermitencia', 'Intermitencia'),
        (r'Camera\s+(\d+).*?\(Borrosa\)', 'Imagen borrosa'),
        (r'([\w\-_]+).*?destruida', 'Vandalismo/Destruida'),
    ]
    
    for patron, tipo_falla in patrones:
        matches = re.finditer(patron, observacion, re.IGNORECASE)
        for match in matches:
            camara = match.group(1)
            fallas.append({
                'camara': camara,
                'tipo_falla': tipo_falla,
                'zona': zona,
                'observacion': observacion[:200]  # Primeros 200 caracteres
            })
    
    return fallas

def validar_falla_antes_insertar(cursor, camara_nombre):
    """
    Validación ANTI-DUPLICADOS
    """
    cursor.execute("""
        SELECT estado 
        FROM fallas 
        WHERE camaras_afectadas LIKE ? 
        ORDER BY fecha_reporte DESC 
        LIMIT 1
    """, (f'%{camara_nombre}%',))
    
    ultima_falla = cursor.fetchone()
    
    if ultima_falla:
        estado = ultima_falla[0]
        if estado in ['Pendiente', 'Asignada', 'En Proceso', 'Reparada']:
            return False
    
    return True

log_message("="*80)
log_message("FASE 4: Extracción de fallas desde INFORME DE CAMARAS")
log_message("="*80)

# Leer informe
log_message(f"\n[1] Leyendo {informe_path}...")
with open(informe_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

lineas = contenido.split('\n')
log_message(f"  Líneas leídas: {len(lineas)}")

# Conectar a BD
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

try:
    log_message("\n[2] Extrayendo fallas del informe...")
    
    todas_las_fallas = []
    
    # Procesar líneas del informe (formato tabla)
    for linea in lineas:
        if '|' in linea and ('(' in linea or 'conexión' in linea.lower() or 'intermitencia' in linea.lower()):
            partes = linea.split('|')
            if len(partes) >= 5:
                zona = partes[1].strip() if len(partes) > 1 else 'Desconocida'
                observacion = partes[4].strip() if len(partes) > 4 else ''
                
                if observacion and observacion != 'OBSERVACION':
                    fallas_extraidas = extraer_fallas_de_observacion(observacion, zona)
                    todas_las_fallas.extend(fallas_extraidas)
    
    log_message(f"  Total fallas extraídas: {len(todas_las_fallas)}")
    
    # Mostrar muestra
    log_message("\n  Muestra de fallas extraídas:")
    for i, falla in enumerate(todas_las_fallas[:10], 1):
        log_message(f"    {i}. {falla['camara']:30} | {falla['tipo_falla']:20} | Zona: {falla['zona']}")
    
    if len(todas_las_fallas) > 10:
        log_message(f"    ... y {len(todas_las_fallas) - 10} más")
    
    # Insertar en base de datos
    log_message("\n[3] Insertando fallas en base de datos...")
    
    insertadas = 0
    duplicados = 0
    
    for falla in todas_las_fallas:
        # Validación anti-duplicados
        if not validar_falla_antes_insertar(cursor, falla['camara']):
            duplicados += 1
            log_message(f"  ⚠ DUPLICADO: {falla['camara']} ya tiene falla abierta", "WARNING")
            continue
        
        # Mapear tipo de falla a categoría
        categoria_map = {
            'Telas de araña': 'LIMPIEZA',
            'Imagen borrosa': 'LIMPIEZA',
            'Mica rallada': 'REPARACION',
            'Desconectada': 'TECNICA',
            'Mancha en lente': 'LIMPIEZA',
            'Empañada': 'LIMPIEZA',
            'Sin conexión': 'TECNICA',
            'Intermitencia': 'TECNICA',
            'Vandalismo/Destruida': 'REPARACION'
        }
        
        categoria = categoria_map.get(falla['tipo_falla'], 'GENERAL')
        
        # Asignar prioridad según tipo
        prioridad_map = {
            'Desconectada': 'Alta',
            'Sin conexión': 'Alta',
            'Vandalismo/Destruida': 'Crítica',
            'Intermitencia': 'Media',
            'Mica rallada': 'Media'
        }
        
        prioridad = prioridad_map.get(falla['tipo_falla'], 'Baja')
        
        # Insertar
        cursor.execute("""
            INSERT INTO fallas (
                categoria, equipo_tipo, equipo_id, descripcion,
                fecha_reporte, campus, ubicacion, estado, prioridad,
                camaras_afectadas, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            categoria,
            'CAMARA',
            falla['camara'],
            f"{falla['tipo_falla']} en cámara {falla['camara']}",
            '2025-10-12',  # Fecha del informe: DOMINGO 12-10-2025
            'Andrés Bello',
            falla['zona'],
            'Pendiente',
            prioridad,
            falla['camara'],
            falla['observacion']
        ))
        
        insertadas += 1
    
    conn.commit()
    
    log_message(f"\n✓ Fallas insertadas: {insertadas}", "SUCCESS")
    log_message(f"⚠ Duplicados evitados: {duplicados}", "WARNING")
    
    # Verificación final
    log_message("\n[4] Verificación final...")
    cursor.execute("SELECT COUNT(*) as count FROM fallas")
    total_fallas = cursor.fetchone()[0]
    log_message(f"  Total fallas en BD: {total_fallas}")
    
    # Fallas por estado
    cursor.execute("""
        SELECT estado, COUNT(*) as count 
        FROM fallas 
        GROUP BY estado
    """)
    
    estados = cursor.fetchall()
    log_message("\n  Fallas por estado:")
    for estado in estados:
        log_message(f"    {estado[0]:20} : {estado[1]:3} fallas")
    
    log_message("\n" + "="*80)
    log_message("✓ FASE 4 COMPLETADA: Fallas del informe procesadas")
    log_message("="*80)
    log_message(f"\nLog guardado en: {log_file}")
    
except Exception as e:
    conn.rollback()
    log_message(f"\n✗ ERROR: {e}", "ERROR")
    import traceback
    log_message(traceback.format_exc(), "ERROR")
    
finally:
    conn.close()
    log_message("\nConexión cerrada.")
