#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Maestro de Reestructuración Completa de Base de Datos
Sistema de Gestión de Cámaras UFRO

Implementa:
- Tarea 2: Consolidar 3 tablas de fallas en 1
- Tarea 3: Limpiar duplicados técnicos (16→4)
- Tarea 4: Eliminar duplicados mantenimientos
- Tarea 5: Normalizar ubicaciones
- Tarea 6: Estandarizar estados de fallas
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

db_path = "sistema_camaras.db"
log_file = f"logs/reestructuracion_bd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Crear directorio de logs
Path("logs").mkdir(exist_ok=True)

def log_message(message, level="INFO"):
    """Registrar mensaje en log y consola"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def ejecutar_query(cursor, query, params=None, descripcion=""):
    """Ejecutar query con logging"""
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        log_message(f"✓ {descripcion}", "SUCCESS")
        return True
    except Exception as e:
        log_message(f"✗ Error en {descripcion}: {e}", "ERROR")
        return False

log_message("="*80)
log_message("INICIO: Reestructuración Completa de Base de Datos")
log_message("="*80)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

try:
    # ==========================================================================
    # TAREA 2: CONSOLIDAR TABLAS DE FALLAS
    # ==========================================================================
    log_message("\n" + "="*80)
    log_message("TAREA 2: Consolidar 3 tablas de fallas → 1 tabla unificada")
    log_message("="*80)
    
    # Paso 1: Crear tabla estados_falla primero (necesaria para FK)
    log_message("\n[2.0] Creando tabla de estados de fallas...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estados_falla (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            orden INTEGER
        )
    """)
    
    # Insertar estados si no existen
    estados = [
        ('Pendiente', 'Falla reportada, sin asignar', 1),
        ('Asignada', 'Asignada a técnico', 2),
        ('En Proceso', 'Técnico trabajando', 3),
        ('Reparada', 'Reparación completada', 4),
        ('Cerrada', 'Verificada y cerrada', 5),
        ('Cancelada', 'Duplicada o error', 6)
    ]
    
    for nombre, desc, orden in estados:
        cursor.execute("""
            INSERT OR IGNORE INTO estados_falla (nombre, descripcion, orden)
            VALUES (?, ?, ?)
        """, (nombre, desc, orden))
    
    log_message("✓ Tabla estados_falla creada con 6 estados", "SUCCESS")
    
    # Paso 2: Renombrar tabla fallas actual (vacía) a fallas_old
    log_message("\n[2.1] Renombrando tabla 'fallas' actual...")
    try:
        cursor.execute("DROP TABLE IF EXISTS fallas_old")
        cursor.execute("ALTER TABLE fallas RENAME TO fallas_old")
        log_message("✓ Tabla 'fallas' renombrada a 'fallas_old'", "SUCCESS")
    except:
        log_message("⚠ Tabla 'fallas' no existe, continuando...", "WARNING")
    
    # Paso 3: Crear nueva tabla fallas unificada
    log_message("\n[2.2] Creando nueva tabla 'fallas' unificada...")
    cursor.execute("""
        CREATE TABLE fallas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            -- Clasificación
            tipo_falla_id INTEGER,
            categoria TEXT,  -- CAMARA, SWITCH, UPS, NVR, GABINETE, CABLE, ELECTRICO, RED
            
            -- Componente Afectado (polimórfico)
            equipo_tipo TEXT,
            equipo_id TEXT,
            
            -- Detalles de la Falla
            descripcion TEXT NOT NULL,
            fecha_reporte TIMESTAMP NOT NULL,
            reportado_por_id INTEGER,
            
            -- Ubicación
            campus TEXT,
            ubicacion TEXT,
            ubicacion_id INTEGER,
            
            -- Workflow
            estado TEXT DEFAULT 'Pendiente',
            prioridad TEXT DEFAULT 'Media',
            
            -- Asignación
            fecha_asignacion TIMESTAMP,
            tecnico_asignado_id INTEGER,
            tecnico_asignado_nombre TEXT,
            
            -- Resolución
            fecha_inicio_reparacion TIMESTAMP,
            fecha_fin_reparacion TIMESTAMP,
            tiempo_resolucion_horas REAL,
            solucion_aplicada TEXT,
            materiales_utilizados TEXT,
            costo_reparacion REAL,
            
            -- Impacto
            camaras_afectadas TEXT,
            tiempo_downtime_horas REAL,
            dependencias_cascada TEXT,
            
            -- Metadatos
            observaciones TEXT,
            lecciones_aprendidas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (tipo_falla_id) REFERENCES tipos_fallas(id),
            FOREIGN KEY (tecnico_asignado_id) REFERENCES tecnicos(id),
            FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id)
        )
    """)
    log_message("✓ Nueva tabla 'fallas' creada con estructura completa", "SUCCESS")
    
    # Paso 4: Migrar datos de fallas_especificas
    log_message("\n[2.3] Migrando datos de 'fallas_especificas'...")
    cursor.execute("SELECT COUNT(*) as count FROM fallas_especificas")
    count_fallas_esp = cursor.fetchone()['count']
    log_message(f"Registros a migrar: {count_fallas_esp}")
    
    # Obtener datos únicos (eliminar duplicados)
    cursor.execute("""
        SELECT 
            MIN(id) as id_original,
            fecha_falla,
            tipo_falla,
            componente_afectado_tipo,
            componente_afectado_id,
            descripcion_falla,
            camaras_afectadas,
            tiempo_downtime_horas,
            solucion_aplicada,
            fecha_resolucion,
            tecnico_reparador,
            costo_reparacion,
            estado,
            prioridad,
            campus,
            observaciones
        FROM fallas_especificas
        GROUP BY fecha_falla, componente_afectado_id, descripcion_falla
    """)
    
    fallas_esp_unicas = cursor.fetchall()
    log_message(f"Registros únicos (sin duplicados): {len(fallas_esp_unicas)}")
    
    for falla in fallas_esp_unicas:
        # Mapear estado
        estado_mapeo = {
            'Resuelto': 'Cerrada',
            'Resuelta': 'Cerrada',
            'Pendiente': 'Pendiente',
            'En Proceso': 'En Proceso'
        }
        estado_nuevo = estado_mapeo.get(falla['estado'], 'Cerrada')
        
        # Calcular tiempo resolución si hay fechas
        tiempo_res = falla['tiempo_downtime_horas']
        
        cursor.execute("""
            INSERT INTO fallas (
                categoria, equipo_tipo, equipo_id, descripcion,
                fecha_reporte, campus, ubicacion, estado, prioridad,
                fecha_fin_reparacion, tiempo_resolucion_horas,
                solucion_aplicada, costo_reparacion,
                camaras_afectadas, tiempo_downtime_horas,
                tecnico_asignado_nombre, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            falla['componente_afectado_tipo'],
            falla['componente_afectado_tipo'],
            falla['componente_afectado_id'],
            falla['descripcion_falla'],
            falla['fecha_falla'],
            falla['campus'],
            None,
            estado_nuevo,
            falla['prioridad'],
            falla['fecha_resolucion'],
            tiempo_res,
            falla['solucion_aplicada'],
            falla['costo_reparacion'],
            falla['camaras_afectadas'],
            falla['tiempo_downtime_horas'],
            falla['tecnico_reparador'],
            falla['observaciones']
        ))
    
    log_message(f"✓ Migrados {len(fallas_esp_unicas)} registros de 'fallas_especificas'", "SUCCESS")
    
    # Paso 5: Migrar datos de casos_reales
    log_message("\n[2.4] Migrando datos de 'casos_reales'...")
    cursor.execute("SELECT COUNT(*) as count FROM casos_reales")
    count_casos = cursor.fetchone()['count']
    log_message(f"Registros a migrar: {count_casos}")
    
    cursor.execute("""
        SELECT 
            id,
            nombre_caso,
            fecha_caso,
            descripcion,
            componentes_involucrados,
            dependencias_cascada,
            solucion_aplicada,
            tiempo_resolucion_horas,
            lecciones_aprendidas
        FROM casos_reales
    """)
    
    casos = cursor.fetchall()
    
    for caso in casos:
        # Extraer campus del nombre o descripción
        campus = 'Andrés Bello'  # Default
        if 'CFT' in caso['nombre_caso']:
            campus = 'Andrés Bello'
        elif 'ZM' in caso['nombre_caso']:
            campus = 'Andrés Bello'
        
        cursor.execute("""
            INSERT INTO fallas (
                categoria, equipo_tipo, equipo_id, descripcion,
                fecha_reporte, campus, estado, prioridad,
                tiempo_resolucion_horas, solucion_aplicada,
                camaras_afectadas, dependencias_cascada,
                lecciones_aprendidas, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'CASO_REAL',
            'MULTIPLE',
            caso['nombre_caso'],
            caso['descripcion'],
            caso['fecha_caso'],
            campus,
            'Cerrada',
            'Alta',
            caso['tiempo_resolucion_horas'],
            caso['solucion_aplicada'],
            caso['componentes_involucrados'],
            caso['dependencias_cascada'],
            caso['lecciones_aprendidas'],
            f"Caso de estudio: {caso['nombre_caso']}"
        ))
    
    log_message(f"✓ Migrados {len(casos)} registros de 'casos_reales'", "SUCCESS")
    
    # Paso 6: Verificar migración
    log_message("\n[2.5] Verificando migración...")
    cursor.execute("SELECT COUNT(*) as count FROM fallas")
    count_fallas_nuevas = cursor.fetchone()['count']
    log_message(f"Total registros en tabla 'fallas' nueva: {count_fallas_nuevas}")
    
    # Paso 7: Eliminar tablas obsoletas
    log_message("\n[2.6] Eliminando tablas obsoletas...")
    cursor.execute("DROP TABLE IF EXISTS fallas_especificas")
    log_message("✓ Tabla 'fallas_especificas' eliminada", "SUCCESS")
    
    cursor.execute("DROP TABLE IF EXISTS casos_reales")
    log_message("✓ Tabla 'casos_reales' eliminada", "SUCCESS")
    
    cursor.execute("DROP TABLE IF EXISTS fallas_old")
    log_message("✓ Tabla 'fallas_old' eliminada", "SUCCESS")
    
    conn.commit()
    log_message("\n✓ TAREA 2 COMPLETADA: Consolidación de tablas de fallas exitosa", "SUCCESS")
    
    # ==========================================================================
    # TAREA 3: LIMPIAR DUPLICADOS EN TABLA TECNICOS
    # ==========================================================================
    log_message("\n" + "="*80)
    log_message("TAREA 3: Limpiar duplicados en tabla 'tecnicos' (16→4)")
    log_message("="*80)
    
    # Verificar estado actual
    cursor.execute("SELECT COUNT(*) as count FROM tecnicos")
    count_antes = cursor.fetchone()['count']
    log_message(f"\n[3.1] Técnicos antes de limpieza: {count_antes}")
    
    # Eliminar todos los registros
    cursor.execute("DELETE FROM tecnicos")
    log_message("✓ Registros eliminados", "SUCCESS")
    
    # Reinsertar los 4 técnicos únicos
    log_message("\n[3.2] Insertando 4 técnicos únicos...")
    tecnicos = [
        ('Oliver', 'Carrasco', 'Oliver Carrasco', None, None, 'Mantenimiento de Cámaras', 'Técnico', 'Activo', None),
        ('Marcos', 'Altamirano', 'Marcos Altamirano', None, None, 'Sistemas de Vigilancia', 'Técnico', 'Activo', None),
        ('Charles', 'Jélvez', 'Charles Jélvez', None, None, 'Administración de Sistemas', 'SuperAdmin', 'Activo', 'SuperAdmin del sistema - Desarrollador'),
        ('Marco', 'Contreras', 'Marco Contreras', None, None, 'Encargado Seguridad', 'Supervisor', 'Activo', None)
    ]
    
    for tec in tecnicos:
        cursor.execute("""
            INSERT INTO tecnicos (
                nombre, apellido, nombre_completo, email, telefono,
                especialidad, rol, estado, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tec)
        log_message(f"  ✓ Insertado: {tec[2]} ({tec[6]})", "SUCCESS")
    
    # Verificar
    cursor.execute("SELECT COUNT(*) as count FROM tecnicos")
    count_despues = cursor.fetchone()['count']
    log_message(f"\n[3.3] Técnicos después de limpieza: {count_despues}")
    
    conn.commit()
    log_message("\n✓ TAREA 3 COMPLETADA: Limpieza de técnicos exitosa", "SUCCESS")
    
    # ==========================================================================
    # TAREA 4: ELIMINAR DUPLICADOS EN MANTENIMIENTOS
    # ==========================================================================
    log_message("\n" + "="*80)
    log_message("TAREA 4: Eliminar duplicados en 'mantenimientos_realizados'")
    log_message("="*80)
    
    # Contar duplicados
    log_message("\n[4.1] Identificando duplicados...")
    cursor.execute("""
        SELECT 
            fecha_mantenimiento, 
            componente_id, 
            descripcion_trabajo,
            COUNT(*) as duplicados
        FROM mantenimientos_realizados
        GROUP BY fecha_mantenimiento, componente_id, descripcion_trabajo
        HAVING COUNT(*) > 1
    """)
    
    duplicados = cursor.fetchall()
    log_message(f"Grupos de duplicados encontrados: {len(duplicados)}")
    
    for dup in duplicados:
        log_message(f"  - {dup['fecha_mantenimiento']} | {dup['componente_id']}: {dup['duplicados']} copias")
    
    # Eliminar duplicados (mantener solo el ID más bajo)
    log_message("\n[4.2] Eliminando duplicados...")
    cursor.execute("""
        DELETE FROM mantenimientos_realizados
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM mantenimientos_realizados
            GROUP BY fecha_mantenimiento, componente_id, descripcion_trabajo
        )
    """)
    
    eliminados = cursor.rowcount
    log_message(f"✓ Eliminados {eliminados} registros duplicados", "SUCCESS")
    
    # Verificar
    cursor.execute("SELECT COUNT(*) as count FROM mantenimientos_realizados")
    count_final = cursor.fetchone()['count']
    log_message(f"\n[4.3] Mantenimientos únicos finales: {count_final}")
    
    conn.commit()
    log_message("\n✓ TAREA 4 COMPLETADA: Eliminación de duplicados exitosa", "SUCCESS")
    
    # ==========================================================================
    # TAREA 5: NORMALIZAR UBICACIONES
    # ==========================================================================
    log_message("\n" + "="*80)
    log_message("TAREA 5: Normalizar ubicaciones con tabla centralizada")
    log_message("="*80)
    
    log_message("\n[5.1] Creando tabla 'ubicaciones'...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ubicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campus TEXT NOT NULL,
            edificio TEXT,
            piso TEXT,
            zona TEXT,
            descripcion TEXT,
            latitud REAL,
            longitud REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    log_message("✓ Tabla 'ubicaciones' creada", "SUCCESS")
    
    # Extraer ubicaciones únicas de infraestructura_red
    log_message("\n[5.2] Extrayendo ubicaciones únicas...")
    cursor.execute("""
        SELECT DISTINCT campus, ubicacion
        FROM infraestructura_red
        WHERE campus IS NOT NULL
    """)
    
    ubicaciones = cursor.fetchall()
    log_message(f"Ubicaciones únicas encontradas: {len(ubicaciones)}")
    
    for ubic in ubicaciones:
        # Separar edificio/zona
        edificio = ubic['ubicacion'] if ubic['ubicacion'] else None
        
        cursor.execute("""
            INSERT OR IGNORE INTO ubicaciones (campus, edificio)
            VALUES (?, ?)
        """, (ubic['campus'], edificio))
    
    # Agregar ubicaciones de fallas
    cursor.execute("""
        SELECT DISTINCT campus, ubicacion
        FROM fallas
        WHERE campus IS NOT NULL
    """)
    
    ubicaciones_fallas = cursor.fetchall()
    for ubic in ubicaciones_fallas:
        cursor.execute("""
            INSERT OR IGNORE INTO ubicaciones (campus, edificio)
            VALUES (?, ?)
        """, (ubic['campus'], ubic['ubicacion']))
    
    # Verificar
    cursor.execute("SELECT COUNT(*) as count FROM ubicaciones")
    count_ubicaciones = cursor.fetchone()['count']
    log_message(f"\n[5.3] Total ubicaciones creadas: {count_ubicaciones}")
    
    conn.commit()
    log_message("\n✓ TAREA 5 COMPLETADA: Tabla de ubicaciones creada (FK pendientes para implementación futura)", "SUCCESS")
    
    # ==========================================================================
    # TAREA 6: VERIFICACIÓN FINAL
    # ==========================================================================
    log_message("\n" + "="*80)
    log_message("VERIFICACIÓN FINAL DE REESTRUCTURACIÓN")
    log_message("="*80)
    
    log_message("\n[6.1] Conteo de registros en tablas principales:")
    
    tablas_verificar = [
        'fallas',
        'tecnicos',
        'mantenimientos_realizados',
        'ubicaciones',
        'estados_falla',
        'tipos_fallas',
        'infraestructura_red',
        'camaras'
    ]
    
    for tabla in tablas_verificar:
        try:
            cursor.execute(f"SELECT COUNT(*) as count FROM {tabla}")
            count = cursor.fetchone()['count']
            log_message(f"  • {tabla:30} : {count:5} registros")
        except Exception as e:
            log_message(f"  • {tabla:30} : ERROR - {e}", "ERROR")
    
    log_message("\n[6.2] Verificando integridad de datos migrados...")
    
    # Verificar que no hay fallas sin descripción
    cursor.execute("SELECT COUNT(*) as count FROM fallas WHERE descripcion IS NULL OR descripcion = ''")
    fallas_sin_desc = cursor.fetchone()['count']
    if fallas_sin_desc == 0:
        log_message("  ✓ Todas las fallas tienen descripción", "SUCCESS")
    else:
        log_message(f"  ⚠ {fallas_sin_desc} fallas sin descripción", "WARNING")
    
    # Verificar estados válidos
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM fallas 
        WHERE estado NOT IN ('Pendiente', 'Asignada', 'En Proceso', 'Reparada', 'Cerrada', 'Cancelada')
    """)
    estados_invalidos = cursor.fetchone()['count']
    if estados_invalidos == 0:
        log_message("  ✓ Todos los estados de fallas son válidos", "SUCCESS")
    else:
        log_message(f"  ⚠ {estados_invalidos} fallas con estado inválido", "WARNING")
    
    conn.commit()
    
    log_message("\n" + "="*80)
    log_message("✓ REESTRUCTURACIÓN COMPLETA DE BASE DE DATOS FINALIZADA CON ÉXITO")
    log_message("="*80)
    log_message(f"\nLog guardado en: {log_file}")
    
except Exception as e:
    conn.rollback()
    log_message(f"\n✗ ERROR CRÍTICO: {e}", "ERROR")
    import traceback
    log_message(traceback.format_exc(), "ERROR")
    
finally:
    conn.close()
    log_message("\nConexión a base de datos cerrada.")
