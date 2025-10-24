#!/usr/bin/env python3
"""
Ejecutar SQL de usuarios completos en Railway PostgreSQL
Creado: 2025-10-24 22:25:37
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def ejecutar_sql_usuarios():
    """
    Ejecuta el SQL de usuarios completos en Railway PostgreSQL
    """
    try:
        # Obtener DATABASE_URL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ ERROR: DATABASE_URL no encontrado en variables de entorno")
            return False

        print("🔗 Conectando a Railway PostgreSQL...")
        print(f"📍 Host: {database_url.split('@')[1].split(':')[0] if '@' in database_url else 'No disponible'}")
        
        # Conectar a la base de datos
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ Conexión establecida exitosamente")
        
        # Leer el archivo SQL
        with open('SISTEMA_USUARIOS_COMPLETO.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("\n📋 Ejecutando SQL...")
        print("="*60)
        
        # Dividir en comandos individuales
        comandos = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        for i, comando in enumerate(comandos, 1):
            if comando:
                print(f"📝 Ejecutando comando {i}: {comando[:50]}...")
                cursor.execute(comando)
                conn.commit()
                print(f"✅ Comando {i} ejecutado exitosamente")
        
        print("\n🔍 Verificando usuarios creados...")
        cursor.execute("SELECT username, rol, nombre_completo, email, activo FROM usuario ORDER BY rol, username")
        usuarios = cursor.fetchall()
        
        print(f"\n📊 Total de usuarios creados: {len(usuarios)}")
        print("="*60)
        
        for usuario in usuarios:
            print(f"👤 {usuario['username']} ({usuario['rol']}) - {usuario['nombre_completo']}")
            print(f"   📧 {usuario['email']} - {'✅ Activo' if usuario['activo'] else '❌ Inactivo'}")
        
        # Verificar específicamente a Charles
        cursor.execute("SELECT * FROM usuario WHERE username = 'charles.jelvez'")
        charles = cursor.fetchone()
        
        if charles:
            print("\n🎯 VERIFICACIÓN CHARLES JÉLVEZ:")
            print(f"   Username: {charles['username']}")
            print(f"   Rol: {charles['rol']}")
            print(f"   Nombre: {charles['nombre_completo']}")
            print(f"   Email: {charles['email']}")
            print(f"   Hash: {charles['password_hash'][:50]}...")
            print(f"   Activo: {charles['activo']}")
            print("   ✅ Usuario Charles creado correctamente")
        else:
            print("❌ ERROR: Usuario Charles no encontrado")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 SQL ejecutado exitosamente en Railway PostgreSQL")
        return True
        
    except Exception as e:
        print(f"❌ ERROR al ejecutar SQL: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 EJECUTOR SQL USUARIOS - RAILWAY POSTGRESQL")
    print("="*60)
    print(f"⏰ Fecha: 2025-10-24 22:25:37")
    print("="*60)
    
    # Establecer DATABASE_URL desde la variable guardada
    os.environ['DATABASE_URL'] = 'postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway'
    
    resultado = ejecutar_sql_usuarios()
    
    if resultado:
        print("\n✅ ÉXITO: Sistema de usuarios listo para probar login")
        print("🔐 Credenciales de prueba:")
        print("   Usuario: charles.jelvez")
        print("   Contraseña: charles123")
        print("   URL: https://gestion-camaras-ufro.up.railway.app/")
    else:
        print("\n❌ FALLO: Error al ejecutar SQL")