#!/usr/bin/env python3
"""
Script para agregar el cuarto caso real a la base de datos SQLite del sistema.
"""

import sqlite3
from datetime import datetime
import os

def agregar_caso_bd():
    """Agrega el cuarto caso real a la base de datos del sistema."""
    
    db_path = "/workspace/sistema_camaras.db"
    
    print("🔍 Conectando a la base de datos...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la tabla fallas existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fallas';")
        if not cursor.fetchone():
            print("❌ Tabla 'fallas' no existe. Creando tabla...")
            cursor.execute('''
                CREATE TABLE fallas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_reporte TEXT NOT NULL,
                    hora_reporte TEXT,
                    reportado_por TEXT,
                    tipo_falla TEXT NOT NULL,
                    subtipo TEXT,
                    camara_afectada TEXT,
                    ubicacion TEXT,
                    descripcion TEXT,
                    impacto_visibilidad TEXT,
                    afecta_vision_nocturna TEXT,
                    estado TEXT DEFAULT 'Reportado',
                    prioridad TEXT DEFAULT 'Media',
                    tecnico_asignado TEXT,
                    observaciones TEXT,
                    fecha_resolucion TEXT,
                    solucion_aplicada TEXT,
                    tiempo_resolucion TEXT
                )
            ''')
            print("✅ Tabla 'fallas' creada.")
        
        # Datos del cuarto caso
        caso_4 = {
            'fecha_reporte': '2025-10-17',
            'hora_reporte': '15:45',
            'reportado_por': 'Sistema Automático',
            'tipo_falla': 'Eléctrica',
            'subtipo': 'Corte de energía',
            'camara_afectada': 'ZM-container_Ciclovia, ZM-Ciclovia a AM, ZM-Bodega_Ciclovia',
            'ubicacion': 'Zona ZM - Ciclovia',
            'descripcion': 'Caída simultánea de 3 cámaras del ZM por falla eléctrica. Automático desconectado en caseta guardia frente a taller.',
            'impacto_visibilidad': 'Alto',
            'afecta_vision_nocturna': 'Sí',
            'estado': 'Resuelto',
            'prioridad': 'Alta',
            'tecnico_asignado': 'Marco Contreras',
            'observaciones': 'Automático ubicado fuera de los gabinetes principales, en caseta guardia frente a taller. Reparación realizada por encargado de seguridad.',
            'fecha_resolucion': '2025-10-17',
            'solucion_aplicada': 'Subir automático en caseta guardia',
            'tiempo_resolucion': '15 minutos'
        }
        
        print("\n📝 Insertando caso en la base de datos...")
        
        # Insertar el nuevo caso
        cursor.execute('''
            INSERT INTO fallas (
                fecha_reporte, hora_reporte, reportado_por, tipo_falla, subtipo,
                camara_afectada, ubicacion, descripcion, impacto_visibilidad,
                afecta_vision_nocturna, estado, prioridad, tecnico_asignado,
                observaciones, fecha_resolucion, solucion_aplicada, tiempo_resolucion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            caso_4['fecha_reporte'], caso_4['hora_reporte'], caso_4['reportado_por'],
            caso_4['tipo_falla'], caso_4['subtipo'], caso_4['camara_afectada'],
            caso_4['ubicacion'], caso_4['descripcion'], caso_4['impacto_visibilidad'],
            caso_4['afecta_vision_nocturna'], caso_4['estado'], caso_4['prioridad'],
            caso_4['tecnico_asignado'], caso_4['observaciones'], caso_4['fecha_resolucion'],
            caso_4['solucion_aplicada'], caso_4['tiempo_resolucion']
        ))
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar que se insertó correctamente
        cursor.execute("SELECT COUNT(*) FROM fallas")
        total_fallas = cursor.fetchone()[0]
        
        cursor.execute("SELECT id, fecha_reporte, descripcion FROM fallas ORDER BY id DESC LIMIT 1")
        ultimo_caso = cursor.fetchone()
        
        print(f"✅ Caso insertado exitosamente!")
        print(f"📊 Total de fallas en BD: {total_fallas}")
        print(f"🆔 Último caso: ID {ultimo_caso[0]} - {ultimo_caso[1]} - {ultimo_caso[2]}")
        
        # Mostrar resumen de todos los casos
        cursor.execute("SELECT id, fecha_reporte, tipo_falla, estado FROM fallas ORDER BY fecha_reporte DESC")
        casos = cursor.fetchall()
        
        print("\n📋 RESUMEN DE TODOS LOS CASOS EN BD:")
        print("="*60)
        for caso in casos:
            print(f"ID {caso[0]}: {caso[1]} - {caso[2]} - {caso[3]}")
        
        conn.close()
        print(f"\n🎉 ¡Cuarto caso agregado exitosamente a la base de datos!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Agregando cuarto caso real a la base de datos...")
    print("="*50)
    agregar_caso_bd()