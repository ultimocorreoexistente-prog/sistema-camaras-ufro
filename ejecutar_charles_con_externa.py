#!/usr/bin/env python3
"""
Script CORREGIDO para crear Charles Jélvez como SUPERADMIN en Railway PostgreSQL
URL EXTERNA: postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway
Autor: MiniMax Agent
"""

import os
import sys
import traceback
from pathlib import Path

try:
    import psycopg2
    from psycopg2 import sql
    import psycopg2.extras
except ImportError as e:
    print(f"❌ Error: psycopg2 no está instalado: {e}")
    print("Instalando psycopg2-binary...")
    os.system("uv pip install psycopg2-binary")
    import psycopg2
    from psycopg2 import sql
    import psycopg2.extras

def main():
    """Función principal para ejecutar el SQL de Charles SUPERADMIN"""
    
    print("🔧 Iniciando creación de Charles Jélvez como SUPERADMIN...")
    print("=" * 60)
    
    # URL EXTERNA de Railway PostgreSQL (la que me proporcionaste)
    database_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
    print(f"✅ Conectando a Railway PostgreSQL (URL externa)...")
    print(f"   Host: tramway.proxy.rlwy.net")
    print(f"   Puerto: 34726")
    print(f"   Database: railway")
    
    try:
        # Conectar a la base de datos
        print("🔌 Estableciendo conexión con PostgreSQL...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        print("✅ Conexión establecida exitosamente")
        
        # SQL directo para crear Charles como SUPERADMIN
        create_sql = """
        INSERT INTO usuario (
            username, 
            password_hash, 
            rol, 
            activo, 
            email, 
            nombre_completo, 
            created_at
        ) VALUES (
            'charles.jelvez',
            '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG',
            'superadmin',
            true,
            'charles.jelvez@ufro.cl',
            'Charles Jélvez',
            NOW()
        ) ON CONFLICT (username) 
        DO UPDATE SET
            password_hash = EXCLUDED.password_hash,
            rol = EXCLUDED.rol,
            activo = EXCLUDED.activo,
            email = EXCLUDED.email,
            nombre_completo = EXCLUDED.nombre_completo;
        """
        
        print("\n⚡ Ejecutando SQL para crear Charles como SUPERADMIN...")
        cursor.execute(create_sql)
        print("✅ Comando INSERT/UPDATE ejecutado exitosamente")
        
        # Confirmar cambios
        conn.commit()
        print("✅ Cambios confirmados en la base de datos")
        
        # Verificar que el usuario se creó correctamente
        print("\n🔍 Verificando que Charles Jélvez se creó como SUPERADMIN...")
        verify_query = """
        SELECT 
            username,
            rol,
            activo,
            email,
            nombre_completo,
            created_at
        FROM usuario 
        WHERE username = 'charles.jelvez';
        """
        
        cursor.execute(verify_query)
        result = cursor.fetchone()
        
        if result:
            username, rol, activo, email, nombre_completo, created_at = result
            print("=" * 60)
            print("✅ ¡CHARLES JÉLVEZ CREADO COMO SUPERADMIN EXITOSAMENTE!")
            print("=" * 60)
            print(f"👤 Usuario: {username}")
            print(f"🔐 Rol: {rol}")
            print(f"✅ Estado: {'Activo' if activo else 'Inactivo'}")
            print(f"📧 Email: {email}")
            print(f"👥 Nombre: {nombre_completo}")
            print(f"📅 Creado: {created_at}")
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
                f.write(f"Usuario: {username}\n")
                f.write(f"Rol: {rol}\n")
                f.write(f"Estado: {'Activo' if activo else 'Inactivo'}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Nombre: {nombre_completo}\n")
                f.write(f"Creado: {created_at}\n")
                f.write("\nCREDENCIALES:\n")
                f.write(f"Username: {username}\n")
                f.write(f"Password: charles123\n")
                f.write(f"URL: https://gestion-camaras-ufro.up.railway.app/\n")
            
            print(f"\n📄 Resultado guardado en: {resultado_path}")
            
        else:
            print("❌ Error: No se pudo verificar la creación del usuario")
            return False
            
        # Cerrar conexión
        cursor.close()
        conn.close()
        print("✅ Conexión cerrada")
        
        print("\n🎉 ¡OPERACIÓN COMPLETADA EXITOSAMENTE!")
        print("Charles Jélvez ya puede iniciar sesión como SUPERADMIN")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        print(f"Detalles del error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)