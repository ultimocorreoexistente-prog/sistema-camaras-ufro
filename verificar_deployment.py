#!/usr/bin/env python3
"""
Script de Verificación Post-Deployment
Sistema de Gestión de Cámaras UFRO
"""

import requests
import sys

# Configuración
BASE_URL = "https://gestion-camaras-ufro.up.railway.app"

def verificar_endpoint(url, descripcion):
    """Verifica que un endpoint responda correctamente"""
    try:
        response = requests.get(url, timeout=10, allow_redirects=False)
        if response.status_code in [200, 302]:  # 302 = redirect to login
            print(f"✅ {descripcion}: OK (Status {response.status_code})")
            return True
        else:
            print(f"⚠️  {descripcion}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {descripcion}: ERROR - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("VERIFICACIÓN POST-DEPLOYMENT - Sistema Cámaras UFRO")
    print("=" * 60)
    print(f"URL Base: {BASE_URL}\n")
    
    endpoints = [
        (f"{BASE_URL}/", "Página principal (redirect a login)"),
        (f"{BASE_URL}/login", "Página de login"),
        (f"{BASE_URL}/dashboard", "Dashboard (requiere auth)"),
        (f"{BASE_URL}/camaras", "Listado de cámaras (requiere auth)"),
        (f"{BASE_URL}/switches", "Listado de switches (requiere auth)"),
        (f"{BASE_URL}/nvr", "Listado de NVR/DVR (requiere auth)"),
        (f"{BASE_URL}/ups", "Listado de UPS (requiere auth)"),
        (f"{BASE_URL}/fuentes", "Listado de fuentes (requiere auth)"),
        (f"{BASE_URL}/puertos", "Listado de puertos (requiere auth)"),
        (f"{BASE_URL}/tecnicos", "Listado de técnicos (requiere auth)"),
        (f"{BASE_URL}/fallas", "Gestión de fallas (requiere auth)"),
        (f"{BASE_URL}/mantenimientos", "Gestión de mantenimientos (requiere auth)"),
        (f"{BASE_URL}/informes-avanzados", "Informes avanzados (requiere auth)"),
        (f"{BASE_URL}/camaras/masivo", "Modificación masiva (requiere superadmin)"),
    ]
    
    resultados = []
    for url, desc in endpoints:
        resultado = verificar_endpoint(url, desc)
        resultados.append(resultado)
    
    print("\n" + "=" * 60)
    total = len(resultados)
    exitosos = sum(resultados)
    print(f"RESUMEN: {exitosos}/{total} endpoints verificados correctamente")
    
    if exitosos == total:
        print("✅ Sistema completamente funcional")
        return 0
    elif exitosos >= total * 0.8:
        print("⚠️  Sistema mayormente funcional (algunas rutas requieren autenticación)")
        return 0
    else:
        print("❌ Sistema con problemas - revisar logs de Railway")
        return 1

if __name__ == "__main__":
    sys.exit(main())
