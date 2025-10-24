#!/usr/bin/env python3
"""
Análisis completo de foreign key dependencies para eliminar tablas duplicadas
Determina todas las opciones disponibles para limpiar la base de datos
"""

import os
import psycopg2
from urllib.parse import urlparse
import json

def conectar_bd():
    """Conectar a la base de datos Railway PostgreSQL"""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        db_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
    
    parsed = urlparse(db_url)
    
    return psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password
    )

def obtener_todas_las_dependencias():
    """Obtener todas las foreign key dependencies en la base de datos"""
    print("🔍 ANALIZANDO TODAS LAS FOREIGN KEY DEPENDENCIES...")
    
    conn = conectar_bd()
    cur = conn.cursor()
    
    # Consulta para obtener todas las foreign keys
    cur.execute("""
        SELECT 
            tc.constraint_name, 
            tc.table_name AS referencing_table,
            kcu.column_name AS referencing_column,
            ccu.table_name AS referenced_table,
            ccu.column_name AS referenced_column
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        ORDER BY tc.table_name, ccu.table_name
    """)
    
    dependencias = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return dependencias

def analizar_dependencias_por_tabla():
    """Analizar específicamente las dependencias de las tablas problemáticas"""
    print("🎯 ANALIZANDO DEPENDENCIAS DE TABLAS PROBLEMÁTICAS...")
    
    tablas_objetivo = ['usuario', 'camara', 'ubicacion']
    dependencias_por_tabla = {}
    
    conn = conectar_bd()
    cur = conn.cursor()
    
    for tabla in tablas_objetivo:
        print(f"\n📊 DEPENDENCIAS DE '{tabla}':")
        
        # Buscar foreign keys que referencian a esta tabla
        cur.execute("""
            SELECT 
                tc.constraint_name, 
                tc.table_name AS referencing_table,
                kcu.column_name AS referencing_column,
                ccu.column_name AS referenced_column
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND ccu.table_name = %s
            ORDER BY tc.table_name
        """, (tabla,))
        
        dependencias = cur.fetchall()
        
        if dependencias:
            for dep in dependencias:
                print(f"   🔗 {dep[1]}.{dep[2]} → {tabla}.{dep[3]} (constraint: {dep[0]})")
            dependencias_por_tabla[tabla] = dependencias
        else:
            print(f"   ✅ No hay dependencias directas para {tabla}")
            dependencias_por_tabla[tabla] = []
    
    cur.close()
    conn.close()
    
    return dependencias_por_tabla

def generar_comandos_eliminacion(dependencias_por_tabla):
    """Generar comandos SQL para eliminar las dependencias"""
    print("\n🛠️  GENERANDO COMANDOS DE ELIMINACIÓN...")
    
    comandos_sql = []
    
    for tabla, dependencias in dependencias_por_tabla.items():
        if dependencias:
            print(f"\n📋 COMANDOS PARA ELIMINAR DEPENDENCIAS DE '{tabla}':")
            
            # Agrupar por tabla de referencia
            tablas_ref = {}
            for dep in dependencias:
                constraint_name = dep[0]
                referencing_table = dep[1]
                referencing_column = dep[2]
                
                if referencing_table not in tablas_ref:
                    tablas_ref[referencing_table] = []
                tablas_ref[referencing_table].append({
                    'constraint': constraint_name,
                    'column': referencing_column
                })
            
            # Generar comandos
            for ref_table, constraints in tablas_ref.items():
                for constraint in constraints:
                    cmd = f"ALTER TABLE {ref_table} DROP CONSTRAINT IF EXISTS {constraint['constraint']};"
                    print(f"   🔧 {cmd}")
                    comandos_sql.append(cmd)
        else:
            print(f"✅ No hay comandos para {tabla} - sin dependencias")
    
    return comandos_sql

def generar_script_completo(dependencias_por_tabla, comandos_sql):
    """Generar script SQL completo para limpieza"""
    
    script_content = """-- SCRIPT PARA ELIMINAR FOREIGN KEY DEPENDENCIES Y TABLAS DUPLICADAS
-- Sistema de Gestión de Cámaras UFRO
-- Autor: MiniMax Agent
-- Fecha: 2025-10-25

-- ===============================================================
-- PARTE 1: ELIMINACIÓN DE FOREIGN KEY CONSTRAINTS
-- ===============================================================

"""
    
    for tabla, dependencias in dependencias_por_tabla.items():
        if dependencias:
            script_content += f"-- Dependencias de la tabla '{tabla}':\n"
            for dep in dependencias:
                cmd = f"ALTER TABLE {dep[1]} DROP CONSTRAINT IF EXISTS {dep[0]};"
                script_content += f"{cmd}\n"
            script_content += "\n"
    
    script_content += """-- ===============================================================
-- PARTE 2: ELIMINACIÓN DE TABLAS DUPLICADAS
-- ===============================================================

"""
    
    script_content += "-- Verificar que las tablas plurales existen (usando datos reales)\n"
    script_content += "SELECT 'Verificando tablas principales...' AS status;\n"
    script_content += "SELECT COUNT(*) FROM usuarios;\n"
    script_content += "SELECT COUNT(*) FROM camaras;\n"
    script_content += "SELECT COUNT(*) FROM ubicaciones;\n\n"
    
    script_content += "-- Eliminar tablas singulares (duplicadas)\n"
    script_content += "DROP TABLE IF EXISTS usuario CASCADE;\n"
    script_content += "DROP TABLE IF EXISTS camara CASCADE;\n"
    script_content += "DROP TABLE IF EXISTS ubicacion CASCADE;\n\n"
    
    script_content += "-- ===============================================================\n"
    script_content += "-- PARTE 3: VERIFICACIÓN FINAL\n"
    script_content += "-- ===============================================================\n\n"
    
    script_content += "SELECT 'Estado final de la base de datos' AS status;\n"
    script_content += "SELECT table_name \n"
    script_content += "FROM information_schema.tables \n"
    script_content += "WHERE table_schema = 'public' \n"
    script_content += "AND table_type = 'BASE TABLE'\n"
    script_content += "ORDER BY table_name;\n"
    
    return script_content

