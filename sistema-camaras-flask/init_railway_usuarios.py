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
            ('charles.jelvez', 'charles123', 'superadmin', 'Charles Jélvez', 'charles.jelvez@ufro.cl'),
            ('admin', 'admin123', 'admin', 'Administrador', 'admin@ufro.cl'),
            ('supervisor', 'super123', 'supervisor', 'Supervisor', 'supervisor@ufro.cl'),
            ('tecnico1', 'tecnico123', 'tecnico', 'Técnico 1', 'tecnico1@ufro.cl'),
            ('visualizador', 'viz123', 'visualizador', 'Visualizador', 'visualizador@ufro.cl')
        ]
        
        print("\n👥 Creando usuarios:")
        for username, password, rol, nombre, email in usuarios_data:
            try:
                usuario = Usuario(
                    username=username,
                    rol=rol,
                    nombre_completo=nombre,
                    email=email,
                    activo=True
                )
                usuario.set_password(password)
                db.session.add(usuario)
                db.session.commit()
                print(f"  ✅ {username} ({rol}) - {nombre}")
            except Exception as e:
                print(f"  ❌ Error creando {username}: {e}")
                db.session.rollback()
        
        # Verificar resultado final
        usuarios = Usuario.query.order_by(Usuario.rol.desc()).all()
        print(f"\n📊 Total usuarios creados: {len(usuarios)}")
        
        print("\n🎯 CREDENCIALES PARA RAILWAY:")
        print("=" * 50)
        print("URL: https://gestion-camaras-ufro.up.railway.app/")
        print("=" * 50)
        for usuario in usuarios:
            # Obtener contraseña según rol
            if usuario.username == 'charles.jelvez':
                pwd = 'charles123'
            elif usuario.username == 'admin':
                pwd = 'admin123'
            elif usuario.username == 'supervisor':
                pwd = 'super123'
            elif usuario.username == 'tecnico1':
                pwd = 'tecnico123'
            else:
                pwd = 'viz123'
            
            print(f"{usuario.username:15} | {usuario.rol:10} | {pwd}")
        print("=" * 50)
        
        return True

if __name__ == '__main__':
    success = init_usuarios_railway()
    if success:
        print("\n🎉 Inicialización completada exitosamente!")
    else:
        print("\n❌ Error en la inicialización")