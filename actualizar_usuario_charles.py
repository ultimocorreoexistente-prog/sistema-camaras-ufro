#!/usr/bin/env python3
"""
Script para agregar Charles Jélvez como SUPERADMIN al Sistema de Cámaras UFRO
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

def crear_usuario_charles_jelvez():
    """Crea el usuario Charles Jélvez como SUPERADMIN"""
    
    with app.app_context():
        # Verificar si Charles Jélvez ya existe
        charles = Usuario.query.filter_by(email='charles.jelvez@ufro.cl').first()
        
        if charles:
            print("✅ Charles Jélvez ya existe en el sistema")
            print(f"   Rol actual: {charles.rol}")
            print(f"   Estado: {'Activo' if charles.activo else 'Inactivo'}")
            return charles
        
        # Crear nuevo usuario SUPERADMIN
        charles = Usuario(
            email='charles.jelvez@ufro.cl',
            rol='superadmin',
            nombre='Charles Jélvez',
            activo=True
        )
        charles.set_password('charles123')
        
        db.session.add(charles)
        db.session.commit()
        
        print("✅ Charles Jélvez creado exitosamente como SUPERADMIN")
        print(f"   Email: {charles.email}")
        print(f"   Rol: {charles.rol}")
        return charles

def listar_todos_usuarios():
    """Lista todos los usuarios del sistema"""
    
    with app.app_context():
        usuarios = Usuario.query.order_by(Usuario.rol.desc(), Usuario.email).all()
        
        print("\n👥 USUARIOS DEL SISTEMA:")
        print("=" * 60)
        
        for usuario in usuarios:
            estado = "✅ Activo" if usuario.activo else "❌ Inactivo"
            print(f"{usuario.id:2d}. {usuario.email:20s} | {usuario.rol:12s} | {estado}")
        
        print(f"\nTotal usuarios: {len(usuarios)}")
        
        # Contar por rol
        roles_count = {}
        for usuario in usuarios:
            if usuario.activo:
                roles_count[usuario.rol] = roles_count.get(usuario.rol, 0) + 1
        
        print("\n📊 DISTRIBUCIÓN POR ROL (Solo activos):")
        for rol, count in sorted(roles_count.items(), key=lambda x: x[1], reverse=True):
            print(f"   {rol:12s}: {count} usuario(s)")

def main():
    print("🔧 ACTUALIZACIÓN DE USUARIOS - SISTEMA CÁMARAS UFRO")
    print("=" * 60)
    
    try:
        # Listar usuarios actuales
        listar_todos_usuarios()
        
        # Crear Charles Jélvez
        charles = crear_usuario_charles_jelvez()
        
        # Listar usuarios actualizados
        listar_todos_usuarios()
        
        print("\n🎉 PROCESO COMPLETADO EXITOSAMENTE")
        print(f"\n🔑 CREDENCIALES DE CHARLES JÉLVEZ:")
        print(f"   Email: {charles.email}")
        print(f"   Contraseña: charles123")
        print(f"   Rol: {charles.rol.upper()}")
        print(f"\n🌐 Sistema disponible en: https://gestion-camaras-ufro.up.railway.app/")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()