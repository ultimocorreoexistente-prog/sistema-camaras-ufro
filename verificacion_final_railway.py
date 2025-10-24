#!/usr/bin/env python3
"""
Script de verificación final de credenciales en Railway
Ejecutar en el entorno de Railway
"""
import os
import sys

# Verificar directorio
if os.path.exists('/app'):
    os.chdir('/app')
elif os.path.exists('/workspace/sistema-camaras-flask'):
    os.chdir('/workspace/sistema-camaras-flask')

try:
    from app import app, db
    from models import Usuario
    
    with app.app_context():
        print("🔍 VERIFICACIÓN FINAL DE USUARIOS EN RAILWAY")
        print("=" * 50)
        
        # Obtener todos los usuarios
        usuarios = Usuario.query.order_by(Usuario.rol.desc()).all()
        
        if not usuarios:
            print("❌ NO HAY USUARIOS EN LA BASE DE DATOS")
            print("Esto explica por qué Charles no puede ingresar")
        else:
            print(f"✅ USUARIOS ENCONTRADOS: {len(usuarios)}")
            print()
            
            # Verificar específicamente Charles
            charles = Usuario.query.filter_by(username='charles.jelvez').first()
            
            if charles:
                print(f"👑 CHARLES ENCONTRADO:")
                print(f"   Usuario: {charles.username}")
                print(f"   Rol: {charles.rol}")
                print(f"   Nombre: {charles.nombre_completo}")
                print(f"   Email: {charles.email}")
                print(f"   Activo: {'✅' if charles.activo else '❌'}")
                
                # Probar credenciales
                if charles.check_password('charles123'):
                    print("   🔑 Contraseña CORRECTA: charles123")
                    print()
                    print("🎉 CHARLES PUEDE INGRESAR!")
                    print("   URL: https://gestion-camaras-ufro.up.railway.app/")
                    print("   Usuario: charles.jelvez")
                    print("   Contraseña: charles123")
                else:
                    print("   ❌ Contraseña INCORRECTA")
                    # Actualizar contraseña
                    charles.set_password('charles123')
                    db.session.commit()
                    print("   ✅ Contraseña actualizada a: charles123")
            else:
                print("❌ CHARLES NO EXISTE EN LA BASE DE DATOS")
                print("   Creando usuario...")
                
                # Crear Charles
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
                print("   ✅ Charles creado exitosamente")
        
        print()
        print("📊 TODOS LOS USUARIOS:")
        credenciales_test = {
            'charles.jelvez': 'charles123',
            'admin': 'admin123', 
            'supervisor': 'super123',
            'tecnico1': 'tecnico123',
            'visualizador': 'viz123'
        }
        
        for usuario in usuarios:
            pwd_test = credenciales_test.get(usuario.username, 'N/A')
            estado_pwd = "✅" if usuario.check_password(pwd_test) else "❌"
            print(f"  {usuario.username:15} | {usuario.rol:10} | {pwd_test} | {estado_pwd}")
        
        print()
        print("=" * 50)
        print("🎯 CREDENCIALES FINALES VERIFICADAS:")
        print("SUPERADMIN: charles.jelvez / charles123")
        print("ADMIN: admin / admin123")
        print("=" * 50)

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()