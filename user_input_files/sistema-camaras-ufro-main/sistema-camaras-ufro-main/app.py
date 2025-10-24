from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session, make_response
import os
import sqlite3
import psycopg2
from urllib.parse import urlparse
import json
from datetime import datetime, timedelta
import io
import tempfile
from werkzeug.utils import secure_filename
import hashlib
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones_2024'

# Configuración de la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'doc', 'pdf', 'txt'}

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    try:
        if DATABASE_URL:
            # PostgreSQL para producción
            url = urlparse(DATABASE_URL)
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        else:
            # SQLite para desarrollo local
            conn = sqlite3.connect('sistema_camaras.db')
            conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error de conexión a BD: {e}")
        # Crear BD SQLite como fallback
        conn = sqlite3.connect('sistema_camaras.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Inicializa la base de datos completa"""
    print("Iniciando configuración de base de datos...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if DATABASE_URL:
            print("Configurando PostgreSQL...")
            # PostgreSQL - Crear todas las tablas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    rol VARCHAR(20) DEFAULT 'tecnico',
                    activo BOOLEAN DEFAULT TRUE,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS camaras (
                    id SERIAL PRIMARY KEY,
                    ubicacion VARCHAR(200) NOT NULL,
                    marca VARCHAR(100),
                    modelo VARCHAR(100),
                    ip VARCHAR(45),
                    estado VARCHAR(50) DEFAULT 'operativa',
                    fecha_instalacion DATE,
                    campus VARCHAR(100),
                    edificio VARCHAR(100),
                    responsable VARCHAR(100),
                    observaciones TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fallas (
                    id SERIAL PRIMARY KEY,
                    camara_id INTEGER REFERENCES camaras(id),
                    descripcion TEXT NOT NULL,
                    gravedad VARCHAR(20) DEFAULT 'media',
                    estado VARCHAR(20) DEFAULT 'abierta',
                    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_asignacion TIMESTAMP,
                    fecha_resolucion TIMESTAMP,
                    tecnico_asignado VARCHAR(100),
                    reportado_por VARCHAR(100),
                    solucion TEXT,
                    costo_reparacion DECIMAL(10,2),
                    tiempo_resolucion INTEGER
                )
            """)
            
        else:
            print("Configurando SQLite...")
            # SQLite - Crear todas las tablas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    rol TEXT DEFAULT 'tecnico',
                    activo INTEGER DEFAULT 1,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS camaras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ubicacion TEXT NOT NULL,
                    marca TEXT,
                    modelo TEXT,
                    ip TEXT,
                    estado TEXT DEFAULT 'operativa',
                    fecha_instalacion DATE,
                    campus TEXT,
                    edificio TEXT,
                    responsable TEXT,
                    observaciones TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fallas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    camara_id INTEGER,
                    descripcion TEXT NOT NULL,
                    gravedad TEXT DEFAULT 'media',
                    estado TEXT DEFAULT 'abierta',
                    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_asignacion DATETIME,
                    fecha_resolucion DATETIME,
                    tecnico_asignado TEXT,
                    reportado_por TEXT,
                    solucion TEXT,
                    costo_reparacion REAL,
                    tiempo_resolucion INTEGER,
                    FOREIGN KEY (camara_id) REFERENCES camaras (id)
                )
            """)
        
        print("Tablas creadas exitosamente")
        
        # Insertar usuarios de prueba
        usuarios_prueba = [
            ('admin', 'admin123', 'Administrador Sistema', 'administrador'),
            ('tecnico1', 'tecnico123', 'Juan Pérez', 'tecnico'),
            ('tecnico2', 'tecnico123', 'María González', 'tecnico'),
            ('supervisor', 'super123', 'Carlos Rodríguez', 'supervisor')
        ]
        
        for username, password, nombre, rol in usuarios_prueba:
            password_hash = hashlib.md5(password.encode()).hexdigest()
            print(f"Creando usuario: {username} con rol: {rol}")
            
            try:
                if DATABASE_URL:
                    cursor.execute("""
                        INSERT INTO usuarios (username, password_hash, nombre, rol)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (username) DO NOTHING
                    """, (username, password_hash, nombre, rol))
                else:
                    cursor.execute("""
                        INSERT OR IGNORE INTO usuarios (username, password_hash, nombre, rol)
                        VALUES (?, ?, ?, ?)
                    """, (username, password_hash, nombre, rol))
                    
                print(f"Usuario {username} procesado correctamente")
            except Exception as e:
                print(f"Error creando usuario {username}: {e}")
        
        # Insertar cámaras de ejemplo
        camaras_ejemplo = [
            ('Entrada Principal Campus Norte', 'Hikvision', 'DS-2CD2055', '192.168.1.100', 'Campus Norte', 'Edificio A', 'Juan Pérez'),
            ('Estacionamiento Norte', 'Dahua', 'IPC-HFW4431R-Z', '192.168.1.101', 'Campus Norte', 'Exterior', 'María González'),
            ('Biblioteca Central', 'Axis', 'M3027-PVE', '192.168.1.102', 'Campus Centro', 'Biblioteca', 'Carlos Rodríguez'),
        ]
        
        print("Creando cámaras de ejemplo...")
        for camara in camaras_ejemplo:
            try:
                if DATABASE_URL:
                    cursor.execute("""
                        INSERT INTO camaras (ubicacion, marca, modelo, ip, campus, edificio, responsable)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, camara)
                else:
                    cursor.execute("""
                        INSERT OR IGNORE INTO camaras (ubicacion, marca, modelo, ip, campus, edificio, responsable)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, camara)
            except Exception as e:
                print(f"Error creando cámara: {e}")
        
        conn.commit()
        print("Base de datos inicializada correctamente con usuarios y datos de prueba")
        
        # Verificar que los usuarios se crearon
        print("Verificando usuarios creados:")
        cursor.execute("SELECT username, rol FROM usuarios")
        usuarios_existentes = cursor.fetchall()
        for user in usuarios_existentes:
            if DATABASE_URL:
                print(f"- Usuario: {user[0]}, Rol: {user[1]}")
            else:
                print(f"- Usuario: {user['username']}, Rol: {user['rol']}")
        
    except Exception as e:
        print(f"Error inicializando BD: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

def verificar_login(username, password):
    """Verifica las credenciales del usuario"""
    print(f"Intentando login para usuario: {username}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password_hash = hashlib.md5(password.encode()).hexdigest()
    print(f"Hash de contraseña generado: {password_hash}")
    
    try:
        if DATABASE_URL:
            cursor.execute("""
                SELECT id, username, nombre, rol
                FROM usuarios 
                WHERE username = %s AND password_hash = %s AND activo = TRUE
            """, (username, password_hash))
        else:
            cursor.execute("""
                SELECT id, username, nombre, rol
                FROM usuarios 
                WHERE username = ? AND password_hash = ? AND activo = 1
            """, (username, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            if DATABASE_URL:
                print(f"Login exitoso para usuario: {user[1]}, rol: {user[3]}")
                return user
            else:
                print(f"Login exitoso para usuario: {user['username']}, rol: {user['rol']}")
                return user
        else:
            print(f"Login fallido - usuario no encontrado o credenciales incorrectas")
            # Debug: mostrar todos los usuarios existentes
            cursor.execute("SELECT username, password_hash FROM usuarios")
            todos_usuarios = cursor.fetchall()
            print("Usuarios en BD:")
            for u in todos_usuarios:
                if DATABASE_URL:
                    print(f"  - {u[0]}: {u[1]}")
                else:
                    print(f"  - {u['username']}: {u['password_hash']}")
            return None
            
    except Exception as e:
        print(f"Error en verificar_login: {e}")
        return None
    finally:
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje_error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = verificar_login(username, password)
        
        if user:
            if DATABASE_URL:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['nombre'] = user[2]
                session['rol'] = user[3]
            else:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['nombre'] = user['nombre']
                session['rol'] = user['rol']
            return redirect(url_for('dashboard'))
        else:
            mensaje_error = 'Usuario o contraseña incorrectos'
    
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de Cámaras UFRO - Login</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; display: flex; align-items: center; justify-content: center;
            }}
            .login-container {{
                background: white; border-radius: 20px; padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 600px; width: 90%;
            }}
            @media (max-width: 768px) {{
                .login-container {{ max-width: 400px; padding: 30px; }}
            }}
            @media (min-width: 769px) {{
                .login-container {{ max-width: 600px; padding: 50px; }}
            }}
            @media (min-width: 1200px) {{
                .login-container {{ max-width: 700px; padding: 60px; }}
            }}
            .logo {{ text-align: center; margin-bottom: 30px; }}
            .logo h1 {{ color: #667eea; font-size: 2.5rem; margin-bottom: 10px; }}
            .logo p {{ color: #666; font-size: 1.1rem; }}
            .form-group {{ margin-bottom: 20px; }}
            .form-group label {{ display: block; margin-bottom: 8px; color: #333; font-weight: 500; }}
            .form-group input {{
                width: 100%; padding: 15px; border: 2px solid #e1e5e9;
                border-radius: 10px; font-size: 16px; transition: border-color 0.3s;
            }}
            .form-group input:focus {{ outline: none; border-color: #667eea; }}
            .btn-login {{
                width: 100%; padding: 15px; background: #667eea; color: white;
                border: none; border-radius: 10px; font-size: 16px; font-weight: 600;
                cursor: pointer; transition: background 0.3s;
            }}
            .btn-login:hover {{ background: #5a67d8; }}
            .alert {{ padding: 15px; border-radius: 10px; margin: 15px 0; }}
            .alert-danger {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .credentials {{
                margin-top: 30px; padding: 20px; background: #f8f9fa;
                border-radius: 10px; text-align: center;
            }}
            .credentials h3 {{ color: #667eea; margin-bottom: 15px; }}
            .credentials .cred {{ 
                display: inline-block; margin: 5px 10px; padding: 8px 15px;
                background: white; border-radius: 6px; font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">
                <h1>🎥 Sistema de Cámaras</h1>
                <p>Universidad de la Frontera</p>
            </div>
            
            {f'<div class="alert alert-danger">{mensaje_error}</div>' if mensaje_error else ''}
            
            <form method="POST">
                <div class="form-group">
                    <label for="username">Usuario</label>
                    <input type="text" id="username" name="username" required value="admin">
                </div>
                
                <div class="form-group">
                    <label for="password">Contraseña</label>
                    <input type="password" id="password" name="password" required value="admin123">
                </div>
                
                <button type="submit" class="btn-login">Iniciar Sesión</button>
            </form>
            
            <div class="credentials">
                <h3>🔑 Credenciales de Prueba</h3>
                <div class="cred"><strong>Admin:</strong> admin / admin123</div>
                <div class="cred"><strong>Técnico:</strong> tecnico1 / tecnico123</div>
                <div class="cred"><strong>Supervisor:</strong> supervisor / super123</div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Sistema Cámaras UFRO</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
            .dashboard-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .card h3 {{ color: #667eea; margin-bottom: 15px; }}
            .btn {{ padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
            .btn:hover {{ background: #5a67d8; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎥 Dashboard - Sistema de Cámaras UFRO</h1>
                <p>Bienvenido/a, <strong>{session['nombre']}</strong> ({session['rol']})</p>
                <a href="/logout" class="btn">Cerrar Sesión</a>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h3>📊 Estadísticas Generales</h3>
                    <p>• Total de cámaras: 3</p>
                    <p>• Cámaras operativas: 3</p>
                    <p>• Sistema funcionando correctamente</p>
                </div>
                
                <div class="card">
                    <h3>🎥 Gestión de Cámaras</h3>
                    <button class="btn">Ver Todas las Cámaras</button>
                    <button class="btn">Agregar Nueva Cámara</button>
                    <button class="btn">Generar Reporte</button>
                </div>
                
                <div class="card">
                    <h3>⚠️ Gestión de Fallas</h3>
                    <button class="btn">Ver Fallas Activas</button>
                    <button class="btn">Reportar Nueva Falla</button>
                    <button class="btn">Asignar Técnicos</button>
                </div>
                
                <div class="card">
                    <h3>📈 Reportes y Análisis</h3>
                    <button class="btn">Reporte Mensual</button>
                    <button class="btn">Análisis de Rendimiento</button>
                    <button class="btn">Exportar a Excel</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Forzar inicialización al importar
print("Iniciando aplicación Flask...")
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
