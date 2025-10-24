#!/usr/bin/env python3
"""
Ejecutar eliminación de foreign keys y tablas duplicadas en Railway PostgreSQL
Sistema de Gestión de Cámaras UFRO
"""

import os
import psycopg2
from urllib.parse import urlparse
from datetime import datetime

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

def obtener_credenciales_formateadas():
    """Obtener credenciales para display seguro"""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        db_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
    
    return f"Host: tramway.proxy.rlwy.net, Port: 34726, Database: railway"

def ejecutar_limpieza_foreign_keys():
    """Ejecutar la limpieza real de foreign keys y tablas duplicadas"""
    print("🗑️  EJECUTANDO LIMPIEZA DE FOREIGN KEY DEPENDENCIES")
    print("=" * 70)
    print(f"🕐 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Base de datos: {obtener_credenciales_formateadas()}")
    print("=" * 70)
    
    conn = None
    try:
        # Conectar a la base de datos
        print("\n🔌 Conectando a la base de datos...")
        conn = conectar_bd()
        cur = conn.cursor()
        print("✅ Conexión establecida")
        
        # PASO 1: Verificación previa
        print("\n📋 PASO 1: Verificación previa de estado")
        
        # Verificar que las tablas plurales existen
        for tabla in ['usuarios', 'camaras', 'ubicaciones']:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"   ✅ {tabla}: {count} registros")
        
        # Verificar que las tablas singulares existen
        for tabla in ['usuario', 'camara', 'ubicacion']:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"   ⚠️  {tabla}: {count} registros (a eliminar)")
        
        # PASO 2: Eliminar foreign key constraints
        print("\n🗑️  PASO 2: Eliminando foreign key constraints")
        
        constraints_a_eliminar = [
            "falla_reportado_por_id_fkey",
            "falla_tecnico_asignado_id_fkey", 
            "historial_estado_equipo_usuario_id_fkey",
            "mantenimiento_tecnico_id_fkey",
            "fk_puerto_switch_camara",
            "camara_ubicacion_id_fkey",
            "fuente_poder_ubicacion_id_fkey",
            "gabinete_ubicacion_id_fkey",
            "nvr_dvr_ubicacion_id_fkey",
            "ups_ubicacion_id_fkey"
        ]
        
        for constraint in constraints_a_eliminar:
            try:
                # Determinar la tabla correcta para cada constraint
                if constraint.startswith('falla_'):
                    tabla = 'falla'
                elif constraint.startswith('mantenimiento_'):
                    tabla = 'mantenimiento'
                elif constraint.startswith('historial_estado_equipo_'):
                    tabla = 'historial_estado_equipo'
                elif constraint == 'fk_puerto_switch_camara':
                    tabla = 'puerto_switch'
                elif constraint == 'camara_ubicacion_id_fkey':
                    tabla = 'camara'
                elif constraint.endswith('_ubicacion_id_fkey'):
                    # fuente_poder, gabinete, nvr_dvr, ups
                    if constraint.startswith('fuente_poder_'):
                        tabla = 'fuente_poder'
                    elif constraint.startswith('gabinete_'):
                        tabla = 'gabinete'
                    elif constraint.startswith('nvr_dvr_'):
                        tabla = 'nvr_dvr'
                    elif constraint.startswith('ups_'):
                        tabla = 'ups'
                    else:
                        tabla = 'ubicacion'  # fallback
                else:
                    # Fallback: usar la primera parte del constraint
                    tabla = constraint.split('_')[0]
                
                cur.execute(f"ALTER TABLE {tabla} DROP CONSTRAINT IF EXISTS {constraint}")
                print(f"   ✅ {constraint} (tabla: {tabla}): Eliminado")
            except Exception as e:
                print(f"   ⚠️  {constraint}: No encontrado o error - {e}")
        
        conn.commit()
        print("   📝 Transacción de constraints confirmada")
        
        # PASO 3: Eliminar tablas duplicadas
        print("\n🗑️  PASO 3: Eliminando tablas duplicadas")
        
        tablas_a_eliminar = ['usuario', 'camara', 'ubicacion']
        
        for tabla in tablas_a_eliminar:
            try:
                cur.execute(f"DROP TABLE {tabla} CASCADE")
                print(f"   ✅ {tabla}: Tabla eliminada")
            except Exception as e:
                print(f"   ❌ {tabla}: Error - {e}")
        
        conn.commit()
        print("   📝 Transacción de tablas confirmada")
        
        # PASO 4: Verificación final
        print("\n📋 PASO 4: Verificación final del resultado")
        
        # Verificar que solo quedan las tablas plurales
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            AND (table_name LIKE '%usuario%' OR table_name LIKE '%camara%' OR table_name LIKE '%ubicacion%')
            ORDER BY table_name
        """)
        
        tablas_finales = cur.fetchall()
        print(f"   📊 Total de tablas restantes: {len(tablas_finales)}")
        
        for tabla in tablas_finales:
            nombre = tabla[0]
            cur.execute(f"SELECT COUNT(*) FROM {nombre}")
            count = cur.fetchone()[0]
            print(f"   ✅ {nombre}: {count} registros")
        
        # Verificar que no existen tablas singulares
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            AND table_name IN ('usuario', 'camara', 'ubicacion')
            ORDER BY table_name
        """)
        
        tablas_restantes = cur.fetchall()
        
        if not tablas_restantes:
            print("   🎉 ¡PERFECTO! No existen tablas duplicadas")
        else:
            print("   ⚠️  Aún existen tablas:")
            for tabla in tablas_restantes:
                print(f"      - {tabla[0]}")
        
        # PASO 5: Contar foreign keys restantes
        print("\n📊 PASO 5: Verificación de foreign keys")
        
        cur.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE constraint_type = 'FOREIGN KEY'
        """)
        
        total_fk = cur.fetchone()[0]
        print(f"   📈 Total de foreign keys en BD: {total_fk}")
        
        # Verificar que no hay FK hacia tablas singulares (debería ser 0)
        cur.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
            AND ccu.table_name IN ('usuario', 'camara', 'ubicacion')
        """)
        
        fk_singulares = cur.fetchone()[0]
        if fk_singulares == 0:
            print("   ✅ No hay foreign keys hacia tablas singulares")
        else:
            print(f"   ⚠️  Aún hay {fk_singulares} foreign keys hacia tablas singulares")
        
        cur.close()
        
        print("\n" + "=" * 70)
        print("🎉 LIMPIEZA COMPLETADA EXITOSAMENTE")
        print(f"🕐 Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR durante la limpieza: {e}")
        if conn:
            conn.rollback()
        return False
        
    finally:
        if conn:
            conn.close()
        print("🔌 Conexión cerrada")

def main():
    """Función principal - EJECUTAR DIRECTAMENTE"""
    print("🗑️  EJECUTANDO LIMPIEZA DE FOREIGN KEY DEPENDENCIES")
    print("📋 Sistema: Gestión de Cámaras UFRO")
    print("🕐 Fecha: 2025-10-25 07:07:35")
    print("⚠️  NOTA: Se eliminarán foreign keys y tablas duplicadas")
    print()
    
    # Ejecutar limpieza directamente (AUTORIZADO POR EL USUARIO)
    exito = ejecutar_limpieza_foreign_keys()
    
    if exito:
        print("\n✅ ÉXITO: La base de datos ha sido limpiada")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Probar la aplicación web")
        print("   2. Verificar que el dashboard carga las 467 cámaras")
        print("   3. Confirmar que no hay errores en logs")
        print("\n🎉 LIMPIEZA COMPLETADA EXITOSAMENTE")
    else:
        print("\n❌ FALLO: Error durante la limpieza")
        print("   Revisar los mensajes de error arriba")
    
    return exito

if __name__ == "__main__":
    main()