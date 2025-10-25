#!/usr/bin/env python3
"""
Script completo para inicializar la base de datos y crear Charles Jélvez
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

def inicializar_base_datos():
    """Inicializa la base de datos y crea las tablas"""
    print("🔧 Inicializando base de datos...")
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        
        # Verificar si ya existen usuarios
        usuarios_existentes = Usuario.query.count()
        print(f"👥 Usuarios existentes: {usuarios_existentes}")
        
        return usuarios_existentes

def crear_usuarios_completos():
    """Crea todos los usuarios del sistema incluyendo Charles Jélvez"""
    
    with app.app_context():
        # Lista de usuarios a crear
        usuarios_data = [
            {
                'email': 'charles.jelvez@ufro.cl',
                'nombre': 'Charles Jélvez',
                'rol': 'superadmin',
                'password': 'charles123'
            },
            {
                'email': 'admin@ufro.cl',
                'nombre': 'Administrador',
                'rol': 'admin',
                'password': 'admin123'
            },
            {
                'email': 'supervisor@ufro.cl',
                'nombre': 'Supervisor',
                'rol': 'supervisor',
                'password': 'super123'
            },
            {
                'email': 'tecnico1@ufro.cl',
                'nombre': 'Técnico 1',
                'rol': 'tecnico',
                'password': 'tecnico123'
            },
            {
                'email': 'visualizador@ufro.cl',
                'nombre': 'Visualizador',
                'rol': 'visualizador',
                'password': 'viz123'
            }
        ]
        
        usuarios_creados = 0
        
        for user_data in usuarios_data:
            # Verificar si el usuario ya existe
            usuario_existente = Usuario.query.filter_by(email=user_data['email']).first()
            
            if usuario_existente:
                print(f"⚠️  {user_data['email']} ya existe ({user_data['rol']})")
                continue
            
            # Crear nuevo usuario
            usuario = Usuario(
                email=user_data['email'],
                nombre=user_data['nombre'],
                rol=user_data['rol'],
                activo=True
            )
            usuario.set_password(user_data['password'])
            
            db.session.add(usuario)
            usuarios_creados += 1
            print(f"✅ Creado: {user_data['email']} ({user_data['rol']})")
        
        # Guardar cambios
        if usuarios_creados > 0:
            db.session.commit()
            print(f"🎉 {usuarios_creados} usuario(s) creado(s) exitosamente")
        else:
            print("📋 Todos los usuarios ya existían")
        
        return usuarios_creados

def listar_usuarios_final():
    """Lista todos los usuarios finales"""
    
    with app.app_context():
        usuarios = Usuario.query.order_by(Usuario.rol.desc(), Usuario.email).all()
        
        print("\n👥 USUARIOS FINALES DEL SISTEMA:")
        print("=" * 60)
        
        for usuario in usuarios:
            estado = "✅ Activo" if usuario.activo else "❌ Inactivo"
            rol_badge = {
                'superadmin': '👑',
                'admin': '🔧',
                'supervisor': '👁️',
                'tecnico': '🔨',
                'visualizador': '👁️‍🗨️'
            }.get(usuario.rol, '❓')
            
            print(f"{usuario.id:2d}. {usuario.email:20s} | {rol_badge} {usuario.rol:12s} | {estado}")
        
        print(f"\nTotal usuarios: {len(usuarios)}")

def main():
    print("🚀 INICIALIZACIÓN COMPLETA - SISTEMA CÁMARAS UFRO")
    print("=" * 60)
    
    try:
        # 1. Inicializar base de datos
        inicializar_base_datos()
        
        # 2. Crear usuarios
        crear_usuarios_completos()
        
        # 3. Listar usuarios finales
        listar_usuarios_final()
        
        print("\n🎉 PROCESO COMPLETADO EXITOSAMENTE")
        print(f"\n🔑 ACCESO SUPERADMIN (Charles Jélvez):")
        print(f"   👤 Usuario: charles.jelvez@ufro.cl")
        print(f"   🔑 Contraseña: charles123")
        print(f"   👑 Rol: SUPERADMIN")
        print(f"\n🌐 Sistema disponible en: https://gestion-camaras-ufro.up.railway.app/")
        
        print(f"\n📋 TODOS LOS USUARIOS DISPONIBLES:")
        print(f"   charles.jelvez@ufro.cl / charles123     (SUPERADMIN)")
        print(f"   admin@ufro.cl / admin123               (ADMIN)")
        print(f"   supervisor@ufro.cl / super123          (SUPERVISOR)")
        print(f"   tecnico1@ufro.cl / tecnico123          (TÉCNICO)")
        print(f"   visualizador@ufro.cl / viz123          (VISUALIZADOR)")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()