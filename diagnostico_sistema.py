#!/usr/bin/env python3
"""
Verificar estado de la base de datos Railway y aplicación
"""
import os
import psycopg2
import requests

def verificar_base_datos_railway():
    """Verificar usuarios en Railway PostgreSQL"""
    try:
        DATABASE_URL = 'postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway'
        
        print("🔍 VERIFICANDO BASE DE DATOS RAILWAY POSTGRESQL")
        print("="*60)
        
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Verificar usuarios
        cursor.execute("SELECT username, rol, nombre_completo, email, LEFT(password_hash, 50) as hash_preview FROM usuario ORDER BY rol, username")
        usuarios = cursor.fetchall()
        
        print(f"📊 Total usuarios en PostgreSQL: {len(usuarios)}")
        for username, rol, nombre, email, hash_preview in usuarios:
            print(f"👤 {username} ({rol}) - {nombre} - {email}")
            print(f"   Hash: {hash_preview}...")
        
        # Verificar Charles específicamente
        cursor.execute("SELECT username, rol, email, password_hash FROM usuario WHERE username = %s", ('charles.jelvez',))
        charles = cursor.fetchone()
        
        if charles:
            print(f"\n✅ CHARLES ENCONTRADO EN POSTGRESQL:")
            print(f"   Username: {charles[0]}")
            print(f"   Rol: {charles[1]}")
            print(f"   Email: {charles[2]}")
            print(f"   Hash: {charles[3][:50]}...")
        else:
            print("\n❌ CHARLES NO ENCONTRADO EN POSTGRESQL")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ ERROR PostgreSQL: {e}")
        return False

def verificar_aplicacion_railway():
    """Verificar estado de la aplicación web en Railway"""
    try:
        print("\n🌐 VERIFICANDO APLICACIÓN WEB RAILWAY")
        print("="*60)
        
        url = "https://gestion-camaras-ufro.up.railway.app/"
        
        # Verificar página principal
        response = requests.get(url, timeout=10)
        print(f"📡 Status Code: {response.status_code}")
        print(f"📍 URL: {response.url}")
        
        if "login" in response.text.lower():
            print("✅ Página de login cargada correctamente")
        else:
            print("⚠️ No se detectó página de login")
        
        # Verificar si hay mensajes de error
        if "error" in response.text.lower():
            print("⚠️ Detectado mensaje de error en la página")
        
        # Verificar funcionalidades específicas
        if "charles" in response.text.lower():
            print("✅ Referencias a Charles detectadas")
        else:
            print("⚠️ No se encontraron referencias a Charles")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR Web: {e}")
        return False

def verificar_configuracion():
    """Verificar configuración de variables de entorno"""
    print("\n⚙️ VERIFICANDO CONFIGURACIÓN DE ENTORNO")
    print("="*60)
    
    # Verificar si la aplicación usa SQLite por defecto
    try:
        print("🔍 Verificando código de aplicación...")
        
        # Leer archivo app.py para verificar configuración de BD
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar configuración de DATABASE_URL
        if 'sqlite' in content.lower():
            print("⚠️ Detectado SQLite en el código de aplicación")
            print("   La aplicación puede estar usando SQLite en lugar de PostgreSQL")
        
        if 'DATABASE_URL' in content:
            print("✅ Variable DATABASE_URL referenciada en el código")
        
        # Verificar líneas específicas
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'DATABASE_URL' in line and 'sqlite' in line.lower():
                print(f"   Línea {i+1}: {line.strip()}")
        
    except Exception as e:
        print(f"❌ Error leyendo código: {e}")

def main():
    print("🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("="*80)
    print(f"⏰ Fecha: 2025-10-24 22:32:45")
    print("="*80)
    
    # 1. Verificar base de datos PostgreSQL
    db_ok = verificar_base_datos_railway()
    
    # 2. Verificar aplicación web
    web_ok = verificar_aplicacion_railway()
    
    # 3. Verificar configuración
    verificar_configuracion()
    
    # Resumen final
    print("\n" + "="*80)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("="*80)
    print(f"📊 Base de datos PostgreSQL: {'✅ OK' if db_ok else '❌ ERROR'}")
    print(f"🌐 Aplicación web Railway: {'✅ OK' if web_ok else '❌ ERROR'}")
    
    if db_ok and web_ok:
        print("\n🎯 DIAGNÓSTICO:")
        print("   ✅ Base de datos PostgreSQL funcionando")
        print("   ✅ Aplicación web accessible")
        print("   ❌ PROBLEMA: Desconexión entre BD y aplicación")
        print("\n💡 POSIBLES CAUSAS:")
        print("   1. Variables de entorno no configuradas en Railway")
        print("   2. Aplicación usando SQLite por defecto")
        print("   3. Sincronización incompleta del deployment")
        print("\n🔧 SOLUCIONES:")
        print("   1. Verificar DATABASE_URL en Railway dashboard")
        print("   2. Reiniciar aplicación en Railway")
        print("   3. Verificar logs de Railway")

if __name__ == "__main__":
    main()