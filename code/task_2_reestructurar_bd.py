#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Migración y Reestructuración de Base de Datos
Consolida todas las tablas de fallas en una única tabla optimizada
"""

import sqlite3
import sys
from datetime import datetime
import json

def conectar_db():
    """Conecta a la base de datos"""
    try:
        conn = sqlite3.connect('sistema_camaras.db')
        conn.execute('PRAGMA foreign_keys = ON;')  # Activar FKs
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error al conectar: {e}")
        sys.exit(1)

def crear_backup(conn):
    """Crea backup de las tablas antes de migrar"""
    print("\n" + "="*80)
    print("💾 CREANDO BACKUP DE SEGURIDAD")
    print("="*80)
    
    cursor = conn.cursor()
    
    try:
        # Backup casos_reales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backup_casos_reales AS 
            SELECT * FROM casos_reales
        """)
        cursor.execute("SELECT COUNT(*) FROM backup_casos_reales")
        print(f"  ✓ backup_casos_reales: {cursor.fetchone()[0]} registros")
        
        # Backup fallas_especificas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backup_fallas_especificas AS 
            SELECT * FROM fallas_especificas
        """)
        cursor.execute("SELECT COUNT(*) FROM backup_fallas_especificas")
        print(f"  ✓ backup_fallas_especificas: {cursor.fetchone()[0]} registros")
        
        # Backup tecnicos (con duplicados)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backup_tecnicos AS 
            SELECT * FROM tecnicos
        """)
        cursor.execute("SELECT COUNT(*) FROM backup_tecnicos")
        print(f"  ✓ backup_tecnicos: {cursor.fetchone()[0]} registros")
        
        conn.commit()
        print("\n✅ Backup completado")
        print("="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error en backup: {e}")
        return False

def limpiar_tecnicos_duplicados(conn):
    """Elimina técnicos duplicados, mantiene solo los primeros"""
    print("\n" + "="*80)
    print("🧹 LIMPIANDO TÉCNICOS DUPLICADOS")
    print("="*80)
    
    cursor = conn.cursor()
    
    try:
        # Contar antes
        cursor.execute("SELECT COUNT(*) FROM tecnicos")
        antes = cursor.fetchone()[0]
        print(f"\n  Técnicos antes: {antes}")
        
        # Mantener solo el técnico con menor ID por nombre_completo
        cursor.execute("""
            DELETE FROM tecnicos 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM tecnicos 
                GROUP BY nombre_completo
            )
        """)
        
        # Contar después
        cursor.execute("SELECT COUNT(*) FROM tecnicos")
        despues = cursor.fetchone()[0]
        eliminados = antes - despues
        
        print(f"  Técnicos después: {despues}")
        print(f"  Eliminados: {eliminados}")
        
        # Mostrar técnicos finales
        cursor.execute("""
            SELECT id, nombre_completo, rol 
            FROM tecnicos 
            ORDER BY id
        """)
        print("\n  Técnicos finales:")
        for tec in cursor.fetchall():
            print(f"    {tec[0]}. {tec[1]} - {tec[2]}")
        
        conn.commit()
        print("\n✅ Limpieza completada")
        print("="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al limpiar duplicados: {e}")
        conn.rollback()
        return False

def crear_nueva_tabla_fallas(conn):
    """Crea la nueva tabla fallas consolidada"""
    print("\n" + "="*80)
    print("🔧 CREANDO NUEVA TABLA FALLAS CONSOLIDADA")
    print("="*80)
    
    cursor = conn.cursor()
    
    try:
        # Renombrar tabla fallas antigua (está vacía de todas formas)
        cursor.execute("""
            DROP TABLE IF EXISTS fallas_old
        """)
        cursor.execute("""
            ALTER TABLE fallas RENAME TO fallas_old
        """)
        
        # Crear nueva tabla fallas mejorada
        cursor.execute("""
            CREATE TABLE fallas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                -- Identificación del componente afectado
                nombre_camara TEXT,
                componente_afectado_tipo TEXT,
                componente_afectado_id TEXT,
                
                -- Clasificación de la falla
                tipo_falla_id INTEGER,
                tipo_falla_nombre TEXT NOT NULL,
                categoria TEXT,
                prioridad TEXT DEFAULT 'Media' CHECK(prioridad IN ('Baja', 'Media', 'Alta', 'Crítica')),
                
                -- Descripción
                descripcion TEXT NOT NULL,
                observaciones TEXT,
                
                -- Fechas
                fecha_reporte TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                fecha_resolucion TIMESTAMP,
                
                -- Estado y asignación
                estado TEXT DEFAULT 'Pendiente' CHECK(estado IN ('Pendiente', 'Asignada', 'EnProceso', 'Resuelta', 'Cerrada', 'Cancelada')),
                tecnico_id INTEGER,
                
                -- Resolución
                solucion_aplicada TEXT,
                tiempo_resolucion_horas REAL,
                materiales_utilizados TEXT,
                costo_reparacion REAL DEFAULT 0,
                
                -- Contexto
                campus TEXT,
                ubicacion TEXT,
                camaras_afectadas TEXT,  -- JSON o lista separada por comas
                
                -- Datos heredados de casos_reales
                nombre_caso TEXT,
                componentes_involucrados TEXT,
                dependencias_cascada TEXT,
                lecciones_aprendidas TEXT,
                
                -- Auditoría
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Foreign Keys
                FOREIGN KEY (tipo_falla_id) REFERENCES tipos_fallas(id),
                FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id)
            )
        """)
        
        print("\n✅ Tabla 'fallas' consolidada creada")
        print("\n📋 Características:")
        print("  • Soporte para múltiples tipos de componentes")
        print("  • Vinculación con tipos_fallas y técnicos (FK)")
        print("  • Estados: Pendiente, Asignada, EnProceso, Resuelta, Cerrada, Cancelada")
        print("  • Prioridades: Baja, Media, Alta, Crítica")
        print("  • Campos para resolución completa")
        print("  • Auditoría con timestamps")
        
        conn.commit()
        print("\n" + "="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al crear tabla: {e}")
        conn.rollback()
        return False

def migrar_casos_reales(conn):
    """Migra datos de casos_reales a fallas"""
    print("\n" + "="*80)
    print("📦 MIGRANDO CASOS_REALES → FALLAS")
    print("="*80)
    
    cursor = conn.cursor()
    
    try:
        # Obtener casos reales
        cursor.execute("""
            SELECT id, nombre_caso, fecha_caso, descripcion, 
                   componentes_involucrados, dependencias_cascada,
                   solucion_aplicada, tiempo_resolucion_horas, 
                   lecciones_aprendidas
            FROM casos_reales
        """)
        
        casos = cursor.fetchall()
        print(f"\n  Casos a migrar: {len(casos)}")
        print()
        
        for caso in casos:
            caso_id, nombre, fecha, desc, comp, dep, sol, tiempo, lecc = caso
            
            # Determinar técnico si está en componentes_involucrados
            tecnico_id = None
            if comp and 'Charles Jélvez' in comp:
                tecnico_id = 3  # ID de Charles
            
            # Insertar en fallas
            cursor.execute("""
                INSERT INTO fallas (
                    nombre_caso, fecha_reporte, descripcion,
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas, tipo_falla_nombre,
                    estado, tecnico_id, fecha_resolucion,
                    categoria, prioridad
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                nombre,
                fecha,
                desc,
                comp,
                dep,
                sol,
                tiempo,
                lecc,
                'Caso Real Documentado',
                'Resuelta' if sol else 'Pendiente',
                tecnico_id,
                fecha if sol else None,
                'Operacional',
                'Alta'
            ))
            
            print(f"  ✓ Migrado: {nombre}")
        
        conn.commit()
        print(f"\n✅ {len(casos)} casos migrados exitosamente")
        print("="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error en migración: {e}")
        conn.rollback()
        return False

def migrar_fallas_especificas(conn):
    """Migra datos de fallas_especificas a fallas"""
    print("\n" + "="*80)
    print("📦 MIGRANDO FALLAS_ESPECIFICAS → FALLAS")
    print("="*80)
    
    cursor = conn.cursor()
    
    try:
        # Obtener fallas específicas
        cursor.execute("""
            SELECT id, fecha_falla, tipo_falla, componente_afectado_tipo,
                   componente_afectado_id, descripcion_falla, camaras_afectadas,
                   tiempo_downtime_horas, solucion_aplicada, fecha_resolucion,
                   tecnico_reparador, costo_reparacion, estado, prioridad,
                   campus, observaciones
            FROM fallas_especificas
        """)
        
        fallas = cursor.fetchall()
        print(f"\n  Fallas a migrar: {len(fallas)}")
        print()
        
        for falla in fallas:
            (falla_id, fecha_falla, tipo, comp_tipo, comp_id, desc, camaras,
             tiempo, sol, fecha_res, tec, costo, estado, prio, campus, obs) = falla
            
            # Buscar técnico por nombre
            tecnico_id = None
            if tec:
                cursor.execute(
                    "SELECT id FROM tecnicos WHERE nombre_completo LIKE ?",
                    (f"%{tec}%",)
                )
                result = cursor.fetchone()
                if result:
                    tecnico_id = result[0]
            
            # Insertar en fallas
            cursor.execute("""
                INSERT INTO fallas (
                    fecha_reporte, tipo_falla_nombre, componente_afectado_tipo,
                    componente_afectado_id, descripcion, camaras_afectadas,
                    tiempo_resolucion_horas, solucion_aplicada, fecha_resolucion,
                    tecnico_id, costo_reparacion, estado, prioridad,
                    campus, observaciones, categoria
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fecha_falla,
                tipo or 'No Especificado',
                comp_tipo,
                comp_id,
                desc,
                camaras,
                tiempo,
                sol,
                fecha_res,
                tecnico_id,
                costo or 0,
                estado or 'Pendiente',
                prio or 'Media',
                campus,
                obs,
                'Falla Específica'
            ))
            
            tipo_corto = tipo[:30] + '...' if tipo and len(tipo) > 30 else tipo
            print(f"  ✓ Migrado: {tipo_corto} - {comp_tipo}")
        
        conn.commit()
        print(f"\n✅ {len(fallas)} fallas migradas exitosamente")
        print("="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error en migración: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return False

def crear_indices(conn):
    """Crea índices optimizados para la nueva tabla"""
    print("\n" + "="*80)
    print("📑 CREANDO ÍNDICES OPTIMIZADOS")
    print("="*80)
    
    cursor = conn.cursor()
    
    indices = [
        ("idx_fallas_camara", "nombre_camara"),
        ("idx_fallas_estado", "estado"),
        ("idx_fallas_prioridad", "prioridad"),
        ("idx_fallas_tecnico", "tecnico_id"),
        ("idx_fallas_fecha_reporte", "fecha_reporte"),
        ("idx_fallas_campus", "campus"),
        ("idx_fallas_tipo", "tipo_falla_nombre"),
    ]
    
    try:
        for nombre_idx, columna in indices:
            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS {nombre_idx}
                ON fallas({columna})
            """)
            print(f"  ✓ {nombre_idx}")
        
        conn.commit()
        print("\n✅ Índices creados")
        print("="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al crear índices: {e}")
        return False

def verificar_migracion(conn):
    """Verifica que la migración fue exitosa"""
    print("\n" + "="*80)
    print("✓ VERIFICACIÓN DE MIGRACIÓN")
    print("="*80)
    
    cursor = conn.cursor()
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM fallas")
    total_fallas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tecnicos")
    total_tecnicos = cursor.fetchone()[0]
    
    print(f"\n📊 Estadísticas finales:")
    print(f"  • Total fallas: {total_fallas}")
    print(f"  • Total técnicos: {total_tecnicos}")
    
    # Fallas por estado
    print("\n📈 Fallas por estado:")
    cursor.execute("""
        SELECT estado, COUNT(*) 
        FROM fallas 
        GROUP BY estado
        ORDER BY COUNT(*) DESC
    """)
    for estado, count in cursor.fetchall():
        print(f"  • {estado}: {count}")
    
    # Fallas por técnico
    print("\n👥 Fallas por técnico:")
    cursor.execute("""
        SELECT t.nombre_completo, COUNT(f.id)
        FROM fallas f
        LEFT JOIN tecnicos t ON f.tecnico_id = t.id
        GROUP BY t.nombre_completo
        ORDER BY COUNT(f.id) DESC
    """)
    for tec, count in cursor.fetchall():
        nombre = tec if tec else 'Sin asignar'
        print(f"  • {nombre}: {count}")
    
    # Muestra de fallas migradas
    print("\n📋 Muestra de fallas migradas (primeras 5):")
    cursor.execute("""
        SELECT id, tipo_falla_nombre, estado, fecha_reporte
        FROM fallas
        ORDER BY id
        LIMIT 5
    """)
    print("  ID  | Tipo Falla                    | Estado    | Fecha")
    print("  " + "-"*70)
    for falla in cursor.fetchall():
        fid, tipo, estado, fecha = falla
        tipo_short = (tipo[:28] + '..') if len(tipo) > 30 else tipo
        print(f"  {fid:<4}| {tipo_short:<30}| {estado:<10}| {fecha}")
    
    print("\n" + "="*80)

def eliminar_tablas_obsoletas(conn):
    """Elimina las tablas obsoletas ya migradas"""
    print("\n" + "="*80)
    print("🗑️  ELIMINANDO TABLAS OBSOLETAS")
    print("="*80)
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("DROP TABLE IF EXISTS casos_reales")
        print("  ✓ Eliminada: casos_reales")
        
        cursor.execute("DROP TABLE IF EXISTS fallas_especificas")
        print("  ✓ Eliminada: fallas_especificas")
        
        cursor.execute("DROP TABLE IF EXISTS fallas_old")
        print("  ✓ Eliminada: fallas_old (estaba vacía)")
        
        conn.commit()
        print("\n✅ Tablas obsoletas eliminadas")
        print("⚠️  Las tablas backup_* se mantienen por seguridad")
        print("="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al eliminar tablas: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("🚀 REESTRUCTURACIÓN COMPLETA DE BASE DE DATOS")
    print("="*80)
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nProceso:")
    print("  1. Crear backup de seguridad")
    print("  2. Limpiar técnicos duplicados")
    print("  3. Crear nueva tabla fallas consolidada")
    print("  4. Migrar casos_reales → fallas")
    print("  5. Migrar fallas_especificas → fallas")
    print("  6. Crear índices optimizados")
    print("  7. Verificar migración")
    print("  8. Eliminar tablas obsoletas")
    print("="*80)
    
    conn = conectar_db()
    
    try:
        # Paso 1: Backup
        if not crear_backup(conn):
            print("\n❌ Abortando: Error en backup")
            return
        
        # Paso 2: Limpiar duplicados
        if not limpiar_tecnicos_duplicados(conn):
            print("\n❌ Abortando: Error al limpiar técnicos")
            return
        
        # Paso 3: Crear nueva tabla fallas
        if not crear_nueva_tabla_fallas(conn):
            print("\n❌ Abortando: Error al crear tabla fallas")
            return
        
        # Paso 4: Migrar casos_reales
        if not migrar_casos_reales(conn):
            print("\n❌ Abortando: Error al migrar casos_reales")
            return
        
        # Paso 5: Migrar fallas_especificas
        if not migrar_fallas_especificas(conn):
            print("\n❌ Abortando: Error al migrar fallas_especificas")
            return
        
        # Paso 6: Crear índices
        if not crear_indices(conn):
            print("\n⚠️  Advertencia: Índices no creados, pero migración exitosa")
        
        # Paso 7: Verificar
        verificar_migracion(conn)
        
        # Paso 8: Eliminar tablas obsoletas
        if not eliminar_tablas_obsoletas(conn):
            print("\n⚠️  Advertencia: No se pudieron eliminar todas las tablas obsoletas")
        
        print("\n" + "="*80)
        print("✅ REESTRUCTURACIÓN COMPLETADA EXITOSAMENTE")
        print("="*80)
        print("\n📝 Siguiente paso:")
        print("  • Importar fallas desde INFORME DE CAMARAS.docx")
        print("  • Aplicar validación anti-duplicados")
        print("="*80)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print("\n🔌 Conexión cerrada\n")

if __name__ == "__main__":
    main()
