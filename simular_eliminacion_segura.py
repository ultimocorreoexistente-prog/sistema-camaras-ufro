#!/usr/bin/env python3
"""
Script de prueba para validar eliminación de foreign keys en entorno seguro
Simula el proceso sin modificar la base de datos real
"""

import os
import psycopg2
from urllib.parse import urlparse

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

def simular_eliminacion_segura():
    """Simular el proceso de eliminación sin hacer cambios"""
    print("🧪 SIMULACIÓN SEGURA DE ELIMINACIÓN DE FOREIGN KEYS")
    print("=" * 60)
    
    conn = conectar_bd()
    cur = conn.cursor()
    
    # 1. Verificar que las tablas plurales existen y tienen datos
    print("\n✅ VERIFICANDO TABLAS PRINCIPALES:")
    tablas_principales = ['usuarios', 'camaras', 'ubicaciones']
    
    for tabla in tablas_principales:
        cur.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cur.fetchone()[0]
        print(f"   📊 {tabla}: {count} registros")
    
    # 2. Verificar que las tablas singulares existen
    print("\n⚠️  VERIFICANDO TABLAS DUPLICADAS:")
    tablas_duplicadas = ['usuario', 'camara', 'ubicacion']
    
    for tabla in tablas_duplicadas:
        cur.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cur.fetchone()[0]
        print(f"   📊 {tabla}: {count} registros")
    
    # 3. Simular eliminación de constraints
    print("\n🔧 COMANDOS QUE SE EJECUTARÍAN:")
    
    comandos_validacion = [
        "-- Validación previa: Verificar que no hay registros huérfanos",
        "SELECT COUNT(*) FROM falla WHERE reportado_por_id NOT IN (SELECT id FROM usuario);",
        "SELECT COUNT(*) FROM falla WHERE tecnico_asignado_id NOT IN (SELECT id FROM usuario);",
        "SELECT COUNT(*) FROM mantenimiento WHERE tecnico_id NOT IN (SELECT id FROM usuario);",
        "SELECT COUNT(*) FROM puerto_switch WHERE camara_id NOT IN (SELECT id FROM camara);",
        "SELECT COUNT(*) FROM camara WHERE ubicacion_id NOT IN (SELECT id FROM ubicacion);",
        "",
        "-- COMANDOS DE ELIMINACIÓN REAL:",
        "ALTER TABLE falla DROP CONSTRAINT IF EXISTS falla_reportado_por_id_fkey;",
        "ALTER TABLE falla DROP CONSTRAINT IF EXISTS falla_tecnico_asignado_id_fkey;",
        "ALTER TABLE historial_estado_equipo DROP CONSTRAINT IF EXISTS historial_estado_equipo_usuario_id_fkey;",
        "ALTER TABLE mantenimiento DROP CONSTRAINT IF EXISTS mantenimiento_tecnico_id_fkey;",
        "ALTER TABLE puerto_switch DROP CONSTRAINT IF EXISTS fk_puerto_switch_camara;",
        "ALTER TABLE camara DROP CONSTRAINT IF EXISTS camara_ubicacion_id_fkey;",
        "ALTER TABLE fuente_poder DROP CONSTRAINT IF EXISTS fuente_poder_ubicacion_id_fkey;",
        "ALTER TABLE gabinete DROP CONSTRAINT IF EXISTS gabinete_ubicacion_id_fkey;",
        "ALTER TABLE nvr_dvr DROP CONSTRAINT IF EXISTS nvr_dvr_ubicacion_id_fkey;",
        "ALTER TABLE ups DROP CONSTRAINT IF EXISTS ups_ubicacion_id_fkey;",
        "",
        "-- Eliminación de tablas:",
        "DROP TABLE usuario CASCADE;",
        "DROP TABLE camara CASCADE;",
        "DROP TABLE ubicacion CASCADE;",
        "",
        "-- Verificación final:",
        "SELECT COUNT(*) FROM usuarios;",
        "SELECT COUNT(*) FROM camaras;",
        "SELECT COUNT(*) FROM ubicaciones;"
    ]
    
    for comando in comandos_validacion:
        print(f"   {comando}")
    
    # 4. Ejecutar validaciones reales (solo lecturas)
    print("\n🔍 EJECUTANDO VALIDACIONES:")
    
    # Verificar si hay registros huérfanos
    print("   Verificando integridad de datos...")
    
    # Verificar integridad de foreign keys a 'usuario'
    for tabla, columna, constraint in [
        ('falla', 'reportado_por_id', 'falla_reportado_por_id_fkey'),
        ('falla', 'tecnico_asignado_id', 'falla_tecnico_asignado_id_fkey'),
        ('mantenimiento', 'tecnico_id', 'mantenimiento_tecnico_id_fkey')
    ]:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla} WHERE {columna} NOT IN (SELECT id FROM usuario)")
            huérfanos = cur.fetchone()[0]
            if huérfanos > 0:
                print(f"   ⚠️  {tabla}.{columna}: {huérfanos} registros huérfanos")
            else:
                print(f"   ✅ {tabla}.{columna}: Sin registros huérfanos")
        except Exception as e:
            print(f"   ❌ Error verificando {tabla}.{columna}: {e}")
    
    # Verificar integridad de foreign keys a 'camara'
    try:
        cur.execute("SELECT COUNT(*) FROM puerto_switch WHERE camara_id NOT IN (SELECT id FROM camara)")
        huérfanos = cur.fetchone()[0]
        if huérfanos > 0:
            print(f"   ⚠️  puerto_switch.camara_id: {huérfanos} registros huérfanos")
        else:
            print(f"   ✅ puerto_switch.camara_id: Sin registros huérfanos")
    except Exception as e:
        print(f"   ❌ Error verificando puerto_switch.camara_id: {e}")
    
    # Verificar integridad de foreign keys a 'ubicacion'
    for tabla in ['camara', 'fuente_poder', 'gabinete', 'nvr_dvr', 'ups']:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla} WHERE ubicacion_id NOT IN (SELECT id FROM ubicacion)")
            huérfanos = cur.fetchone()[0]
            if huérfanos > 0:
                print(f"   ⚠️  {tabla}.ubicacion_id: {huérfanos} registros huérfanos")
            else:
                print(f"   ✅ {tabla}.ubicacion_id: Sin registros huérfanos")
        except Exception as e:
            print(f"   ❌ Error verificando {tabla}.ubicacion_id: {e}")
    
    cur.close()
    conn.close()
    
    print("\n🎯 CONCLUSIÓN:")
    print("   Si todos los checks son ✅, la eliminación sería segura.")
    print("   Si hay ⚠️ , se requiere limpieza previa de datos huérfanos.")
    print("   La aplicación seguirá funcionando ya que models.py apunta a tablas plurales.")

def main():
    """Función principal"""
    print("Esta simulación NO modifica la base de datos real")
    print("Ejecuta solo validaciones de lectura")
    print()
    
    simular_eliminacion_segura()

if __name__ == "__main__":
    main()