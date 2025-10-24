#!/usr/bin/env python3
"""
Script para crear Charles Jélvez como SUPERADMIN en Railway PostgreSQL
Proyecto: Sistema de Cámaras UFRO
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
    
    try:
        # Obtener DATABASE_URL desde las variables de entorno
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ Error: DATABASE_URL no está definida en las variables de entorno")
            return False
        
        print(f"✅ DATABASE_URL encontrada (primeros 50 caracteres): {database_url[:50]}...")
        
        # Conectar a la base de datos
        print("\n🔌 Conectando a la base de datos Railway PostgreSQL...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Leer el archivo SQL
        sql_file_path = Path(__file__).parent / "SQL_CHARLES_SUPERADMIN.sql"
        if not sql_file_path.exists():
            print(f"❌ Error: No se encontró el archivo SQL: {sql_file_path}")
            return False
            
        print(f"📖 Leyendo archivo SQL: {sql_file_path}")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("\n⚡ Ejecutando SQL para crear Charles como SUPERADMIN...")
        
        # Ejecutar cada sentencia SQL por separado
        sql_statements = sql_content.split(';')
        statements_executed = 0
        
        for statement in sql_statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    statements_executed += 1
                    print(f"   ✅ Sentencia ejecutada exitosamente")
                except psycopg2.Error as e:
                    print(f"   ❌ Error en sentencia SQL: {e}")
                    print(f"   Sentencia: {statement[:100]}...")
        
        # Confirmar cambios
        print(f"\n✅ {statements_executed} sentencias SQL ejecutadas")
        conn.commit()
        
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
        else:
            print("❌ Error: No se pudo verificar la creación del usuario")
            return False
            
        # Cerrar conexión
        cursor.close()
        conn.close()
        
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