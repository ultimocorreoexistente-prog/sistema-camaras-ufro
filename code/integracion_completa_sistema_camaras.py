#!/usr/bin/env python3
"""
Script de Integración Completa - Sistema de Gestión de Cámaras UFRO
====================================================================

Este script unifica:
1. Actualización de esquema con soporte de campus (actualizar_db_campus.py)
2. Integración de casos reales (integrador_casos_reales_v2.py)
3. Inserción del nuevo Caso 4 proporcionado
4. Inserción de tipos de fallas estándar

Autor: MiniMax Agent
Fecha: 2025-10-20
"""

import sqlite3
import os
from urllib.parse import urlparse
from datetime import datetime
import json

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

class IntegradorSistemaCamaras:
    def __init__(self, db_name='sistema_camaras.db'):
        self.db_name = db_name
        self.conn = None
        
    def get_db_connection(self):
        """Obtiene conexión a la base de datos"""
        DATABASE_URL = os.environ.get('DATABASE_URL')
        
        if DATABASE_URL and POSTGRES_AVAILABLE:
            # PostgreSQL para producción
            url = urlparse(DATABASE_URL)
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            print("✓ Conectado a PostgreSQL")
        else:
            # SQLite para desarrollo local
            conn = sqlite3.connect(self.db_name)
            print(f"✓ Conectado a SQLite: {self.db_name}")
        
        return conn
    
    def crear_tablas_base(self):
        """Crea las tablas base del sistema si no existen"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            print("\n=== CREANDO TABLAS BASE ===")
            
            # Tabla de cámaras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS camaras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    ubicacion TEXT,
                    edificio TEXT,
                    piso TEXT,
                    tipo TEXT,
                    modelo TEXT,
                    ip_address TEXT,
                    estado TEXT DEFAULT 'Activa',
                    campus TEXT,
                    fecha_instalacion TIMESTAMP,
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✓ Tabla 'camaras' creada")
            
            # Tabla de fallas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fallas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    camara_id INTEGER,
                    tipo_falla TEXT,
                    descripcion TEXT,
                    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_resolucion TIMESTAMP,
                    estado TEXT DEFAULT 'Pendiente',
                    prioridad TEXT DEFAULT 'Media',
                    tecnico_asignado TEXT,
                    solucion TEXT,
                    costo REAL,
                    campus TEXT,
                    observaciones TEXT,
                    FOREIGN KEY (camara_id) REFERENCES camaras (id)
                )
            ''')
            print("✓ Tabla 'fallas' creada")
            
            # Tabla de tipos de fallas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tipos_fallas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    categoria TEXT NOT NULL,
                    prioridad TEXT NOT NULL,
                    tiempo_estimado_resolucion INTEGER,
                    descripcion TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✓ Tabla 'tipos_fallas' creada")
            
            # Tabla de casos reales
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS casos_reales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_caso TEXT UNIQUE NOT NULL,
                    fecha_caso DATE NOT NULL,
                    descripcion TEXT,
                    componentes_involucrados TEXT,
                    dependencias_cascada TEXT,
                    solucion_aplicada TEXT,
                    tiempo_resolucion_horas REAL,
                    lecciones_aprendidas TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✓ Tabla 'casos_reales' creada")
            
            # Tabla de fallas específicas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fallas_especificas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_falla DATE NOT NULL,
                    tipo_falla TEXT NOT NULL,
                    componente_afectado_tipo TEXT,
                    componente_afectado_id TEXT,
                    descripcion_falla TEXT,
                    camaras_afectadas TEXT,
                    tiempo_downtime_horas REAL,
                    solucion_aplicada TEXT,
                    fecha_resolucion DATE,
                    tecnico_reparador TEXT,
                    costo_reparacion REAL DEFAULT 0,
                    estado TEXT DEFAULT 'Pendiente',
                    prioridad TEXT DEFAULT 'Media',
                    campus TEXT,
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✓ Tabla 'fallas_especificas' creada")
            
            # Tabla de mantenimientos realizados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mantenimientos_realizados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_mantenimiento DATE NOT NULL,
                    tipo_mantenimiento TEXT NOT NULL,
                    componente_tipo TEXT,
                    componente_id TEXT,
                    descripcion_trabajo TEXT,
                    materiales_utilizados TEXT,
                    tecnico_responsable TEXT,
                    duracion_horas REAL,
                    costo_total REAL DEFAULT 0,
                    resultado TEXT,
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✓ Tabla 'mantenimientos_realizados' creada")
            
            # Tabla de infraestructura de red
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
            
            # Tabla de relaciones entre componentes
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
            print("\n✅ Todas las tablas base creadas exitosamente")
            
        except Exception as e:
            print(f"❌ Error creando tablas base: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def insertar_tipos_fallas(self):
        """Inserta los tipos de fallas estándar"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            print("\n=== INSERTANDO TIPOS DE FALLAS ===")
            
            tipos_fallas = [
                ('Suciedad por telaraña', 'LIMPIEZA', 'MEDIA', 30, 'Acumulación de telarañas en lente'),
                ('Manchas en lente', 'LIMPIEZA', 'MEDIA', 30, 'Manchas que afectan la calidad de imagen'),
                ('Mica rayada', 'REPARACION', 'ALTA', 120, 'Rayones en protección del lente'),
                ('Cámara sin imagen', 'TECNICA', 'CRITICA', 60, 'Pérdida total de señal de video'),
                ('Imagen borrosa', 'AJUSTE', 'MEDIA', 45, 'Falta de enfoque o calibración'),
                ('Falla de conectividad', 'TECNICA', 'ALTA', 90, 'Problemas de red o cableado'),
                ('Cámara desalineada', 'AJUSTE', 'MEDIA', 30, 'Posición incorrecta de la cámara'),
                ('Falla de alimentación', 'TECNICA', 'CRITICA', 120, 'Problemas eléctricos o POE'),
                ('Protección dañada', 'REPARACION', 'ALTA', 180, 'Carcasa o dome dañado'),
                ('Falla de grabación', 'TECNICA', 'ALTA', 90, 'Problemas con almacenamiento'),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO tipos_fallas 
                (nombre, categoria, prioridad, tiempo_estimado_resolucion, descripcion)
                VALUES (?, ?, ?, ?, ?)
            ''', tipos_fallas)
            
            conn.commit()
            print(f"✓ {len(tipos_fallas)} tipos de fallas insertados")
            
        except Exception as e:
            print(f"❌ Error insertando tipos de fallas: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def insertar_casos_reales(self):
        """Inserta los casos reales (incluyendo Caso 4 nuevo)"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            print("\n=== INSERTANDO CASOS REALES ===")
            
            # CASO 1: Telas de araña - Bunker
            cursor.execute('''
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion,
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Telas de araña - Bunker',
                '2024-10-12',
                'Cámara Bunker_EX_costado presenta telas de araña que afectan la calidad de imagen',
                json.dumps(['Cámara Bunker_EX_costado', 'Lente exterior']),
                json.dumps(['Limpieza manual requerida', 'Acceso con escalera']),
                'Limpieza manual del lente y carcasa exterior',
                1.0,
                'Programar limpieza preventiva trimestral para cámaras exteriores'
            ))
            print("✓ Caso 1: Telas de araña - Bunker")
            
            # CASO 2: Mantenimiento Edificio O
            cursor.execute('''
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion,
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Mantenimiento UPS Edificio O',
                '2024-10-13',
                'Cambio preventivo de 1 batería del UPS APC Smart-UPS SC 1500VA en sala técnica tercer piso Edificio O',
                json.dumps(['UPS APC Smart-UPS SC 1500VA', 'Batería RBC7 12V 17Ah', '11 cámaras Edificio O', '1 cámara PTZ Francisco Salazar vía fibra']),
                json.dumps(['Switch Edificio O', 'Enlace fibra óptica', 'Gabinete subterráneo Francisco Salazar', 'Cámara PTZ remota']),
                'Cambio exitoso de batería con sistema funcionando en batería restante',
                2.5,
                'Importancia de tener baterías redundantes para evitar corte total durante mantenimiento. Considerar ventana de mantenimiento para equipos críticos.'
            ))
            print("✓ Caso 2: Mantenimiento UPS Edificio O")
            
            # CASO 3: Falla CFT Prat
            cursor.execute('''
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion,
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Falla Cable NVR CFT Prat',
                '2024-10-14',
                '13 cámaras del CFT Prat perdieron conexión simultáneamente por cable suelto entre NVR e internet',
                json.dumps(['NVR CFT Prat', 'Cable ethernet NVR-Internet', '13 cámaras CFT Prat', 'Router Cisco CFT']),
                json.dumps(['Todas las cámaras CFT dependen de un solo NVR', 'NVR depende de una sola conexión a internet', 'Sin redundancia de conectividad']),
                'Reconexión y ajuste del cable ethernet, verificación de todas las conexiones',
                26.5,
                'Necesidad de implementar redundancia en ubicaciones con múltiples cámaras. Revisar todas las instalaciones de subcontratistas.'
            ))
            print("✓ Caso 3: Falla Cable NVR CFT Prat")
            
            # CASO 4: Caída cámaras ZM - Falla Eléctrica (NUEVO)
            cursor.execute('''
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion,
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Caída cámaras ZM - Falla Eléctrica',
                '2025-10-17',
                'Caída de 3 cámaras del ZM por falla eléctrica. Automático desconectado en caseta guardia frente a taller',
                json.dumps(['ZM-container_Ciclovia', 'ZM-Ciclovia a AM', 'ZM-Bodega_Ciclovia', 'Automático eléctrico caseta guardia']),
                json.dumps(['Caseta guardia frente a taller', 'Automático ubicado fuera de gabinetes principales', 'Zona ZM - Ciclovia']),
                'Subir automático en caseta guardia',
                2.67,  # 2h 40min = 2.67 horas
                'Automáticos eléctricos ubicados en lugares no convencionales requieren señalización y documentación clara. Considerar centralización de protecciones eléctricas.'
            ))
            print("✓ Caso 4: Caída cámaras ZM - Falla Eléctrica")
            
            conn.commit()
            print("\n✅ 4 casos reales insertados exitosamente")
            
        except Exception as e:
            print(f"❌ Error insertando casos reales: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def insertar_fallas_especificas(self):
        """Inserta las fallas específicas de los casos reales"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            print("\n=== INSERTANDO FALLAS ESPECÍFICAS ===")
            
            # Falla CFT Prat
            cursor.execute('''
                INSERT OR REPLACE INTO fallas_especificas (
                    fecha_falla, tipo_falla, componente_afectado_tipo,
                    componente_afectado_id, descripcion_falla,
                    camaras_afectadas, tiempo_downtime_horas,
                    solucion_aplicada, fecha_resolucion,
                    tecnico_reparador, costo_reparacion,
                    estado, prioridad, campus
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                '2024-10-14',
                'Cable suelto',
                'Cable ethernet',
                'cable-nvr-internet-cft',
                'Cable que conecta NVR con internet estaba suelto, causando pérdida total de conectividad',
                json.dumps(['cam-cft-1','cam-cft-2','cam-cft-3','cam-cft-4','cam-cft-5','cam-cft-6','cam-cft-7','cam-cft-8','cam-cft-9','cam-cft-10','cam-cft-11','cam-cft-12','cam-cft-13']),
                26.5,
                'Reconexión del cable ethernet y verificación de todas las conexiones del rack',
                '2024-10-15',
                'Juan Pérez (Personal CFT)',
                0,
                'Resuelto',
                'Alta',
                'Andrés Bello'
            ))
            print("✓ Falla CFT Prat insertada")
            
            # Falla Zona ZM - Caso 4
            cursor.execute('''
                INSERT OR REPLACE INTO fallas_especificas (
                    fecha_falla, tipo_falla, componente_afectado_tipo,
                    componente_afectado_id, descripcion_falla,
                    camaras_afectadas, tiempo_downtime_horas,
                    solucion_aplicada, fecha_resolucion,
                    tecnico_reparador, costo_reparacion,
                    estado, prioridad, campus, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                '2025-10-17',
                'Falla de alimentación',
                'Automático eléctrico',
                'automatico-caseta-guardia-taller',
                'Caída de 3 cámaras del ZM por falla eléctrica. Automático desconectado en caseta guardia frente a taller',
                json.dumps(['ZM-container_Ciclovia', 'ZM-Ciclovia a AM', 'ZM-Bodega_Ciclovia']),
                2.67,
                'Subir automático en caseta guardia',
                '2025-10-17',
                'Marco Contreras (Encargado Seguridad)',
                0,
                'Resuelto',
                'Alta',
                'Andrés Bello',
                'Automático ubicado fuera de los gabinetes principales, en caseta guardia frente a taller. Requiere señalización.'
            ))
            print("✓ Falla Zona ZM insertada")
            
            conn.commit()
            print("\n✅ Fallas específicas insertadas exitosamente")
            
        except Exception as e:
            print(f"❌ Error insertando fallas específicas: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def insertar_mantenimientos(self):
        """Inserta los mantenimientos realizados"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            print("\n=== INSERTANDO MANTENIMIENTOS ===")
            
            # Mantenimiento Edificio O
            cursor.execute('''
                INSERT OR REPLACE INTO mantenimientos_realizados (
                    fecha_mantenimiento, tipo_mantenimiento,
                    componente_tipo, componente_id,
                    descripcion_trabajo, materiales_utilizados,
                    tecnico_responsable, duracion_horas,
                    costo_total, resultado, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                '2024-10-13',
                'Preventivo',
                'UPS',
                'ups-edificio-o-p3',
                'Cambio preventivo de 1 batería UPS APC Smart-UPS SC 1500VA',
                json.dumps(['Batería RBC7 - 12V 17Ah x1']),
                'Personal interno',
                2.5,
                45000,
                'Exitoso',
                '11 cámaras temporalmente en riesgo durante cambio. Sistema funcionó con batería restante.'
            ))
            print("✓ Mantenimiento Edificio O insertado")
            
            conn.commit()
            print("\n✅ Mantenimientos insertados exitosamente")
            
        except Exception as e:
            print(f"❌ Error insertando mantenimientos: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def insertar_infraestructura_ejemplo(self):
        """Inserta datos de ejemplo de infraestructura de red"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            print("\n=== INSERTANDO INFRAESTRUCTURA DE RED ===")
            
            infraestructura_data = [
                # Campus Andrés Bello
                ('CORE-SW-AB', 'Core_Switch', 'Andrés Bello', 'Edificio Central', '192.168.1.1', 'Operativo', '', 0),
                ('SW-AB-001', 'Switch', 'Andrés Bello', 'Edificio O', '192.168.1.10', 'Operativo', 'CORE-SW-AB', 1),
                ('SW-AB-002', 'Switch', 'Andrés Bello', 'CFT Prat', '192.168.1.11', 'Operativo', 'CORE-SW-AB', 1),
                ('SW-AB-003', 'Switch', 'Andrés Bello', 'Zona ZM', '192.168.1.12', 'Operativo', 'CORE-SW-AB', 1),
                ('GAB-O-P3', 'Gabinete', 'Andrés Bello', 'Edificio O - Piso 3', '', 'Operativo', 'SW-AB-001', 2),
                ('GAB-CFT-01', 'Gabinete', 'Andrés Bello', 'CFT Prat - Entrada', '', 'Operativo', 'SW-AB-002', 2),
                ('GAB-ZM-01', 'Gabinete', 'Andrés Bello', 'Zona ZM - Ciclovia', '', 'Operativo', 'SW-AB-003', 2),
                ('UPS-O-P3', 'UPS', 'Andrés Bello', 'Edificio O - Piso 3 Sala Técnica', '', 'Operativo', 'GAB-O-P3', 3),
                ('NVR-CFT', 'NVR', 'Andrés Bello', 'CFT Prat - Sala Servidores', '192.168.1.50', 'Operativo', 'SW-AB-002', 2),
                
                # Campus Pucón
                ('CORE-SW-PUCON', 'Core_Switch', 'Pucón', 'Edificio Principal Pucón', '192.168.2.1', 'Operativo', '', 0),
                ('SW-PU-001', 'Switch', 'Pucón', 'Edificio A', '192.168.2.10', 'Operativo', 'CORE-SW-PUCON', 1),
                
                # Campus Angol
                ('CORE-SW-ANGOL', 'Core_Switch', 'Angol', 'Edificio Principal Angol', '192.168.3.1', 'Operativo', '', 0),
                ('SW-AN-001', 'Switch', 'Angol', 'Edificio Administrativo', '192.168.3.10', 'Operativo', 'CORE-SW-ANGOL', 1),
                
                # Campus Medicina
                ('CORE-SW-MED', 'Core_Switch', 'Medicina', 'Edificio Principal Medicina', '192.168.4.1', 'Operativo', '', 0),
                ('SW-MD-001', 'Switch', 'Medicina', 'Hospital Clínico', '192.168.4.10', 'Operativo', 'CORE-SW-MED', 1),
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO infraestructura_red 
                (componente_id, tipo_componente, campus, ubicacion, ip_address, estado, dependencias, nivel_jerarquico)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', infraestructura_data)
            
            conn.commit()
            print(f"✓ {len(infraestructura_data)} componentes de infraestructura insertados")
            print("\n✅ Infraestructura de red insertada exitosamente")
            
        except Exception as e:
            print(f"❌ Error insertando infraestructura: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def generar_reporte_final(self):
        """Genera un reporte final del estado de la base de datos"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            print("\n" + "="*60)
            print("=" + " "*18 + "REPORTE FINAL" + " "*27 + "=")
            print("="*60)
            
            # Contar registros en cada tabla
            tablas = [
                'camaras', 'fallas', 'tipos_fallas', 'casos_reales',
                'fallas_especificas', 'mantenimientos_realizados',
                'infraestructura_red', 'relaciones_componentes'
            ]
            
            print("\n📊 RESUMEN DE DATOS:")
            print("-" * 60)
            
            for tabla in tablas:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                    count = cursor.fetchone()[0]
                    print(f"  {tabla:.<40} {count:>5} registros")
                except:
                    print(f"  {tabla:.<40} {'N/A':>5}")
            
            # Mostrar casos reales
            print("\n📋 CASOS REALES INSERTADOS:")
            print("-" * 60)
            cursor.execute("SELECT nombre_caso, fecha_caso, tiempo_resolucion_horas FROM casos_reales ORDER BY fecha_caso")
            casos = cursor.fetchall()
            for i, (nombre, fecha, tiempo) in enumerate(casos, 1):
                print(f"  {i}. {nombre}")
                print(f"     Fecha: {fecha} | Tiempo resolución: {tiempo}h")
            
            # Mostrar tipos de fallas
            print("\n🚨 TIPOS DE FALLAS CONFIGURADOS:")
            print("-" * 60)
            cursor.execute("SELECT categoria, COUNT(*) FROM tipos_fallas GROUP BY categoria")
            categorias = cursor.fetchall()
            for categoria, count in categorias:
                print(f"  {categoria:.<40} {count:>3} tipos")
            
            # Mostrar infraestructura por campus
            print("\n🌐 INFRAESTRUCTURA POR CAMPUS:")
            print("-" * 60)
            cursor.execute("SELECT campus, COUNT(*) FROM infraestructura_red GROUP BY campus")
            campus_infra = cursor.fetchall()
            for campus, count in campus_infra:
                print(f"  {campus:.<40} {count:>3} componentes")
            
            print("\n" + "="*60)
            print("✅ BASE DE DATOS ACTUALIZADA EXITOSAMENTE")
            print("="*60)
            print("\n📁 Archivo: " + self.db_name)
            print("📅 Fecha actualización: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("\n" + "="*60)
            
        except Exception as e:
            print(f"❌ Error generando reporte: {str(e)}")
        finally:
            conn.close()
    
    def ejecutar_integracion_completa(self):
        """Ejecuta todo el proceso de integración"""
        print("\n" + "="*60)
        print("  INTEGRACIÓN COMPLETA - SISTEMA DE CÁMARAS UFRO")
        print("="*60)
        print(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("  Base de datos: " + self.db_name)
        print("="*60)
        
        # Paso 1: Crear tablas
        self.crear_tablas_base()
        
        # Paso 2: Insertar tipos de fallas
        self.insertar_tipos_fallas()
        
        # Paso 3: Insertar casos reales
        self.insertar_casos_reales()
        
        # Paso 4: Insertar fallas específicas
        self.insertar_fallas_especificas()
        
        # Paso 5: Insertar mantenimientos
        self.insertar_mantenimientos()
        
        # Paso 6: Insertar infraestructura de red
        self.insertar_infraestructura_ejemplo()
        
        # Paso 7: Generar reporte final
        self.generar_reporte_final()

def main():
    """Función principal"""
    integrador = IntegradorSistemaCamaras()
    integrador.ejecutar_integracion_completa()

if __name__ == "__main__":
    main()
