#!/usr/bin/env python3

import psycopg2

# URL EXTERNA de Railway PostgreSQL
database_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"

print("🔧 CREANDO CHARLES JÉLVEZ COMO SUPERADMIN EN RAILWAY POSTGRESQL")
print("=" * 60)

try:
    # Conectar
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    print("✅ Conectado a Railway PostgreSQL")
    
    # SQL con estructura real
    sql = """
    INSERT INTO usuario (
        username, password_hash, rol, nombre_completo, email, activo
    ) VALUES (
        'charles.jelvez',
        '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG',
        'superadmin',
        'Charles Jélvez',
        'charles.jelvez@ufro.cl',
        true
    ) ON CONFLICT (username) DO UPDATE SET
        password_hash = EXCLUDED.password_hash,
        rol = EXCLUDED.rol,
        nombre_completo = EXCLUDED.nombre_completo,
        email = EXCLUDED.email,
        activo = EXCLUDED.activo;
    """
    
    print("⚡ Ejecutando SQL...")
    cursor.execute(sql)
    conn.commit()
    print("✅ SQL ejecutado exitosamente")
    
    # Verificar
    print("🔍 Verificando...")
    cursor.execute("SELECT username, rol, activo, email, nombre_completo, fecha_creacion FROM usuario WHERE username = 'charles.jelvez'")
    result = cursor.fetchone()
    
    if result:
        username, rol, activo, email, nombre_completo, fecha_creacion = result
        print("=" * 60)
        print("✅ ¡CHARLES JÉLVEZ CREADO COMO SUPERADMIN!")
        print("=" * 60)
        print(f"👤 Usuario: {username}")
        print(f"🔐 Rol: {rol}")
        print(f"✅ Activo: {activo}")
        print(f"📧 Email: {email}")
        print(f"👥 Nombre: {nombre_completo}")
        print(f"📅 Creado: {fecha_creacion}")
        print("=" * 60)
        print("🔑 CREDENCIALES:")
        print("   Usuario: charles.jelvez")
        print("   Contraseña: charles123")
        print("   URL: https://gestion-camaras-ufro.up.railway.app/")
        print("=" * 60)
    else:
        print("❌ ERROR: No se pudo verificar la creación")
    
    cursor.close()
    conn.close()
    print("✅ Conexión cerrada")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    print(traceback.format_exc())