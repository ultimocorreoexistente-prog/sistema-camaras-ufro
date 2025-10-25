#!/usr/bin/env python3
"""
Script para inicializar usuarios en Railway PostgreSQL
Ejecutar después del deploy
"""
from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

def init_usuarios_railway():
    """Inicializa usuarios en Railway PostgreSQL"""
    
    with app.app_context():
        print("🚀 Inicializando usuarios en Railway PostgreSQL...")
        
        # Crear tablas si no existen
        try:
            db.create_all()
            print("✅ Tablas creadas/verificadas")
        except Exception as e:
            print(f"❌ Error creando tablas: {e}")
            return False
        
        # Limpiar usuarios existentes para empezar de cero
        try:
            Usuario.query.delete()
            db.session.commit()
            print("🧹 Usuarios existentes eliminados")
        except Exception as e:
            print(f"⚠️ Error limpiando usuarios: {e}")
        
        # Crear usuarios en orden de prioridad
        usuarios_data = [
            ('charles.jelvez@ufro.cl', 'charles123', 'superadmin', 'Charles Jélvez'),
            ('admin@ufro.cl', 'admin123', 'admin', 'Administrador'),
            ('supervisor@ufro.cl', 'super123', 'supervisor', 'Supervisor'),
            ('tecnico1@ufro.cl', 'tecnico123', 'tecnico', 'Técnico 1'),
            ('visualizador@ufro.cl', 'viz123', 'visualizador', 'Visualizador')
        ]
        
        print("\n👥 Creando usuarios:")
        for email, password, rol, nombre in usuarios_data:
            try:
                usuario = Usuario(
                    email=email,
                    nombre=nombre,
                    rol=rol,
                    activo=True
                )
                usuario.set_password(password)
                db.session.add(usuario)
                db.session.commit()
                print(f"  ✅ {email} ({rol}) - {nombre}")
            except Exception as e:
                print(f"  ❌ Error creando {email}: {e}")
                db.session.rollback()
        
        # Verificar resultado final
        usuarios = Usuario.query.order_by(Usuario.rol.desc()).all()
        print(f"\n📊 Total usuarios creados: {len(usuarios)}")
        
        print("\n🎯 CREDENCIALES PARA RAILWAY:")
        print("=" * 50)
        print("URL: https://gestion-camaras-ufro.up.railway.app/")
        print("=" * 50)
        for usuario in usuarios:
            # Obtener contraseña según email
            if usuario.email == 'charles.jelvez@ufro.cl':
                pwd = 'charles123'
            elif usuario.email == 'admin@ufro.cl':
                pwd = 'admin123'
            elif usuario.email == 'supervisor@ufro.cl':
                pwd = 'super123'
            elif usuario.email == 'tecnico1@ufro.cl':
                pwd = 'tecnico123'
            else:
                pwd = 'viz123'
            
            print(f"{usuario.email:25} | {usuario.rol:10} | {pwd}")
        print("=" * 50)
        
        return True

if __name__ == '__main__':
    success = init_usuarios_railway()
    if success:
        print("\n🎉 Inicialización completada exitosamente!")
    else:
        print("\n❌ Error en la inicialización")