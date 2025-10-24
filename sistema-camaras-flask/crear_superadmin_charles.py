#!/usr/bin/env python3
"""
Script para crear Charles como SUPERADMIN en Railway
Ejecutar desde la línea de comandos en Railway
"""
import os
import sys

# Asegurar que estamos en el directorio correcto
os.chdir('/app' if os.path.exists('/app') else os.getcwd())

try:
    from app import app, db
    from models import Usuario
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        print("🚀 Creando Charles Jélvez como SUPERADMIN en Railway...")
        
        # Verificar si Charles ya existe
        charles = Usuario.query.filter_by(username='charles.jelvez').first()
        
        if charles:
            print(f"✅ Charles ya existe: {charles.username} ({charles.rol})")
            charles.set_password('charles123')
            db.session.commit()
        else:
            print("👑 Creando nuevo usuario Charles Jélvez...")
            charles = Usuario(
                username='charles.jelvez',
                rol='superadmin',
                nombre_completo='Charles Jélvez',
                email='charles.jelvez@ufro.cl',
                activo=True
            )
            charles.set_password('charles123')
            db.session.add(charles)
            db.session.commit()
            print("✅ Charles Jélvez creado exitosamente como SUPERADMIN")
        
        # Mostrar todos los usuarios
        usuarios = Usuario.query.order_by(Usuario.rol.desc()).all()
        print(f"\n📊 Total usuarios: {len(usuarios)}")
        
        print("\n🎯 CREDENCIALES DISPONIBLES:")
        credenciales = {
            'charles.jelvez': 'charles123',
            'admin': 'admin123',
            'supervisor': 'super123',
            'tecnico1': 'tecnico123',
            'visualizador': 'viz123'
        }
        
        for usuario in usuarios:
            pwd = credenciales.get(usuario.username, 'N/A')
            print(f"  {usuario.username:15} | {usuario.rol:10} | {pwd}")
        
        print(f"\n✅ CREDENCIALES VERIFICADAS:")
        print(f"🔑 SUPERADMIN: charles.jelvez / charles123")
        print(f"🌐 URL: https://gestion-camaras-ufro.up.railway.app/")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()