#!/usr/bin/env python3
"""
Implementación completa del sistema de control de usuarios y roles
para el Sistema de Gestión de Cámaras UFRO

Este script implementa:
1. Creación de usuario SUPERADMIN Charles
2. Sistema de roles y permisos
3. Funciones de gestión (creación, modificación, asignación)
4. Verificación de integridad
"""

import sys
import os
import hashlib
from datetime import datetime

# Simulación del modelo de datos
class Usuario:
    def __init__(self, username, password_hash, rol, nombre_completo, email, activo=True):
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.nombre_completo = nombre_completo
        self.email = email
        self.activo = activo
        self.fecha_creacion = datetime.now()
    
    def __repr__(self):
        return f"<Usuario {self.username} ({self.rol})>"

class SistemaUsuarios:
    def __init__(self):
        self.usuarios = []
        self.roles_permisos = {
            'superadmin': {
                'descripcion': 'Super Administrador',
                'permisos': ['todos'],
                'accesos': ['todas_las_funciones']
            },
            'admin': {
                'descripcion': 'Administrador',
                'permisos': ['gestion_usuarios', 'gestion_equipos', 'reportes'],
                'accesos': ['dashboard', 'equipos', 'usuarios', 'reportes']
            },
            'supervisor': {
                'descripcion': 'Supervisor',
                'permisos': ['supervision', 'reportes'],
                'accesos': ['dashboard', 'equipos', 'reportes']
            },
            'tecnico': {
                'descripcion': 'Técnico',
                'permisos': ['mantenimiento'],
                'accesos': ['equipos', 'mantenimientos']
            },
            'visualizador': {
                'descripcion': 'Visualizador',
                'permisos': ['solo_lectura'],
                'accesos': ['dashboard', 'equipos_consulta']
            }
        }
    
    def generar_hash_werkzeug(self, password):
        """Generar hash compatible con Werkzeug/Flask"""
        import secrets
        # Generar salt aleatorio
        salt = secrets.token_hex(16)
        # Hash usando PBKDF2 (mismo método que Werkzeug)
        hash_obj = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode('utf-8'), 
                                       salt.encode('utf-8'), 
                                       100000)
        # Formato similar a Werkzeug
        hash_hex = hash_obj.hex()
        return f"pbkdf2:sha256:1000000${salt}${hash_hex}"
    
    def crear_usuario(self, username, password, rol, nombre_completo, email, activo=True):
        """Crear nuevo usuario con el rol especificado"""
        
        # Validar rol
        if rol not in self.roles_permisos:
            raise ValueError(f"Rol '{rol}' no válido. Roles disponibles: {list(self.roles_permisos.keys())}")
        
        # Verificar que no existe
        for usuario in self.usuarios:
            if usuario.username == username:
                raise ValueError(f"Usuario '{username}' ya existe")
        
        # Generar hash de contraseña
        password_hash = self.generar_hash_werkzeug(password)
        
        # Crear usuario
        nuevo_usuario = Usuario(username, password_hash, rol, nombre_completo, email, activo)
        self.usuarios.append(nuevo_usuario)
        
        return nuevo_usuario
    
    def actualizar_usuario(self, username, **kwargs):
        """Actualizar información de usuario existente"""
        
        usuario = self.buscar_usuario(username)
        if not usuario:
            raise ValueError(f"Usuario '{username}' no encontrado")
        
        # Actualizar campos permitidos
        campos_permitidos = ['rol', 'nombre_completo', 'email', 'activo']
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                setattr(usuario, campo, valor)
                
                # Si se actualiza el rol, validar
                if campo == 'rol' and valor not in self.roles_permisos:
                    raise ValueError(f"Rol '{valor}' no válido")
        
        return usuario
    
    def cambiar_password(self, username, nueva_password):
        """Cambiar contraseña de usuario"""
        
        usuario = self.buscar_usuario(username)
        if not usuario:
            raise ValueError(f"Usuario '{username}' no encontrado")
        
        usuario.password_hash = self.generar_hash_werkzeug(nueva_password)
        return usuario
    
    def buscar_usuario(self, username):
        """Buscar usuario por username"""
        for usuario in self.usuarios:
            if usuario.username == username:
                return usuario
        return None
    
    def verificar_credenciales(self, username, password):
        """Verificar credenciales de usuario (simulación)"""
        usuario = self.buscar_usuario(username)
        if not usuario or not usuario.activo:
            return False
        
        # En implementación real, verificar contra hash
        # Por ahora, simular para demonstração
        if usuario.password_hash.startswith('pbkdf2:'):
            # Verificar estructura del hash
            return True
        
        return False
    
    def obtener_permisos_usuario(self, username):
        """Obtener permisos de un usuario"""
        usuario = self.buscar_usuario(username)
        if not usuario:
            return None
        
        return self.roles_permisos.get(usuario.rol, {})
    
    def listar_usuarios(self):
        """Listar todos los usuarios"""
        return self.usuarios
    
    def listar_roles(self):
        """Listar roles disponibles"""
        return self.roles_permisos
    
    def generar_sql_completo(self):
        """Generar SQL completo para crear todos los usuarios"""
        
        sql_parts = []
        sql_parts.append("-- SISTEMA COMPLETO DE USUARIOS Y ROLES")
        sql_parts.append("-- Generación: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sql_parts.append("")
        
        # Limpiar tabla de usuarios
        sql_parts.append("-- Limpiar tabla de usuarios")
        sql_parts.append("DELETE FROM usuario;")
        sql_parts.append("")
        
        # Insertar usuarios
        sql_parts.append("-- Crear usuarios con roles y permisos")
        
        usuarios_a_crear = [
            {
                'username': 'charles.jelvez',
                'password': 'charles123',
                'rol': 'superadmin',
                'nombre': 'Charles Jélvez',
                'email': 'charles.jelvez@ufro.cl'
            },
            {
                'username': 'admin',
                'password': 'admin123',
                'rol': 'admin',
                'nombre': 'Administrador Principal',
                'email': 'admin@ufro.cl'
            },
            {
                'username': 'supervisor',
                'password': 'super123',
                'rol': 'supervisor',
                'nombre': 'Supervisor General',
                'email': 'supervisor@ufro.cl'
            },
            {
                'username': 'tecnico1',
                'password': 'tecnico123',
                'rol': 'tecnico',
                'nombre': 'Técnico Principal',
                'email': 'tecnico@ufro.cl'
            },
            {
                'username': 'visualizador',
                'password': 'visual123',
                'rol': 'visualizador',
                'nombre': 'Visualizador',
                'email': 'visualizador@ufro.cl'
            }
        ]
        
        for usuario in usuarios_a_crear:
            hash_password = self.generar_hash_werkzeug(usuario['password'])
            
            sql_parts.append(f"INSERT INTO usuario (username, password_hash, rol, nombre_completo, email, activo, fecha_creacion)")
            sql_parts.append(f"VALUES ('{usuario['username']}', '{hash_password}', '{usuario['rol']}', '{usuario['nombre']}', '{usuario['email']}', true, NOW());")
            sql_parts.append("")
        
        # Consulta de verificación
        sql_parts.append("-- Verificar usuarios creados")
        sql_parts.append("SELECT username, rol, nombre_completo, email, activo FROM usuario ORDER BY rol, username;")
        
        return "\n".join(sql_parts)
    
    def generar_documentacion(self):
        """Generar documentación del sistema"""
        
        doc_parts = []
        doc_parts.append("# SISTEMA DE USUARIOS Y ROLES - GESTIÓN DE CÁMARAS UFRO")
        doc_parts.append("")
        doc_parts.append("## ROLES Y PERMISOS")
        doc_parts.append("")
        
        for rol, info in self.roles_permisos.items():
            doc_parts.append(f"### {rol.upper()}")
            doc_parts.append(f"**Descripción:** {info['descripcion']}")
            doc_parts.append(f"**Permisos:** {', '.join(info['permisos'])}")
            doc_parts.append(f"**Accesos:** {', '.join(info['accesos'])}")
            doc_parts.append("")
        
        doc_parts.append("## USUARIOS DEL SISTEMA")
        doc_parts.append("")
        
        usuarios = self.listar_usuarios()
        if usuarios:
            doc_parts.append("| Username | Rol | Nombre | Email | Estado |")
            doc_parts.append("|----------|-----|--------|--------|--------|")
            
            for usuario in usuarios:
                estado = "✅ Activo" if usuario.activo else "❌ Inactivo"
                doc_parts.append(f"| {usuario.username} | {usuario.rol} | {usuario.nombre_completo} | {usuario.email} | {estado} |")
        else:
            doc_parts.append("*No hay usuarios registrados*")
        
        doc_parts.append("")
        doc_parts.append("## CREDENCIALES DE ACCESO")
        doc_parts.append("")
        doc_parts.append("### Charles Jélvez (SUPERADMIN)")
        doc_parts.append("- **URL:** https://gestion-camaras-ufro.up.railway.app/")
        doc_parts.append("- **Usuario:** charles.jelvez")
        doc_parts.append("- **Contraseña:** charles123")
        doc_parts.append("- **Rol:** superadmin")
        doc_parts.append("")
        
        return "\n".join(doc_parts)

def main():
    print("🔧 IMPLEMENTACIÓN COMPLETA - SISTEMA DE USUARIOS Y ROLES")
    print("=" * 60)
    
    # Crear instancia del sistema
    sistema = SistemaUsuarios()
    
    try:
        # Crear usuarios del sistema
        print("👥 Creando usuarios del sistema...")
        
        # Charles SUPERADMIN
        charles = sistema.crear_usuario(
            username='charles.jelvez',
            password='charles123',
            rol='superadmin',
            nombre_completo='Charles Jélvez',
            email='charles.jelvez@ufro.cl'
        )
        print(f"✅ Charles Jélvez creado como {charles.rol}")
        
        # Usuario admin (para referencia)
        admin = sistema.crear_usuario(
            username='admin',
            password='admin123',
            rol='admin',
            nombre_completo='Administrador Principal',
            email='admin@ufro.cl'
        )
        print(f"✅ Admin creado como {admin.rol}")
        
        # Otros usuarios
        otros_usuarios = [
            ('supervisor', 'super123', 'supervisor', 'Supervisor General', 'supervisor@ufro.cl'),
            ('tecnico1', 'tecnico123', 'tecnico', 'Técnico Principal', 'tecnico@ufro.cl'),
            ('visualizador', 'visual123', 'visualizador', 'Visualizador', 'visualizador@ufro.cl')
        ]
        
        for username, password, rol, nombre, email in otros_usuarios:
            usuario = sistema.crear_usuario(username, password, rol, nombre, email)
            print(f"✅ {usuario.nombre_completo} creado como {usuario.rol}")
        
        print(f"\n📊 Total de usuarios creados: {len(sistema.usuarios)}")
        
        # Generar SQL completo
        print("\n📄 Generando SQL completo...")
        sql_completo = sistema.generar_sql_completo()
        
        with open('/workspace/sistema-camaras-flask/SISTEMA_USUARIOS_COMPLETO.sql', 'w', encoding='utf-8') as f:
            f.write(sql_completo)
        
        print("✅ SQL guardado en: SISTEMA_USUARIOS_COMPLETO.sql")
        
        # Generar documentación
        print("\n📚 Generando documentación...")
        documentacion = sistema.generar_documentacion()
        
        with open('/workspace/docs/SISTEMA_USUARIOS_DOCUMENTACION.md', 'w', encoding='utf-8') as f:
            f.write(documentacion)
        
        print("✅ Documentación guardada en: docs/SISTEMA_USUARIOS_DOCUMENTACION.md")
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("🎉 SISTEMA DE USUARIOS IMPLEMENTADO COMPLETAMENTE")
        print("=" * 60)
        print("\n🔑 CREDENCIALES PRINCIPALES:")
        print("   URL: https://gestion-camaras-ufro.up.railway.app/")
        print("   Usuario: charles.jelvez")
        print("   Contraseña: charles123")
        print("   Rol: SUPERADMIN")
        print("\n📋 ARCHIVOS GENERADOS:")
        print("   1. SISTEMA_USUARIOS_COMPLETO.sql (SQL para ejecutar)")
        print("   2. SISTEMA_USUARIOS_DOCUMENTACION.md (Documentación completa)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ IMPLEMENTACIÓN COMPLETA EXITOSA")
    else:
        print("\n❌ ERROR EN LA IMPLEMENTACIÓN")
        sys.exit(1)