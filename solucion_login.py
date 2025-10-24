#!/usr/bin/env python3
"""
Script para crear trigger de reinicio en Railway
y forzar uso de PostgreSQL
"""
import os
import requests
import json

def create_restart_trigger():
    """Crear trigger para reiniciar Railway"""
    
    # Crear archivo de trigger que force reinicio
    with open('.railway_rebuild_trigger', 'w') as f:
        f.write(f'Reinicio manual: {os.path.basename(__file__)} - {os.getcwd()}\n')
    
    # Crear archivo de configuración para Railway
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python app.py",
            "healthcheckPath": "/",
            "healthcheckTimeout": 100,
            "restartPolicyType": "ON_FAILURE"
        },
        "variables": {
            "DATABASE_URL": "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway",
            "SECRET_KEY": "railway-production-secret-key-2025",
            "FLASK_ENV": "production"
        }
    }
    
    with open('railway.json', 'w') as f:
        json.dump(railway_config, f, indent=2)
    
    print("🔧 Trigger de reinicio creado en Railway")
    print("✅ Variables de entorno configuradas:")
    print("   DATABASE_URL: PostgreSQL Railway")
    print("   SECRET_KEY: Configurada para producción")
    print("   FLASK_ENV: production")
    
    return True

def add_debug_info():
    """Agregar información de debug al app.py"""
    
    # Leer app.py actual
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar logging después de la configuración de base de datos
    debug_code = '''
# Debug: Información de base de datos
print(f"🔧 DEBUG: DATABASE_URL = {os.environ.get('DATABASE_URL', 'NO DEFINIDO')}")
print(f"🔧 DEBUG: SQLALCHEMY_DATABASE_URI = {app.config.get('SQLALCHEMY_DATABASE_URI', 'NO CONFIGURADO')}")
print(f"🔧 DEBUG: Usando SQLite = {'sqlite' in app.config.get('SQLALCHEMY_DATABASE_URI', '').lower()}")

# Logging del usuario Charles si existe
try:
    charles_check = Usuario.query.filter_by(username='charles.jelvez').first()
    if charles_check:
        print(f"✅ Charles encontrado en BD: {charles_check.username} ({charles_check.rol})")
    else:
        print("❌ Charles NO encontrado en BD")
        total_users = Usuario.query.count()
        print(f"📊 Total usuarios en BD: {total_users}")
except Exception as e:
    print(f"❌ Error verificando usuarios: {e}")

'''
    
    # Insertar después de db.init_app(app)
    insertion_point = 'db.init_app(app)'
    new_content = content.replace(insertion_point, insertion_point + debug_code)
    
    # Escribir versión de debug
    with open('app_debug.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("🗺️ Archivo de debug creado: app_debug.py")
    print("   Incluye logging de base de datos y verificación de Charles")
    
    return True

def main():
    print("🔧 CONFIGURACIÓN PARA RESOLVER PROBLEMA DE LOGIN")
    print("="*60)
    print("Problema identificado: Railway usa SQLite en lugar de PostgreSQL")
    print("Charles existe en PostgreSQL pero la app no lo puede ver")
    print("="*60)
    
    # 1. Crear trigger de reinicio
    print("\n1️⃣ Creando trigger de reinicio...")
    create_restart_trigger()
    
    # 2. Agregar información de debug
    print("\n2️⃣ Agregando información de debug...")
    add_debug_info()
    
    # 3. Crear mensaje final
    print("\n3️⃣ CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print("✅ Archivos creados:")
    print("   - .railway_rebuild_trigger (fuerza reinicio)")
    print("   - railway.json (configuración de variables)")
    print("   - app_debug.py (versión con debug)")
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Hacer commit y push de estos cambios")
    print("2. Railway se reiniciará automáticamente")
    print("3. Verificar logs de Railway para confirmar PostgreSQL")
    print("4. Probar login con charles.jelvez / charles123")
    
    print("\n💡 SI EL PROBLEMA PERSISTE:")
    print("- Verificar dashboard de Railway manualmente")
    print("- Confirmar variable DATABASE_URL en Railway dashboard")
    print("- Revisar logs de Railway para errores")

if __name__ == "__main__":
    main()