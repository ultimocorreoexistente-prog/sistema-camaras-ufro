#!/usr/bin/env python3
"""
Script para agregar Caso 5: Falla Fibra Óptica Bicicletero Principal

Fecha del incidente: 16/10/2025
Autor: MiniMax Agent
Fecha script: 2025-10-20
"""

import sqlite3
import json
from datetime import datetime, timedelta

def agregar_caso_5():
    """Agrega el Caso 5 a la base de datos"""
    
    db_path = 'sistema_camaras.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("\n" + "="*70)
        print(" "*15 + "AGREGANDO CASO 5 - BICICLETERO")
        print("="*70)
        
        # Calcular tiempo de resolución
        # Asumiendo que se reportó temprano en la mañana (ej: 08:00)
        # y se resolvió a las 16:57
        hora_reporte = "08:00"  # Estimado
        hora_resolucion = "16:57"
        # Aproximadamente 8h 57min = 8.95 horas
        tiempo_resolucion = 8.95
        
        print("\n📋 INFORMACIÓN DEL CASO:")
        print("-" * 70)
        print("  Fecha: 16/10/2025 (Jueves)")
        print("  Ubicación: Bicicletero Principal")
        print("  Problema: Todas las cámaras caídas por falla de fibra óptica")
        print("  Hora resolución: 16:57")
        print(f"  Tiempo estimado: {tiempo_resolucion}h")
        
        # PASO 1: Insertar caso real
        print("\n🔧 Insertando caso real...")
        cursor.execute('''
            INSERT OR REPLACE INTO casos_reales (
                nombre_caso, fecha_caso, descripcion,
                componentes_involucrados, dependencias_cascada,
                solucion_aplicada, tiempo_resolucion_horas,
                lecciones_aprendidas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Falla Fibra Óptica Bicicletero Principal',
            '2025-10-16',
            'Todas las cámaras del Bicicletero Principal perdieron conexión por falla en cable de fibra óptica proveniente del Edificio L (Odontología)',
            json.dumps([
                'Gabinete Bicicletero Principal',
                'Switch Bicicletero',
                'Fuente de poder Bicicletero',
                'Cable fibra óptica Edificio L → Bicicletero',
                'Todas las cámaras Bicicletero Principal'
            ]),
            json.dumps([
                'Dinfo (Sistema Central) → Fibra → Edificio Matemáticas',
                'Edificio Matemáticas → Fibra → Edificio L (Odontología)',
                'Edificio L (Odontología) → Fibra → Bicicletero Principal',
                'Bicicletero Principal: Switch + Fuente → Cámaras'
            ]),
            'Apertura de gabinete, identificación de cable fibra suelto, reconexión del cable de fibra óptica',
            tiempo_resolucion,
            'Puntos críticos de falla en enlaces de fibra óptica de larga distancia. Necesidad de monitoreo de conectividad de enlaces críticos. Documentar topología completa de red de fibra. El Bicicletero depende de una cadena de 3 enlaces de fibra (Dinfo→Matemáticas→Odontología→Bicicletero).'
        ))
        print("  ✓ Caso real insertado")
        
        # PASO 2: Insertar falla específica
        print("\n🚨 Insertando falla específica...")
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
            '2025-10-16',
            'Falla de conectividad',
            'Cable fibra óptica',
            'fibra-edificio-l-bicicletero',
            'Cable de fibra óptica desconectado entre Edificio L (Odontología) y Bicicletero Principal. No llegaba señal al switch del gabinete.',
            json.dumps(['Todas las cámaras Bicicletero Principal']),
            tiempo_resolucion,
            'Reconexión de cable de fibra óptica en gabinete Bicicletero. Señal recuperada a las 16:57.',
            '2025-10-16',
            'Personal técnico',
            0,
            'Resuelto',
            'Alta',
            'Andrés Bello',
            'El Bicicletero Principal depende de enlace de fibra desde Edificio L. Topología: Dinfo → Matemáticas → Odontología → Bicicletero. Gabinete contiene 1 switch + 1 fuente de poder.'
        ))
        print("  ✓ Falla específica insertada")
        
        # PASO 3: Actualizar/Agregar infraestructura de red
        print("\n🌐 Actualizando infraestructura de red...")
        
        # Agregar componentes de la topología identificada
        infraestructura_nueva = [
            # Dinfo (Sistema Central)
            ('CORE-DINFO', 'Core_System', 'Andrés Bello', 'Dirección de Informática (Dinfo) - Sistema Central', '', 'Operativo', '', 0),
            
            # Edificio Matemáticas
            ('SW-MATEMATICAS', 'Switch', 'Andrés Bello', 'Edificio Matemáticas', '', 'Operativo', 'CORE-DINFO', 1),
            
            # Edificio L (Odontología)
            ('SW-ODONTOLOGIA', 'Switch', 'Andrés Bello', 'Edificio L (Odontología)', '', 'Operativo', 'SW-MATEMATICAS', 2),
            
            # Bicicletero Principal
            ('GAB-BICICLETERO', 'Gabinete', 'Andrés Bello', 'Bicicletero Principal', '', 'Operativo', 'SW-ODONTOLOGIA', 3),
            ('SW-BICICLETERO', 'Switch', 'Andrés Bello', 'Bicicletero Principal - Gabinete', '', 'Operativo', 'GAB-BICICLETERO', 4),
            ('FP-BICICLETERO', 'Fuente_Poder', 'Andrés Bello', 'Bicicletero Principal - Gabinete', '', 'Operativo', 'GAB-BICICLETERO', 4),
            
            # Enlaces de fibra
            ('FIBRA-DINFO-MAT', 'Enlace_Fibra', 'Andrés Bello', 'Dinfo → Matemáticas', '', 'Operativo', 'CORE-DINFO', 1),
            ('FIBRA-MAT-ODON', 'Enlace_Fibra', 'Andrés Bello', 'Matemáticas → Odontología', '', 'Operativo', 'SW-MATEMATICAS', 2),
            ('FIBRA-ODON-BICI', 'Enlace_Fibra', 'Andrés Bello', 'Odontología → Bicicletero', '', 'Reparado', 'SW-ODONTOLOGIA', 3),
        ]
        
        for componente in infraestructura_nueva:
            cursor.execute('''
                INSERT OR REPLACE INTO infraestructura_red 
                (componente_id, tipo_componente, campus, ubicacion, ip_address, estado, dependencias, nivel_jerarquico)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', componente)
        
        print(f"  ✓ {len(infraestructura_nueva)} componentes de infraestructura agregados/actualizados")
        
        # PASO 4: Agregar relaciones entre componentes
        print("\n🔗 Agregando relaciones de componentes...")
        
        relaciones = [
            ('CORE-DINFO', 'FIBRA-DINFO-MAT', 'Alimenta'),
            ('FIBRA-DINFO-MAT', 'SW-MATEMATICAS', 'Conecta'),
            ('SW-MATEMATICAS', 'FIBRA-MAT-ODON', 'Alimenta'),
            ('FIBRA-MAT-ODON', 'SW-ODONTOLOGIA', 'Conecta'),
            ('SW-ODONTOLOGIA', 'FIBRA-ODON-BICI', 'Alimenta'),
            ('FIBRA-ODON-BICI', 'GAB-BICICLETERO', 'Conecta'),
            ('GAB-BICICLETERO', 'SW-BICICLETERO', 'Contiene'),
            ('GAB-BICICLETERO', 'FP-BICICLETERO', 'Contiene'),
        ]
        
        for padre, hijo, tipo in relaciones:
            cursor.execute('''
                INSERT OR REPLACE INTO relaciones_componentes 
                (componente_padre, componente_hijo, tipo_relacion)
                VALUES (?, ?, ?)
            ''', (padre, hijo, tipo))
        
        print(f"  ✓ {len(relaciones)} relaciones agregadas")
        
        conn.commit()
        print("\n" + "="*70)
        print("✅ CASO 5 AGREGADO EXITOSAMENTE")
        print("="*70)
        
        # Mostrar resumen actualizado
        print("\n📊 RESUMEN ACTUALIZADO:")
        print("-" * 70)
        
        cursor.execute("SELECT COUNT(*) FROM casos_reales")
        print(f"  Casos reales totales: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM fallas_especificas")
        print(f"  Fallas específicas totales: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM infraestructura_red")
        print(f"  Componentes infraestructura: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM relaciones_componentes")
        print(f"  Relaciones componentes: {cursor.fetchone()[0]}")
        
        # Mostrar todos los casos
        print("\n📋 CASOS REALES DOCUMENTADOS:")
        print("-" * 70)
        cursor.execute("""
            SELECT nombre_caso, fecha_caso, tiempo_resolucion_horas 
            FROM casos_reales 
            ORDER BY fecha_caso
        """)
        for i, (nombre, fecha, tiempo) in enumerate(cursor.fetchall(), 1):
            print(f"  {i}. [{fecha}] {nombre} ({tiempo}h)")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    agregar_caso_5()
