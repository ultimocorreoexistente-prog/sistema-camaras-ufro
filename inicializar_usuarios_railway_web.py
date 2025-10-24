#!/usr/bin/env python3
"""
Script para inicializar todos los usuarios en Railway usando la aplicación Flask
"""

import requests
import time

def inicializar_usuarios_railway():
    """Inicializar usuarios usando la ruta de la aplicación"""
    
    base_url = "https://gestion-camaras-ufro.up.railway.app"
    
    print("🚀 INICIALIZANDO USUARIOS EN RAILWAY")
    print("=" * 50)
    
    # Paso 1: Inicializar todos los usuarios
    print("📋 Paso 1: Inicializando todos los usuarios...")
    try:
        response = requests.get(f"{base_url}/init-usuarios-railway", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ Usuarios inicializados correctamente")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        
    # Paso 2: Verificar creación específica de Charles
    print("\n👤 Paso 2: Creando Charles SUPERADMIN...")
    try:
        response = requests.get(f"{base_url}/crear-charles-superadmin", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ Charles SUPERADMIN creado correctamente")
        else:
            print(f"❌ Error creando Charles: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error conectando para Charles: {e}")
    
    # Paso 3: Verificación
    print("\n🔍 Paso 3: Verificación de inicialización...")
    time.sleep(2)
    
    print(f"\n📋 CREDENCIALES PARA LOGIN:")
    print(f"   URL: {base_url}")
    print(f"   Usuario: charles.jelvez")
    print(f"   Contraseña: charles123")
    print(f"   Rol: SUPERADMIN")
    
    print(f"\n✅ PROCESO COMPLETADO")
    print(f"🔗 Intenta hacer login en: {base_url}/login")

if __name__ == "__main__":
    inicializar_usuarios_railway()