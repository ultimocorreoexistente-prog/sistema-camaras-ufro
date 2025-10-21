#!/usr/bin/env python3
"""
Script para actualizar la base de datos con soporte para campus y infraestructura de red
"""

import sqlite3
import psycopg2
import os
from urllib.parse import urlparse

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
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
        conn = sqlite3.connect('fallas_mantenimiento.db')
    
    return conn

def actualizar_esquema_campus():
    """Actualiza las tablas existentes para agregar soporte de campus"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Actualizando esquema de base de datos...")
        
        # Agregar campo campus a tabla camaras si no existe
        try:
            cursor.execute("ALTER TABLE camaras ADD COLUMN campus TEXT")
            print("✓ Campo 'campus' agregado a tabla 'camaras'")
        except:
            print("• Campo 'campus' ya existe en tabla 'camaras'")
        
        # Agregar campo campus a tabla fallas si no existe
        try:
            cursor.execute("ALTER TABLE fallas ADD COLUMN campus TEXT")
            print("✓ Campo 'campus' agregado a tabla 'fallas'")
        except:
            print("• Campo 'campus' ya existe en tabla 'fallas'")
        
        # Agregar campo campus a tabla fallas_mejoradas si existe
        try:
            cursor.execute("ALTER TABLE fallas_mejoradas ADD COLUMN campus TEXT")
            print("✓ Campo 'campus' agregado a tabla 'fallas_mejoradas'")
        except:
            print("• Campo 'campus' ya existe en tabla 'fallas_mejoradas' o la tabla no existe")
        
        # Crear tabla de infraestructura de red
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS infraestructura_red (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                componente_id TEXT UNIQUE NOT NULL,
                tipo_componente TEXT NOT NULL,
                campus TEXT NOT NULL,
                ubicacion TEXT,
                ip_address TEXT,
                estado TEXT DEFAULT 'Operativo',
                dependencias TEXT,
                nivel_jerarquico INTEGER DEFAULT 1,
                fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                especificaciones TEXT,
                observaciones TEXT
            )
        ''')
        print("✓ Tabla 'infraestructura_red' creada")
        
        # Crear tabla de relaciones entre componentes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relaciones_componentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                componente_padre TEXT NOT NULL,
                componente_hijo TEXT NOT NULL,
                tipo_relacion TEXT NOT NULL,
                FOREIGN KEY (componente_padre) REFERENCES infraestructura_red (componente_id),
                FOREIGN KEY (componente_hijo) REFERENCES infraestructura_red (componente_id)
            )
        ''')
        print("✓ Tabla 'relaciones_componentes' creada")
        
        conn.commit()
        print("\n✅ Esquema actualizado exitosamente")
        
    except Exception as e:
        print(f"❌ Error actualizando esquema: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def poblar_datos_ejemplo():
    """Pobla la base de datos con datos de ejemplo de infraestructura"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("\nPoblando datos de ejemplo...")
        
        # Campus ejemplo
        campus_data = [
            # Campus Norte
            ('CORE-SW-NORTE', 'Core_Switch', 'Campus Norte', 'Edificio Central Norte', '192.168.1.1', 'Operativo', '', 0),
            ('SW-CN-001', 'Switch', 'Campus Norte', 'Edificio A', '192.168.1.10', 'Operativo', 'CORE-SW-NORTE', 1),
            ('SW-CN-002', 'Switch', 'Campus Norte', 'Edificio B', '192.168.1.11', 'Operativo', 'CORE-SW-NORTE', 1),
            ('GAB-CN-A01', 'Gabinete', 'Campus Norte', 'Entrada Edificio A', '', 'Operativo', 'SW-CN-001', 2),
            ('GAB-CN-A02', 'Gabinete', 'Campus Norte', 'Pasillo Edificio A', '', 'Operativo', 'SW-CN-001', 2),
            ('GAB-CN-B01', 'Gabinete', 'Campus Norte', 'Entrada Edificio B', '', 'Operativo', 'SW-CN-002', 2),
            ('UPS-CN-A01', 'UPS', 'Campus Norte', 'Edificio A - Sótano', '', 'Operativo', 'GAB-CN-A01', 3),
            ('UPS-CN-B01', 'UPS', 'Campus Norte', 'Edificio B - Sótano', '', 'Operativo', 'GAB-CN-B01', 3),
            
            # Campus Sur
            ('CORE-SW-SUR', 'Core_Switch', 'Campus Sur', 'Edificio Central Sur', '192.168.2.1', 'Operativo', '', 0),
            ('SW-CS-001', 'Switch', 'Campus Sur', 'Laboratorios', '192.168.2.10', 'Operativo', 'CORE-SW-SUR', 1),
            ('SW-CS-002', 'Switch', 'Campus Sur', 'Biblioteca', '192.168.2.11', 'Operativo', 'CORE-SW-SUR', 1),
            ('GAB-CS-L01', 'Gabinete', 'Campus Sur', 'Entrada Laboratorios', '', 'Operativo', 'SW-CS-001', 2),
            ('GAB-CS-B01', 'Gabinete', 'Campus Sur', 'Entrada Biblioteca', '', 'Operativo', 'SW-CS-002', 2),
            ('UPS-CS-L01', 'UPS', 'Campus Sur', 'Laboratorios - Técnico', '', 'Operativo', 'GAB-CS-L01', 3),
            
            # Campus Centro
            ('CORE-SW-CENTRO', 'Core_Switch', 'Campus Centro', 'Edificio Administrativo', '192.168.3.1', 'Operativo', '', 0),
            ('SW-CC-001', 'Switch', 'Campus Centro', 'Rectoría', '192.168.3.10', 'Operativo', 'CORE-SW-CENTRO', 1),
            ('GAB-CC-R01', 'Gabinete', 'Campus Centro', 'Entrada Rectoría', '', 'Operativo', 'SW-CC-001', 2),
            ('UPS-CC-R01', 'UPS', 'Campus Centro', 'Rectoría - Técnico', '', 'Operativo', 'GAB-CC-R01', 3),
        ]
        
        # Insertar datos de infraestructura
        cursor.executemany('''
            INSERT OR REPLACE INTO infraestructura_red 
            (componente_id, tipo_componente, campus, ubicacion, ip_address, estado, dependencias, nivel_jerarquico)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', campus_data)
        
        # Actualizar algunas cámaras con campus ejemplo
        campus_updates = [
            ('Campus Norte', 'CAM-001'),
            ('Campus Norte', 'CAM-002'),
            ('Campus Norte', 'CAM-003'),
            ('Campus Sur', 'CAM-015'),
            ('Campus Sur', 'CAM-016'),
            ('Campus Centro', 'CAM-033'),
            ('Campus Centro', 'CAM-034'),
        ]
        
        for campus, camara in campus_updates:
            try:
                cursor.execute('UPDATE camaras SET campus = ? WHERE nombre = ?', (campus, camara))
            except:
                pass  # Si no existe la cámara, continuar
        
        conn.commit()
        print("✅ Datos de ejemplo poblados exitosamente")
        
    except Exception as e:
        print(f"❌ Error poblando datos: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def verificar_estructura():
    """Verifica que la estructura esté correctamente creada"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("\nVerificando estructura de base de datos...")
        
        # Verificar tablas
        if os.environ.get('DATABASE_URL'):
            # PostgreSQL
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)
        else:
            # SQLite
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        
        tablas = [row[0] for row in cursor.fetchall()]
        print(f"Tablas encontradas: {', '.join(tablas)}")
        
        # Verificar datos de infraestructura
        cursor.execute("SELECT COUNT(*) FROM infraestructura_red")
        count_infra = cursor.fetchone()[0]
        print(f"Componentes de infraestructura: {count_infra}")
        
        # Verificar campus en cámaras
        try:
            cursor.execute("SELECT DISTINCT campus FROM camaras WHERE campus IS NOT NULL")
            campus_camaras = [row[0] for row in cursor.fetchall()]
            print(f"Campus en cámaras: {', '.join(campus_camaras) if campus_camaras else 'Ninguno'}")
        except:
            print("Campo campus no disponible en tabla cámaras")
        
        print("✅ Verificación completada")
        
    except Exception as e:
        print(f"❌ Error en verificación: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== ACTUALIZACIÓN DE BASE DE DATOS PARA SISTEMA DE CAMPUS ===\n")
    
    actualizar_esquema_campus()
    poblar_datos_ejemplo()
    verificar_estructura()
    
    print("\n=== ACTUALIZACIÓN COMPLETADA ===")
    print("\nPróximos pasos:")
    print("1. Ejecutar la aplicación: python app.py")
    print("2. Acceder a /informes-avanzados para ver las nuevas funcionalidades")
    print("3. Configurar datos reales de campus para cada cámara")