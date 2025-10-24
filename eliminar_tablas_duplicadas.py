#!/usr/bin/env python3
"""
Script para eliminar tablas duplicadas en Railway PostgreSQL
Tablas a eliminar: usuario (singular), camara (singular), ubicacion (singular)
Mantenemos: usuarios (plural), camaras (plural), ubicaciones (plural) - con datos reales
"""

import os
import psycopg2
from urllib.parse import urlparse

def conectar_bd():
    """Conectar a la base de datos Railway PostgreSQL"""
    # Obtener DATABASE_URL del entorno
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        # URL hardcodeada de la memoria
        db_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
    
    # Parsear la URL
    parsed = urlparse(db_url)
    
    return psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password
    )

def verificar_tablas():
    """Verificar qué tablas existen"""
    print("🔍 VERIFICANDO TABLAS EXISTENTES...")
    
    conn = conectar_bd()
    cur = conn.cursor()
    
    # Listar todas las tablas
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    
    tablas = [row[0] for row in cur.fetchall()]
    print(f"📋 Total de tablas encontradas: {len(tablas)}")
    
    # Categorizar tablas
    usuario_tablas = [t for t in tablas if 'usuario' in t.lower()]
    camara_tablas = [t for t in tablas if 'camara' in t.lower()]
    ubicacion_tablas = [t for t in tablas if 'ubicacion' in t.lower() and 'ubicacion' not in t.lower() and 'ubicacion' not in t.lower()]
    
    print("\n📊 CATEGORIZACIÓN DE TABLAS:")
    print(f"👥 Tablas de usuarios: {usuario_tablas}")
    print(f"📹 Tablas de cámaras: {camara_tablas}")
    print(f"📍 Tablas de ubicaciones: {ubicacion_tablas}")
    
    cur.close()
    conn.close()
    
    return tablas, usuario_tablas, camara_tablas, ubicacion_tablas

def contar_registros(tabla):
    """Contar registros en una tabla"""
    conn = conectar_bd()
    cur = conn.cursor()
    
    try:
        cur.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cur.fetchone()[0]
        return count
    except Exception as e:
        print(f"❌ Error contando registros en {tabla}: {e}")
        return 0
    finally:
        cur.close()
        conn.close()

def verificar_dependencias(tabla):
    """Verificar si una tabla tiene dependencias (foreign keys)"""
    conn = conectar_bd()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT DISTINCT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND ccu.table_name = %s
        """, (tabla,))
        
        dependencias = cur.fetchall()
        return dependencias
    except Exception as e:
        print(f"❌ Error verificando dependencias para {tabla}: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def eliminar_tablas_duplicadas():
    """Eliminar tablas duplicadas en Railway PostgreSQL"""
    print("🗑️  INICIANDO ELIMINACIÓN DE TABLAS DUPLICADAS...")
    
    tablas, usuario_tablas, camara_tablas, ubicacion_tablas = verificar_tablas()
    
    # Definir qué tablas eliminar y cuáles mantener
    tablas_eliminar = {
        'usuario': 'Usar usuarios (plural) - datos reales',
        'camara': 'Usar camaras (plural) - datos reales', 
        'ubicacion': 'Usar ubicaciones (plural) - datos reales'
    }
    
    print(f"\n🎯 PLAN DE LIMPIEZA:")
    for tabla_singular, razon in tablas_eliminar.items():
        print(f"   ❌ {tabla_singular} → {razon}")
    
    exitos = []
    fallidos = []
    
    # Procesar cada tabla singular
    for tabla_singular, razon in tablas_eliminar.items():
        if tabla_singular in tablas:
            print(f"\n🗑️  PROCESANDO: {tabla_singular}")
            
            # Contar registros
            registros = contar_registros(tabla_singular)
            print(f"   📊 Registros actuales: {registros}")
            
            # Verificar dependencias
            dependencias = verificar_dependencias(tabla_singular)
            
            if dependencias:
                print(f"   ⚠️  DEPENDENCIAS ENCONTRADAS:")
                for dep in dependencias:
                    print(f"      - {dep[1]}.{dep[2]} → {dep[3]}")
                print(f"   ❌ NO SE PUEDE ELIMINAR {tabla_singular} - tiene dependencias")
                fallidos.append(tabla_singular)
                continue
            
            # Intentar eliminar
            conn = conectar_bd()
            cur = conn.cursor()
            
            try:
                print(f"   🔄 Ejecutando DROP TABLE {tabla_singular}...")
                cur.execute(f"DROP TABLE {tabla_singular} CASCADE")
                conn.commit()
                print(f"   ✅ ELIMINADO EXITOSAMENTE: {tabla_singular}")
                exitos.append(tabla_singular)
                
            except Exception as e:
                print(f"   ❌ ERROR eliminando {tabla_singular}: {e}")
                fallidos.append(tabla_singular)
                conn.rollback()
            finally:
                cur.close()
                conn.close()
        else:
            print(f"ℹ️  {tabla_singular} no existe en la base de datos")
    
    # Reporte final
    print(f"\n📋 REPORTE DE LIMPIEZA:")
    print(f"   ✅ Eliminadas exitosamente: {len(exitos)}")
    if exitos:
        for tabla in exitos:
            print(f"      - {tabla}")
    
    print(f"   ❌ No se pudieron eliminar: {len(fallidos)}")
    if fallidos:
        for tabla in fallidos:
            print(f"      - {tabla} (tiene dependencias)")
    
    # Verificar estado final
    print(f"\n🔍 ESTADO FINAL DE TABLAS:")
    tablas_finales, _, _, _ = verificar_tablas()
    
    usuario_finales = [t for t in tablas_finales if 'usuario' in t.lower()]
    camara_finales = [t for t in tablas_finales if 'camara' in t.lower()]
    ubicacion_finales = [t for t in tablas_finales if 'ubicacion' in t.lower()]
    
    print(f"   👥 Usuarios: {usuario_finales}")
    print(f"   📹 Cámaras: {camara_finales}")
    print(f"   📍 Ubicaciones: {ubicacion_finales}")
    
    if len(usuario_finales) <= 1 and len(camara_finales) <= 1 and len(ubicacion_finales) <= 1:
        print(f"\n🎉 LIMPIEZA COMPLETADA - Solo quedan las tablas principales (plural)")
    else:
        print(f"\n⚠️  LIMPIEZA PARCIAL - Aún existen duplicados")

if __name__ == "__main__":
    eliminar_tablas_duplicadas()