def evaluar_opciones_limpieza():
    """Evaluar diferentes opciones para la limpieza"""
    print("\n📊 EVALUANDO OPCIONES DE LIMPIEZA...")
    
    opciones = {
        "OPCIÓN 1 - ELIMINACIÓN DIRECTA (CASCADE)": {
            "comando": "DROP TABLE {tabla} CASCADE;",
            "riesgo": "ALTO - Puede eliminar datos y restricciones",
            "ventaja": "Proceso simple y rápido",
            "conclusión": "❌ NO RECOMENDADO - Riesgo de pérdida de datos"
        },
        "OPCIÓN 2 - ELIMINACIÓN SELECTIVA": {
            "comando": "ALTER TABLE {tabla_ref} DROP CONSTRAINT {constraint_name}; DROP TABLE {tabla};",
            "riesgo": "BAJO - Precisión quirúrgica",
            "ventaja": "Control total sobre qué eliminar",
            "conclusión": "✅ RECOMENDADA - Método más seguro"
        },
        "OPCIÓN 3 - MIGRACIÓN PROGRESSIVA": {
            "comando": "INSERT INTO plural_table SELECT * FROM singular_table; DROP TABLE {tabla};",
            "riesgo": "MEDIO - Doble proceso",
            "ventaja": "Preservación de datos históricos",
            "conclusión": "⚠️  CONSIDERAR si hay datos importantes en tablas singulares"
        },
        "OPCIÓN 4 - NO HACER NADA": {
            "comando": "Mantener ambas tablas",
            "riesgo": "NINGUNO - Estado actual",
            "ventaja": "No riesgo de ruptura del sistema",
            "conclusión": "✅ RECOMENDADA SI NO HAY PROBLEMAS RENDIMIENTO"
        }
    }
    
    for opcion, detalles in opciones.items():
        print(f"\n{opcion}:")
        print(f"   Comando: {detalles['comando']}")
        print(f"   Riesgo: {detalles['riesgo']}")
        print(f"   Ventaja: {detalles['ventaja']}")
        print(f"   Conclusión: {detalles['conclusión']}")
    
    return opciones

def main():
    """Función principal de análisis"""
    print("🚀 ANÁLISIS COMPLETO DE FOREIGN KEY DEPENDENCIES")
    print("=" * 60)
    
    # 1. Obtener todas las dependencias
    todas_dependencias = obtener_todas_las_dependencias()
    print(f"\n📊 Total de foreign key constraints: {len(todas_dependencias)}")
    
    # 2. Analizar dependencias específicas
    dependencias_por_tabla = analizar_dependencias_por_tabla()
    
    # 3. Generar comandos SQL
    comandos_sql = generar_comandos_eliminacion(dependencias_por_tabla)
    
    # 4. Evaluar opciones
    opciones = evaluar_opciones_limpieza()
    
    # 5. Generar script completo
    script_sql = generar_script_completo(dependencias_por_tabla, comandos_sql)
    
    # Guardar script
    script_path = "/workspace/sistema-camaras-flask/limpiar_foreign_keys_completo.sql"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_sql)
    
    print(f"\n💾 Script SQL generado: {script_path}")
    
    # 6. Reporte resumen
    print("\n" + "=" * 60)
    print("📋 REPORTE RESUMEN:")
    print("=" * 60)
    
    total_dependencias = sum(len(deps) for deps in dependencias_por_tabla.values())
    print(f"🔗 Total de foreign keys que referencian tablas singulares: {total_dependencias}")
    
    tablas_con_dependencias = [tabla for tabla, deps in dependencias_por_tabla.items() if deps]
    print(f"⚠️  Tablas con dependencias: {tablas_con_dependencias}")
    
    if not tablas_con_dependencias:
        print("✅ No hay dependencias - Se puede eliminar tablas directamente")
    else:
        print("🚫 Hay dependencias - Requiere eliminación selectiva")
    
    print("\n🎯 RECOMENDACIÓN:")
    if len(todas_dependencias) == 0:
        print("✅ OPCIÓN RECOMENDADA: No hacer nada - las tablas duplicadas no afectan")
    elif total_dependencias < 5:
        print("✅ OPCIÓN RECOMENDADA: Eliminación selectiva (Opción 2)")
    else:
        print("⚠️  OPCIÓN RECOMENDADA: No hacer nada (Opción 4) - Demasiadas dependencias")
    
    print("\n📝 Para ejecutar la limpieza manualmente:")
    print(f"   1. Conectar a la base de datos PostgreSQL")
    print(f"   2. Ejecutar: {script_path}")
    print(f"   3. Verificar integridad de datos después")
    
    return {
        'dependencias': dependencias_por_tabla,
        'comandos_sql': comandos_sql,
        'script_path': script_path,
        'recomendacion': "No hacer nada" if len(tablas_con_dependencias) == 0 else "Eliminación selectiva"
    }

if __name__ == "__main__":
    resultado = main()