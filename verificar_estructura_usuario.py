#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla usuario en Railway PostgreSQL
Autor: MiniMax Agent
"""

import psycopg2

# URL EXTERNA de Railway PostgreSQL
database_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"

try:
    print("🔌 Conectando a Railway PostgreSQL...")
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    print("✅ Conexión establecida")
    
    # Verificar estructura de la tabla usuario
    print("\n📋 Verificando estructura de la tabla 'usuario'...")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'usuario' 
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    
    print("\n📊 COLUMNAS DE LA TABLA 'usuario':")
    print("=" * 50)
    for column in columns:
        col_name, data_type, nullable, default = column
        nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
        default_str = f"DEFAULT: {default}" if default else "Sin default"
        print(f"  {col_name:20} | {data_type:15} | {nullable_str:10} | {default_str}")
    
    print("\n" + "=" * 50)
    
    # Verificar si Charles ya existe
    print("\n🔍 Verificando si Charles ya existe...")
    cursor.execute("SELECT username, rol, activo, email, nombre_completo FROM usuario WHERE username = 'charles.jelvez';")
    result = cursor.fetchone()
    
    if result:
        username, rol, activo, email, nombre_completo = result
        print("✅ Charles ya existe:")
        print(f"   Username: {username}")
        print(f"   Rol: {rol}")
        print(f"   Activo: {activo}")
        print(f"   Email: {email}")
        print(f"   Nombre: {nombre_completo}")
    else:
        print("ℹ️  Charles no existe en la base de datos")
    
    cursor.close()
    conn.close()
    print("\n✅ Verificación completada")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Detalles: {e}")