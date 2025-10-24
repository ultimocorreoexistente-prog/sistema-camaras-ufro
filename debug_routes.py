#!/usr/bin/env python3
"""
Script de debug para verificar las rutas disponibles en la aplicación
Este script lista todas las rutas registradas en Flask para diagnosticar el problema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar la app
from app import app

def debug_routes():
    """Lista todas las rutas registradas en la aplicación Flask"""
    print("=== DEBUG DE RUTAS FLASK ===")
    print(f"Nombre de la app: {app.name}")
    print(f"Configuración: {app.config.get('ENV', 'No configurado')}")
    print("\n📋 RUTAS REGISTRADAS:")
    print("-" * 60)
    
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    
    # Ordenar por endpoint
    routes.sort(key=lambda x: x['endpoint'])
    
    for i, route in enumerate(routes, 1):
        print(f"{i:2d}. {route['rule']}")
        print(f"    Endpoint: {route['endpoint']}")
        print(f"    Métodos: {', '.join(sorted(route['methods']))}")
        print()
    
    print("🔍 BÚSQUEDA DE RUTAS ESPECÍFICAS:")
    print("-" * 40)
    
    target_routes = ['crear-charles-superadmin', 'init-usuarios-railway', 'init_db']
    for target in target_routes:
        found = False
        for route in routes:
            if target in route['endpoint'] or target in route['rule']:
                print(f"✅ ENCONTRADA: {target}")
                print(f"   - Endpoint: {route['endpoint']}")
                print(f"   - URL: {route['rule']}")
                print(f"   - Métodos: {', '.join(route['methods'])}")
                found = True
                break
        if not found:
            print(f"❌ NO ENCONTRADA: {target}")
        print()

if __name__ == "__main__":
    debug_routes()