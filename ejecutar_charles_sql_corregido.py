#!/usr/bin/env python3
"""
Script CORREGIDO para crear Charles Jélvez como SUPERADMIN en Railway PostgreSQL
Estructura real de tabla usuario verificada:
- id, username, password_hash, rol, nombre_completo, email, telefono, activo, fecha_creacion
Autor: MiniMax Agent
"""

import psycopg2
from pathlib import Path

# URL EXTERNA de Railway PostgreSQL
database_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"

try:
    print("🔧 Iniciando creación de Charles Jélvez como SUPERADMIN...")
    print("=" * 60)
    print("🔌 Conectando a Railway PostgreSQL...")
    
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    print("✅ Conexión establecida")
    
    # SQL CORREGIDO para crear Charles como SUPERADMIN usando estructura real
    create_sql = """
    INSERT INTO usuario (
        username, 
        password_hash, 
        rol, 
        nombre_completo, 
        email, 
        activo
    ) VALUES (
        'charles.jelvez',
        '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG',
        'superadmin',
        'Charles Jélvez',
        'charles.jelvez@ufro.cl',
        true
    ) ON CONFLICT (username) 
    DO UPDATE SET
        password_hash = EXCLUDED.password_hash,
        rol = EXCLUDED.rol,
        nombre_completo = EXCLUDED.nombre_completo,
        email = EXCLUDED.email,
        activo = EXCLUDED.activo;
    """
    
    print("\n⚡ Ejecutando SQL para crear Charles como SUPERADMIN...")
    print("   (usando estructura real de la tabla)")
    
    cursor.execute(create_sql)
    print("✅ Comando INSERT/UPDATE ejecutado exitosamente")
    
    # Confirmar cambios
    conn.commit()
    print("✅ Cambios confirmados en la base de datos")
    
    # Verificar que el usuario se creó correctamente
    print("\n🔍 Verificando que Charles Jélvez se creó como SUPERADMIN...")
    verify_query = """
    SELECT 
        id,
        username,
        rol,
        activo,
        email,
        nombre_completo,
        fecha_creacion
    FROM usuario 
    WHERE username = 'charles.jelvez';
    """
    
    cursor.execute(verify_query)
    result = cursor.fetchone()
    
    if result:
        user_id, username, rol, activo, email, nombre_completo, fecha_creacion = result
        print("=" * 60)
        print("✅ ¡CHARLES JÉLVEZ CREADO COMO SUPERADMIN EXITOSAMENTE!")
        print("=" * 60)
        print(f"🆔 ID: {user_id}")
        print(f"👤 Usuario: {username}")
        print(f"🔐 Rol: {rol}")
        print(f"✅ Estado: {'Activo' if activo else 'Inactivo'}")
        print(f"📧 Email: {email}")
        print(f"👥 Nombre: {nombre_completo}")
        print(f"📅 Creado: {fecha_creacion}")
        print("=" * 60)
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print(f"   Username: {username}")
        print(f"   Password: charles123")
        print(f"   URL: https://gestion-camaras-ufro.up.railway.app/")
        print("=" * 60)
        
        # Guardar resultado en archivo para referencia
        resultado_path = Path(__file__).parent / "CHARLES_CREADO_EXITOSAMENTE.txt"
        with open(resultado_path, 'w', encoding='utf-8') as f:
            f.write("CHARLES JÉLVEZ - SUPERADMIN CREADO EXITOSAMENTE\n")
            f.write("=" * 50 + "\n")
            f.write(f"ID: {user_id}\n")
            f.write(f"Usuario: {username}\n")
            f.write(f"Rol: {rol}\n")
            f.write(f"Estado: {'Activo' if activo else 'Inactivo'}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Nombre: {nombre_completo}\n")
            f.write(f"Creado: {fecha_creacion}\n")
            f.write("\nCREDENCIALES:\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: charles123\n")
            f.write(f"URL: https://gestion-camaras-ufro.up.railway.app/\n")
            f.write("\n✅ CREADO EXITOSAMENTE EN RAILWAY POSTGRESQL\n")
        
        print(f"\n📄 Resultado guardado en: {resultado_path}")
        
    else:
        print("❌ Error: No se pudo verificar la creación del usuario")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        return False
        
    # Cerrar conexión
    cursor.close()
    conn.close()
    print("✅ Conexión cerrada")
    
    print("\n🎉 ¡OPERACIÓN COMPLETADA EXITOSAMENTE!")
    print("Charles Jélvez ya puede iniciar sesión como SUPERADMIN")
    
    # Crear archivo SQL final para referencia
    sql_final_path = Path(__file__).parent / "SQL_CHARLES_EJECUTADO_EXITOSAMENTE.sql"
    with open(sql_final_path, 'w', encoding='utf-8') as f:
        f.write("-- SQL EJECUTADO EXITOSAMENTE PARA CHARLES JÉLVEZ\n")
        f.write("-- Proyecto: Sistema de Cámaras UFRO\n")
        f.write("-- Fecha: 2025-10-24 21:59:00\n")
        f.write("-- Estado: EXITOSO\n")
        f.write("\n")
        f.write("INSERT INTO usuario (\n")
        f.write("    username, \n")
        f.write("    password_hash, \n")
        f.write("    rol, \n")
        f.write("    nombre_completo, \n")
        f.write("    email, \n")
        f.write("    activo\n")
        f.write(") VALUES (\n")
        f.write("    'charles.jelvez',\n")
        f.write("    '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG',\n")
        f.write("    'superadmin',\n")
        f.write("    'Charles Jélvez',\n")
        f.write("    'charles.jelvez@ufro.cl',\n")
        f.write("    true\n")
        f.write(") ON CONFLICT (username) \n")
        f.write("DO UPDATE SET\n")
        f.write("    password_hash = EXCLUDED.password_hash,\n")
        f.write("    rol = EXCLUDED.rol,\n")
        f.write("    nombre_completo = EXCLUDED.nombre_completo,\n")
        f.write("    email = EXCLUDED.email,\n")
        f.write("    activo = EXCLUDED.activo;\n")
    
    print(f"📄 SQL de referencia guardado en: {sql_final_path}")
    
    return True
    
except Exception as e:
    print(f"\n❌ Error durante la ejecución: {e}")
    import traceback
    print(f"Detalles del error: {traceback.format_exc()}")
    return False