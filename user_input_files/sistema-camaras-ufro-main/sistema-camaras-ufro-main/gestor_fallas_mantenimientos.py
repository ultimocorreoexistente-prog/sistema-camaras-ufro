#!/usr/bin/env python3
"""
Módulo de Gestión de Fallas y Mantenimientos
Sistema de Cámaras UFRO - Procesamiento de INFORMEDECAMARAS.docx
"""

import os
import pandas as pd
from datetime import datetime
import sqlite3
import json
from typing import Dict, List, Optional
import logging

class GestorFallasMantenimientos:
    """Gestor de fallas y mantenimientos de cámaras"""
    
    def __init__(self, db_path='camaras_ufro.db'):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.crear_tablas_fallas()
    
    def crear_tablas_fallas(self):
        """Crea las tablas necesarias para gestión de fallas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de fallas/incidencias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fallas_camaras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                camara_nombre TEXT NOT NULL,
                camara_ip TEXT,
                ubicacion TEXT,
                edificio TEXT,
                tipo_falla TEXT,
                descripcion_falla TEXT,
                estado TEXT DEFAULT 'PENDIENTE',
                fecha_reporte DATE,
                fecha_deteccion DATETIME,
                archivo_origen TEXT,
                prioridad TEXT DEFAULT 'MEDIA',
                tecnico_asignado TEXT,
                observaciones TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de historial de mantenimientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial_mantenimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                falla_id INTEGER,
                camara_nombre TEXT NOT NULL,
                accion_realizada TEXT,
                tipo_mantenimiento TEXT,
                descripcion TEXT,
                tecnico TEXT,
                fecha_inicio DATETIME,
                fecha_finalizacion DATETIME,
                estado_anterior TEXT,
                estado_nuevo TEXT,
                observaciones TEXT,
                materiales_usados TEXT,
                costo_estimado REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (falla_id) REFERENCES fallas_camaras (id)
            )
        ''')
        
        # Tabla de estados de cámaras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estados_camaras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                camara_nombre TEXT NOT NULL,
                camara_ip TEXT,
                estado_operativo TEXT,
                estado_fisico TEXT,
                ultimo_mantenimiento DATE,
                proxima_revision DATE,
                observaciones_estado TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de tipos de fallas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipos_fallas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE,
                categoria TEXT,
                prioridad_default TEXT,
                tiempo_resolucion_estimado INTEGER,
                descripcion TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insertar tipos de fallas comunes
        self.insertar_tipos_fallas_iniciales()
    
    def insertar_tipos_fallas_iniciales(self):
        """Inserta tipos de fallas comunes del sistema"""
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
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for tipo in tipos_fallas:
            cursor.execute('''
                INSERT OR IGNORE INTO tipos_fallas 
                (nombre, categoria, prioridad_default, tiempo_resolucion_estimado, descripcion)
                VALUES (?, ?, ?, ?, ?)
            ''', tipo)
        
        conn.commit()
        conn.close()
    
    def procesar_informe_docx(self, archivo_path: str) -> Dict:
        """Procesa archivo INFORMEDECAMARAS.docx y extrae fallas"""
        try:
            # Intentar leer como DOCX usando python-docx si está disponible
            try:
                from docx import Document
                doc = Document(archivo_path)
                texto_completo = '\n'.join([p.text for p in doc.paragraphs])
            except ImportError:
                # Fallback: convertir DOCX a texto plano
                texto_completo = self.extraer_texto_docx_fallback(archivo_path)
            
            # Procesar el texto extraído
            fallas_detectadas = self.analizar_texto_fallas(texto_completo)
            
            # Guardar en base de datos
            fallas_guardadas = self.guardar_fallas_detectadas(fallas_detectadas, archivo_path)
            
            return {
                'exito': True,
                'archivo_procesado': archivo_path,
                'fallas_detectadas': len(fallas_detectadas),
                'fallas_guardadas': len(fallas_guardadas),
                'fecha_procesamiento': datetime.now().isoformat(),
                'detalle_fallas': fallas_guardadas
            }
            
        except Exception as e:
            self.logger.error(f"Error procesando DOCX: {e}")
            return {
                'exito': False,
                'error': str(e),
                'archivo_procesado': archivo_path
            }
    
    def extraer_texto_docx_fallback(self, archivo_path: str) -> str:
        """Método fallback para extraer texto de DOCX"""
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            
            texto = []
            with zipfile.ZipFile(archivo_path, 'r') as docx:
                xml_content = docx.read('word/document.xml')
                tree = ET.XML(xml_content)
                
                for paragraph in tree.iter():
                    if paragraph.text:
                        texto.append(paragraph.text)
            
            return '\n'.join(texto)
            
        except Exception as e:
            self.logger.error(f"Error en extracción fallback: {e}")
            return ""
    
    def analizar_texto_fallas(self, texto: str) -> List[Dict]:
        """Analiza el texto del informe y detecta fallas"""
        fallas = []
        lineas = texto.split('\n')
        
        # Patrones de búsqueda para diferentes tipos de fallas
        patrones_fallas = {
            'telaraña': ['telaraña', 'telarañas', 'araña', 'web'],
            'suciedad': ['sucia', 'suciedad', 'mancha', 'manchas', 'polvo'],
            'mica_rayada': ['rayada', 'rayado', 'rayones', 'mica dañada'],
            'sin_imagen': ['sin imagen', 'no funciona', 'fuera de servicio', 'offline'],
            'borrosa': ['borrosa', 'desenfocada', 'mala calidad'],
            'desalineada': ['desalineada', 'mal posición', 'angulo incorrecto'],
            'conectividad': ['sin conexión', 'desconectada', 'red', 'ip'],
        }
        
        for i, linea in enumerate(lineas):
            linea_lower = linea.lower().strip()
            
            if len(linea_lower) < 5:  # Saltar líneas muy cortas
                continue
            
            # Buscar patrones de fallas
            for tipo_falla, patrones in patrones_fallas.items():
                for patron in patrones:
                    if patron in linea_lower:
                        falla = self.extraer_datos_falla(linea, tipo_falla, i)
                        if falla:
                            fallas.append(falla)
                        break
        
        return fallas
    
    def extraer_datos_falla(self, linea: str, tipo_falla: str, numero_linea: int) -> Dict:
        """Extrae datos específicos de una línea que contiene una falla"""
        import re
        
        # Buscar patrones de cámara e IP
        patron_camara = r'([A-Za-z0-9_-]+(?:cam|cámara|CAM)[A-Za-z0-9_-]*)'
        patron_ip = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        patron_edificio = r'(ED-[A-Za-z0-9]+|[A-Za-z]+-\d+|Edificio\s+[A-Za-z0-9]+)'
        
        camara_match = re.search(patron_camara, linea, re.IGNORECASE)
        ip_match = re.search(patron_ip, linea)
        edificio_match = re.search(patron_edificio, linea, re.IGNORECASE)
        
        # Mapear tipos de fallas
        mapeo_fallas = {
            'telaraña': 'Suciedad por telaraña',
            'suciedad': 'Manchas en lente',
            'mica_rayada': 'Mica rayada',
            'sin_imagen': 'Cámara sin imagen',
            'borrosa': 'Imagen borrosa',
            'desalineada': 'Cámara desalineada',
            'conectividad': 'Falla de conectividad'
        }
        
        return {
            'camara_nombre': camara_match.group(1) if camara_match else f'Cámara_línea_{numero_linea}',
            'camara_ip': ip_match.group(1) if ip_match else None,
            'edificio': edificio_match.group(1) if edificio_match else 'Por determinar',
            'tipo_falla': mapeo_fallas.get(tipo_falla, 'Falla general'),
            'descripcion_falla': linea.strip(),
            'ubicacion': f'Línea {numero_linea} del informe',
            'prioridad': self.determinar_prioridad(tipo_falla),
            'fecha_deteccion': datetime.now()
        }
    
    def determinar_prioridad(self, tipo_falla: str) -> str:
        """Determina la prioridad basada en el tipo de falla"""
        prioridades = {
            'sin_imagen': 'CRITICA',
            'conectividad': 'ALTA',
            'mica_rayada': 'ALTA',
            'borrosa': 'MEDIA',
            'desalineada': 'MEDIA',
            'telaraña': 'MEDIA',
            'suciedad': 'MEDIA'
        }
        return prioridades.get(tipo_falla, 'MEDIA')
    
    def guardar_fallas_detectadas(self, fallas: List[Dict], archivo_origen: str) -> List[Dict]:
        """Guarda las fallas detectadas en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fallas_guardadas = []
        
        for falla in fallas:
            try:
                cursor.execute('''
                    INSERT INTO fallas_camaras 
                    (camara_nombre, camara_ip, ubicacion, edificio, tipo_falla, 
                     descripcion_falla, fecha_reporte, fecha_deteccion, archivo_origen, prioridad)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    falla['camara_nombre'],
                    falla['camara_ip'],
                    falla['ubicacion'],
                    falla['edificio'],
                    falla['tipo_falla'],
                    falla['descripcion_falla'],
                    datetime.now().date(),
                    falla['fecha_deteccion'],
                    archivo_origen,
                    falla['prioridad']
                ))
                
                falla_id = cursor.lastrowid
                falla['id'] = falla_id
                fallas_guardadas.append(falla)
                
            except Exception as e:
                self.logger.error(f"Error guardando falla: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return fallas_guardadas
    
    def marcar_falla_resuelta(self, falla_id: int, tecnico: str, descripcion_solucion: str) -> bool:
        """Marca una falla como resuelta y crea registro de mantenimiento"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Actualizar estado de la falla
            cursor.execute('''
                UPDATE fallas_camaras 
                SET estado = 'RESUELTA', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (falla_id,))
            
            # Obtener datos de la falla
            cursor.execute('SELECT * FROM fallas_camaras WHERE id = ?', (falla_id,))
            falla = cursor.fetchone()
            
            if falla:
                # Crear registro de mantenimiento
                cursor.execute('''
                    INSERT INTO historial_mantenimientos
                    (falla_id, camara_nombre, accion_realizada, tipo_mantenimiento,
                     descripcion, tecnico, fecha_inicio, fecha_finalizacion,
                     estado_anterior, estado_nuevo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    falla_id,
                    falla[1],  # camara_nombre
                    'Resolución de falla',
                    self.determinar_tipo_mantenimiento(falla[5]),  # tipo_falla
                    descripcion_solucion,
                    tecnico,
                    datetime.now(),
                    datetime.now(),
                    'PENDIENTE',
                    'RESUELTA'
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Error marcando falla resuelta: {e}")
            return False
    
    def determinar_tipo_mantenimiento(self, tipo_falla: str) -> str:
        """Determina el tipo de mantenimiento según la falla"""
        mapeo = {
            'Suciedad por telaraña': 'LIMPIEZA',
            'Manchas en lente': 'LIMPIEZA',
            'Mica rayada': 'REPARACION',
            'Cámara sin imagen': 'REPARACION_TECNICA',
            'Imagen borrosa': 'CALIBRACION',
            'Cámara desalineada': 'AJUSTE',
            'Falla de conectividad': 'REPARACION_TECNICA'
        }
        return mapeo.get(tipo_falla, 'MANTENIMIENTO_GENERAL')
    
    def obtener_fallas_pendientes(self) -> List[Dict]:
        """Obtiene todas las fallas pendientes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM fallas_camaras 
            WHERE estado = 'PENDIENTE'
            ORDER BY 
                CASE prioridad 
                    WHEN 'CRITICA' THEN 1
                    WHEN 'ALTA' THEN 2
                    WHEN 'MEDIA' THEN 3
                    ELSE 4
                END,
                fecha_deteccion ASC
        ''')
        
        fallas = cursor.fetchall()
        conn.close()
        
        return [self.fila_a_dict(falla) for falla in fallas]
    
    def obtener_estadisticas_fallas(self) -> Dict:
        """Obtiene estadísticas generales de fallas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total por estado
        cursor.execute('SELECT estado, COUNT(*) FROM fallas_camaras GROUP BY estado')
        stats['por_estado'] = dict(cursor.fetchall())
        
        # Total por tipo
        cursor.execute('SELECT tipo_falla, COUNT(*) FROM fallas_camaras GROUP BY tipo_falla')
        stats['por_tipo'] = dict(cursor.fetchall())
        
        # Total por prioridad
        cursor.execute('SELECT prioridad, COUNT(*) FROM fallas_camaras GROUP BY prioridad')
        stats['por_prioridad'] = dict(cursor.fetchall())
        
        # Resueltas en los últimos 30 días
        cursor.execute('''
            SELECT COUNT(*) FROM fallas_camaras 
            WHERE estado = 'RESUELTA' AND updated_at >= date('now', '-30 days')
        ''')
        stats['resueltas_ultimo_mes'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def fila_a_dict(self, fila) -> Dict:
        """Convierte una fila de base de datos a diccionario"""
        columnas = [
            'id', 'camara_nombre', 'camara_ip', 'ubicacion', 'edificio',
            'tipo_falla', 'descripcion_falla', 'estado', 'fecha_reporte',
            'fecha_deteccion', 'archivo_origen', 'prioridad', 'tecnico_asignado',
            'observaciones', 'created_at', 'updated_at'
        ]
        return dict(zip(columnas, fila))

# Función de utilidad para pruebas
def probar_gestor_fallas():
    """Prueba el gestor de fallas"""
    gestor = GestorFallasMantenimientos()
    
    # Simular procesamiento de informe
    texto_ejemplo = """
    Reporte de fallas de cámaras - 18/10/2025
    
    - CAM_2030_01 (IP: 172.22.3.9) en ED-2030: Lente con telarañas
    - Cámara_Aulas_B2 (IP: 192.168.1.55): Imagen borrosa
    - CAM_Biblioteca_P3: Sin imagen, posible falla eléctrica
    - Cámara_Ingeniería_A1: Mica rayada, necesita reemplazo
    """
    
    fallas = gestor.analizar_texto_fallas(texto_ejemplo)
    print(f"Fallas detectadas: {len(fallas)}")
    
    for falla in fallas:
        print(f"- {falla['camara_nombre']}: {falla['tipo_falla']}")
    
    return gestor

if __name__ == "__main__":
    probar_gestor_fallas()