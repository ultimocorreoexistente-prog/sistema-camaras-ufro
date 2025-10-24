#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para inicializar la base de datos PostgreSQL en Railway"""

import psycopg2
import sys
import os

# DATABASE_URL de Railway
DATABASE_URL = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@postgres.railway.internal:5432/railway"

def main():
    try:
        print("🔄 Intentando conectar a PostgreSQL Railway...")
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        print("✅ Conexión exitosa!\n")
        
        # Leer el script de creación de tablas
        print("📋 Leyendo script de creación de tablas...")
        with open('user_input_files/01_crear_tablas.sql', 'r', encoding='utf-8') as f:
            sql_tablas = f.read()
        
        # Ejecutar script de tablas
        print("📋 Ejecutando script de creación de tablas...")
        cursor = conn.cursor()
        cursor.execute(sql_tablas)
        conn.commit()
        print("✅ Tablas creadas exitosamente!\n")
        
        # Leer el script de usuarios
        print("👥 Leyendo script de inserción de usuarios...")
        with open('user_input_files/02_insertar_usuarios.sql', 'r', encoding='utf-8') as f:
            sql_usuarios = f.read()
        
        # Ejecutar script de usuarios
        print("👥 Ejecutando script de inserción de usuarios...")
        cursor.execute(sql_usuarios)
        conn.commit()
        print("✅ Usuarios insertados exitosamente!\n")
        
        # Verificar tablas creadas
        print("📊 Verificando tablas creadas...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tablas = cursor.fetchall()
        print(f"\n✅ Total de tablas creadas: {len(tablas)}")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
        
        # Verificar usuarios
        print("\n👥 Verificando usuarios creados...")
        cursor.execute("SELECT username, rol, nombre_completo FROM usuario ORDER BY id;")
        usuarios = cursor.fetchall()
        print(f"\n✅ Total de usuarios creados: {len(usuarios)}")
        for user in usuarios:
            print(f"  - {user[0]} ({user[1]}) - {user[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("🎉 ¡BASE DE DATOS INICIALIZADA CORRECTAMENTE!")
        print("="*60)
        print("\n📌 Credenciales de acceso:")
        print("  - admin / admin123 (Administrador)")
        print("  - supervisor / super123 (Supervisor)")
        print("  - tecnico1 / tecnico123 (Técnico)")
        print("  - visualizador / viz123 (Visualizador)")
        print("\n⚠️  IMPORTANTE: Cambia estas contraseñas después del primer login")
        
        return 0
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 La dirección 'postgres.railway.internal' es una red privada de Railway.")
        print("   Para conectarme desde aquí, necesito la URL de conexión PÚBLICA.")
        print("\n📝 Alternativas:")
        print("   1. Proporcionarme la URL pública (tramway.proxy.rlwy.net:PUERTO)")
        print("   2. Ejecutar los scripts SQL manualmente desde Railway Query Editor")
        print("   3. Usar Railway CLI desde tu computadora")
        return 1
        
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        print("\n💡 Asegúrate de ejecutar este script desde /workspace")
        return 1
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
