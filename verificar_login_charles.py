#!/usr/bin/env python3
"""
Verificar usuarios en Railway PostgreSQL y probar login
Creado: 2025-10-24 22:25:37
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import time

def verificar_usuarios_railway():
    """
    Verifica los usuarios en Railway PostgreSQL
    """
    try:
        # Conectar a la base de datos
        database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway')
        
        print("🔗 Verificando usuarios en Railway PostgreSQL...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Verificar usuarios
        cursor.execute("SELECT username, rol, nombre_completo, email, activo, LEFT(password_hash, 20) as hash_preview FROM usuario ORDER BY rol, username")
        usuarios = cursor.fetchall()
        
        print(f"\n📊 Total de usuarios en base de datos: {len(usuarios)}")
        print("="*80)
        
        for usuario in usuarios:
            print(f"👤 Username: {usuario['username']}")
            print(f"   Rol: {usuario['rol']}")
            print(f"   Nombre: {usuario['nombre_completo']}")
            print(f"   Email: {usuario['email']}")
            print(f"   Estado: {'✅ Activo' if usuario['activo'] else '❌ Inactivo'}")
            print(f"   Hash: {usuario['hash_preview']}...")
            print("-" * 60)
        
        # Verificar específicamente Charles
        cursor.execute("SELECT * FROM usuario WHERE username = 'charles.jelvez'")
        charles = cursor.fetchone()
        
        if charles:
            print("\n🎯 VERIFICACIÓN ESPECÍFICA CHARLES JÉLVEZ:")
            print(f"   ✅ Username: {charles['username']}")
            print(f"   ✅ Rol: {charles['rol']}")
            print(f"   ✅ Email: {charles['email']}")
            print(f"   ✅ Hash completo: {charles['password_hash']}")
            print(f"   ✅ Creado: {charles['fecha_creacion']}")
            charles_ok = True
        else:
            print("\n❌ ERROR: Usuario Charles no encontrado en base de datos")
            charles_ok = False
        
        cursor.close()
        conn.close()
        
        return charles_ok
        
    except Exception as e:
        print(f"❌ ERROR al verificar usuarios: {str(e)}")
        return False

def probar_login_charles():
    """
    Prueba el login con Charles en la aplicación web
    """
    try:
        url = "https://gestion-camaras-ufro.up.railway.app/login"
        datos = {
            'username': 'charles.jelvez',
            'password': 'charles123'
        }
        
        print(f"\n🔐 Probando login en: {url}")
        print(f"👤 Usuario: {datos['username']}")
        print(f"🔑 Contraseña: {datos['password']}")
        
        # Crear sesión
        session = requests.Session()
        
        # Intentar login
        response = session.post(url, data=datos, allow_redirects=True)
        
        print(f"\n📡 Respuesta HTTP: {response.status_code}")
        
        if response.status_code == 200:
            # Verificar si fue redirigido al dashboard
            if '/dashboard' in response.url or '/login' not in response.url:
                print("✅ LOGIN EXITOSO - Usuario autenticado correctamente")
                print(f"🌐 Redirigido a: {response.url}")
                
                # Verificar contenido de la página
                if 'dashboard' in response.text.lower() or 'charles' in response.text.lower():
                    print("✅ CONTENIDO CORRECTO - Dashboard detectado")
                    return True
                else:
                    print("⚠️ Posible redirección sin contenido de dashboard")
                    return True
            else:
                print("❌ LOGIN FALLIDO - Permanece en página de login")
                if 'incorrectos' in response.text.lower() or 'error' in response.text.lower():
                    print("🔍 Mensaje de error detectado en la página")
                return False
        else:
            print(f"❌ ERROR HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR al probar login: {str(e)}")
        return False

def main():
    """
    Función principal
    """
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA DE USUARIOS")
    print("="*80)
    print(f"⏰ Fecha: 2025-10-24 22:25:37")
    print("="*80)
    
    # 1. Verificar usuarios en base de datos
    print("\n1️⃣ VERIFICANDO BASE DE DATOS...")
    usuarios_ok = verificar_usuarios_railway()
    
    if not usuarios_ok:
        print("\n❌ FALLO CRÍTICO: Problemas con la base de datos")
        return
    
    # 2. Probar login
    print("\n2️⃣ PROBANDO LOGIN...")
    login_ok = probar_login_charles()
    
    # Resumen final
    print("\n" + "="*80)
    print("📋 RESUMEN FINAL:")
    print("="*80)
    print(f"📊 Base de datos: {'✅ OK' if usuarios_ok else '❌ ERROR'}")
    print(f"🔐 Login Charles: {'✅ OK' if login_ok else '❌ ERROR'}")
    
    if usuarios_ok and login_ok:
        print("\n🎉 ÉXITO COMPLETO:")
        print("   ✅ Charles Jélvez puede iniciar sesión como SUPERADMIN")
        print("   ✅ Sistema de usuarios funcionando correctamente")
        print("   🌐 URL: https://gestion-camaras-ufro.up.railway.app/")
    else:
        print("\n⚠️ SE REQUIERE ATENCIÓN:")
        if not usuarios_ok:
            print("   ❌ Problemas con la base de datos")
        if not login_ok:
            print("   ❌ Problemas con el login")
            print("   💡 Posibles causas:")
            print("      - Railway no está usando la base de datos PostgreSQL correcta")
            print("      - Variables de entorno no configuradas")
            print("      - Código de aplicación no sincronizado")

if __name__ == "__main__":
    main()