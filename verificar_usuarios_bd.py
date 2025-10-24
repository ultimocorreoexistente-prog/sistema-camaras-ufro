#!/usr/bin/env python3
"""
Verificar el estado real de los usuarios en la base de datos
"""

import psycopg2
import os
from getpass import getpass

def conectar_db():
    """Conectar a la base de datos"""
    try:
        # DATABASE_URL proporcionada
        DATABASE_URL = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
        
        print("🔌 Conectando a la base de datos...")
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conexión exitosa")
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def verificar_usuarios(conn):
    """Verificar todos los usuarios en la base de datos"""
    cursor = conn.cursor()
    
    try:
        # Obtener todos los usuarios
        print("\n📋 === VERIFICANDO USUARIOS EN LA BASE DE DATOS ===\n")
        
        query = "SELECT username, rol, activo, email, nombre_completo, fecha_creacion FROM usuario ORDER BY fecha_creacion DESC;"
        cursor.execute(query)
        usuarios = cursor.fetchall()
        
        print("👥 USUARIOS ENCONTRADOS:")
        print("-" * 80)
        
        if usuarios:
            for usuario in usuarios:
                username, rol, activo, email, nombre_completo, fecha_creacion = usuario
                estado = "✅ ACTIVO" if activo else "❌ INACTIVO"
                print(f"👤 Username: {username}")
                print(f"   Rol: {rol}")
                print(f"   Estado: {estado}")
                print(f"   Email: {email}")
                print(f"   Nombre: {nombre_completo}")
                print(f"   Creado: {fecha_creacion}")
                print("-" * 40)
        else:
            print("❌ NO hay usuarios en la tabla usuario")
            
        # Verificar específicamente Charles
        print("\n🔍 === BÚSQUEDA ESPECÍFICA DE CHARLES ===\n")
        cursor.execute("SELECT * FROM usuario WHERE username ILIKE '%charles%';")
        charles_users = cursor.fetchall()
        
        if charles_users:
            print("✅ CHARLES ENCONTRADO:")
            for charles in charles_users:
                print(f"   {charles}")
        else:
            print("❌ CHARLES NO EXISTE en la base de datos")
            
        # Verificar tabla y estructura
        print("\n🔍 === VERIFICANDO ESTRUCTURA DE LA TABLA ===\n")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'usuario' 
            ORDER BY ordinal_position;
        """)
        estructura = cursor.fetchall()
        
        print("📊 ESTRUCTURA DE LA TABLA 'usuario':")
        for col in estructura:
            nombre, tipo, nullable, default = col
            print(f"   {nombre}: {tipo} (nullable: {nullable}, default: {default})")
            
    except Exception as e:
        print(f"❌ Error consultando usuarios: {e}")
    finally:
        cursor.close()

def main():
    print("🔍 VERIFICADOR DE USUARIOS - GESTIÓN DE CÁMARAS UFRO")
    print("=" * 60)
    
    # Conectar a la base de datos
    conn = conectar_db()
    if not conn:
        return
    
    try:
        verificar_usuarios(conn)
    finally:
        conn.close()
        print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    main()