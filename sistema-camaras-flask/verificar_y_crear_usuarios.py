#!/usr/bin/env python3
"""
Script para verificar y crear usuarios en Railway
Incluye Charles Jélvez como SUPERADMIN
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.getcwd())

from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

def verificar_y_crear_usuarios():
    """Verifica y crea usuarios, incluyendo Charles como SUPERADMIN"""
    
    with app.app_context():
        print("🔍 Verificando estado actual de usuarios...")
        
        # Mostrar usuarios existentes
        usuarios_existentes = Usuario.query.all()
        print(f"Usuarios actuales en la BD: {len(usuarios_existentes)}")
        
        for usuario in usuarios_existentes:
            print(f"  - {usuario.username} ({usuario.rol}) - {'✅' if usuario.activo else '❌'}")
        
        # Crear Charles como SUPERADMIN si no existe
        charles = Usuario.query.filter_by(username='charles.jelvez').first()
        
        if not charles:
            print("\n👑 Creando Charles Jélvez como SUPERADMIN...")
            charles = Usuario(
                username='charles.jelvez',
                rol='superadmin',
                nombre_completo='Charles Jélvez',
                email='charles.jelvez@ufro.cl',
                activo=True
            )
            charles.set_password('charles123')
            db.session.add(charles)
            print("✅ Charles Jélvez creado exitosamente")
        else:
            print(f"\n✅ Charles ya existe: {charles.username} ({charles.rol})")
            # Asegurar que tiene la contraseña correcta
            charles.set_password('charles123')
        
        # Crear otros usuarios si no existen
        usuarios_default = [
            ('admin', 'admin123', 'admin', 'Administrador'),
            ('supervisor', 'super123', 'supervisor', 'Supervisor'),
            ('tecnico1', 'tecnico123', 'tecnico', 'Técnico 1'),
            ('visualizador', 'viz123', 'visualizador', 'Visualizador')
        ]
        
        for username, password, rol, nombre in usuarios_default:
            usuario = Usuario.query.filter_by(username=username).first()
            
            if not usuario:
                print(f"➕ Creando {username} ({rol})...")
                usuario = Usuario(
                    username=username,
                    rol=rol,
                    nombre_completo=nombre,
                    email=f'{username}@ufro.cl',
                    activo=True
                )
                usuario.set_password(password)
                db.session.add(usuario)
                print(f"✅ {username} creado")
            else:
                print(f"✅ {username} ya existe")
                # Asegurar que tiene la contraseña correcta
                usuario.set_password(password)
        
        # Confirmar cambios
        db.session.commit()
        
        print("\n📊 RESUMEN FINAL:")
        usuarios_finales = Usuario.query.order_by(Usuario.rol.desc()).all()
        print("Usuarios configurados:")
        
        for usuario in usuarios_finales:
            print(f"  👤 {usuario.username:12} | {usuario.rol:10} | {usuario.nombre_completo:15} | {'✅' if usuario.activo else '❌'}")
        
        print(f"\n🎯 CREDENCIALES VERIFICADAS:")
        print("  SUPERADMIN: charles.jelvez / charles123")
        print("  ADMIN: admin / admin123")
        print("  SUPERVISOR: supervisor / super123")
        print("  TÉCNICO: tecnico1 / tecnico123")
        print("  VISUALIZADOR: visualizador / viz123")

if __name__ == '__main__':
    verificar_y_crear_usuarios()