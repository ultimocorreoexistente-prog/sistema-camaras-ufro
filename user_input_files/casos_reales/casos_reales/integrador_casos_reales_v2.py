#!/usr/bin/env python3
"""
Integrador de Casos Reales (Corregido) - Sistema UFRO
===================================================

Script corregido para integrar los casos reales usando la estructura
real de la base de datos del sistema.

Autor: MiniMax Agent
Fecha: 2025-10-18
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path

class IntegradorCasosRealesV2:
    def __init__(self, base_path='/workspace'):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / 'sistema_camaras.db'
        self.casos_path = self.base_path / 'casos_reales'
        self.casos_path.mkdir(exist_ok=True)
        
        # Verificar y mostrar estructura de DB
        self.verificar_estructura_db()
    
    def verificar_estructura_db(self):
        """Verifica y muestra la estructura actual de la base de datos"""
        print("🗺️ Verificando estructura de base de datos...")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [table[0] for table in cursor.fetchall()]
            
        print(f"Tablas disponibles: {', '.join(tables)}")
        return tables
    
    def insertar_casos_semana_v2(self):
        """Inserta los casos reales usando la estructura real de DB"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # CASO 1: Insertar en casos_reales
                caso_edificio_o = """
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion, 
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas, created_at
                ) VALUES (
                    'Mantenimiento UPS Edificio O',
                    '2024-10-13',
                    'Cambio preventivo de 1 batería del UPS APC Smart-UPS SC 1500VA en sala técnica tercer piso Edificio O',
                    '["UPS APC Smart-UPS SC 1500VA", "Batería RBC7 12V 17Ah", "11 cámaras Edificio O", "1 cámara PTZ Francisco Salazar vía fibra"]',
                    '["Switch Edificio O", "Enlace fibra óptica", "Gabinete subterráneo Francisco Salazar", "Cámara PTZ remota"]',
                    'Cambio exitoso de batería con sistema funcionando en batería restante',
                    2.5,
                    'Importancia de tener baterías redundantes para evitar corte total durante mantenimiento. Considerar ventana de mantenimiento para equipos críticos.',
                    datetime.now().isoformat()
                )
                """
                
                conn.execute(caso_edificio_o)
                
                # CASO 2: Falla CFT Prat
                caso_cft_prat = """
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion,
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas, created_at
                ) VALUES (
                    'Falla Cable NVR CFT Prat',
                    '2024-10-14',
                    '13 cámaras del CFT Prat perdieron conexión simultáneamente por cable suelto entre NVR e internet',
                    '["NVR CFT Prat", "Cable ethernet NVR-Internet", "13 cámaras CFT Prat", "Router Cisco CFT"]',
                    '["Todas las cámaras CFT dependen de un solo NVR", "NVR depende de una sola conexión a internet", "Sin redundancia de conectividad"]',
                    'Reconexión y ajuste del cable ethernet, verificación de todas las conexiones',
                    26.5,
                    'Necesidad de implementar redundancia en ubicaciones con múltiples cámaras. Revisar todas las instalaciones de subcontratistas.',
                    datetime.now().isoformat()
                )
                """
                
                conn.execute(caso_cft_prat)
                
                # Insertar falla específica para CFT Prat
                falla_cft = """
                INSERT OR REPLACE INTO fallas_especificas (
                    fecha_falla, tipo_falla, componente_afectado_tipo,
                    componente_afectado_id, descripcion_falla,
                    camaras_afectadas, tiempo_downtime_horas,
                    solucion_aplicada, fecha_resolucion,
                    tecnico_reparador, costo_reparacion,
                    estado, prioridad
                ) VALUES (
                    '2024-10-14',
                    'Cable suelto',
                    'Cable ethernet',
                    'cable-nvr-internet-cft',
                    'Cable que conecta NVR con internet estaba suelto, causando pérdida total de conectividad',
                    '["cam-cft-1","cam-cft-2","cam-cft-3","cam-cft-4","cam-cft-5","cam-cft-6","cam-cft-7","cam-cft-8","cam-cft-9","cam-cft-10","cam-cft-11","cam-cft-12","cam-cft-13"]',
                    26.5,
                    'Reconexión del cable ethernet y verificación de todas las conexiones del rack',
                    '2024-10-15',
                    'Juan Pérez (Personal CFT)',
                    0,
                    'Resuelto',
                    'Alta'
                )
                """
                
                conn.execute(falla_cft)
                
                # Insertar mantenimiento para Edificio O
                mant_edificio_o = """
                INSERT OR REPLACE INTO mantenimientos_realizados (
                    fecha_mantenimiento, tipo_mantenimiento,
                    componente_tipo, componente_id,
                    descripcion_trabajo, materiales_utilizados,
                    tecnico_responsable, duracion_horas,
                    costo_total, resultado, observaciones,
                    created_at
                ) VALUES (
                    '2024-10-13',
                    'Preventivo',
                    'UPS',
                    'ups-edificio-o-p3',
                    'Cambio preventivo de 1 batería UPS APC Smart-UPS SC 1500VA',
                    '["Batería RBC7 - 12V 17Ah x1"]',
                    'Personal interno',
                    2.5,
                    45000,
                    'Exitoso',
                    '11 cámaras temporalmente en riesgo durante cambio. Sistema funcionó con batería restante.',
                    datetime.now().isoformat()
                )
                """
                
                conn.execute(mant_edificio_o)
                
                conn.commit()
                print("✅ Casos reales insertados correctamente en la estructura real de DB")
                return True
                
        except Exception as e:
            print(f"❌ Error insertando casos: {e}")
            return False
    
    def generar_consultas_casos_reales(self):
        """Genera consultas específicas para los casos reportados"""
        
        print("\n🔍 CONSULTAS ESPECÍFICAS - CASOS REALES")
        print("=" * 50)
        
        with sqlite3.connect(self.db_path) as conn:
            
            # 1. Consulta de casos de esta semana
            print("\n1️⃣ CASOS REPORTADOS ESTA SEMANA:")
            query_casos = """
            SELECT 
                nombre_caso,
                fecha_caso,
                tiempo_resolucion_horas,
                descripcion,
                lecciones_aprendidas
            FROM casos_reales 
            WHERE fecha_caso >= '2024-10-13'
            ORDER BY fecha_caso DESC
            """
            
            casos = pd.read_sql_query(query_casos, conn)
            for _, caso in casos.iterrows():
                print(f"\n📅 {caso['fecha_caso']} - {caso['nombre_caso']}")
                print(f"   Duración: {caso['tiempo_resolucion_horas']} horas")
                print(f"   Descripción: {caso['descripcion'][:80]}...")
                print(f"   Lección: {caso['lecciones_aprendidas'][:80]}...")
            
            # 2. Fallas por tipo
            print("\n\n2️⃣ FALLAS POR TIPO (ESTA SEMANA):")
            query_fallas = """
            SELECT 
                tipo_falla,
                COUNT(*) as cantidad,
                AVG(tiempo_downtime_horas) as promedio_horas_caida,
                SUM(costo_reparacion) as costo_total
            FROM fallas_especificas 
            WHERE fecha_falla >= '2024-10-13'
            GROUP BY tipo_falla
            ORDER BY cantidad DESC
            """
            
            fallas = pd.read_sql_query(query_fallas, conn)
            for _, falla in fallas.iterrows():
                print(f"🚫 {falla['tipo_falla']}: {falla['cantidad']} casos")
                print(f"   Promedio caída: {falla['promedio_horas_caida']:.1f} horas")
                print(f"   Costo total: ${falla['costo_total']:,.0f}")
            
            # 3. Mantenimientos realizados
            print("\n\n3️⃣ MANTENIMIENTOS REALIZADOS:")
            query_mant = """
            SELECT 
                fecha_mantenimiento,
                tipo_mantenimiento,
                componente_tipo,
                descripcion_trabajo,
                duracion_horas,
                costo_total
            FROM mantenimientos_realizados 
            WHERE fecha_mantenimiento >= '2024-10-13'
            ORDER BY fecha_mantenimiento DESC
            """
            
            mantenimientos = pd.read_sql_query(query_mant, conn)
            for _, mant in mantenimientos.iterrows():
                print(f"🔧 {mant['fecha_mantenimiento']} - {mant['tipo_mantenimiento']}")
                print(f"   Componente: {mant['componente_tipo']}")
                print(f"   Trabajo: {mant['descripcion_trabajo'][:60]}...")
                print(f"   Duración: {mant['duracion_horas']} horas")
                print(f"   Costo: ${mant['costo_total']:,.0f}")
    
    def consulta_dependencias_edificio_o(self):
        """Consulta las dependencias del caso Edificio O"""
        
        print("\n\n🏢 ANÁLISIS DE DEPENDENCIAS - EDIFICIO O")
        print("=" * 50)
        
        # Simulación de la consulta bidireccional
        dependencias = {
            "rack_principal": {
                "ubicacion": "Edificio O - Piso 3 - Sala técnica",
                "equipos_contenidos": [
                    "UPS APC Smart-UPS SC 1500VA",
                    "Switch Cisco SG350-28P (24 puertos)",
                    "Panel de fibra óptica"
                ]
            },
            "camaras_dependientes_directas": {
                "cantidad": 11,
                "ubicaciones": [
                    "Edificio O - 1er piso (3 cámaras)",
                    "Edificio O - 2do piso (2 cámaras)", 
                    "Edificio O - 3er piso (3 cámaras)",
                    "Edificio O - 4to piso (2 cámaras)",
                    "Edificio O - Exterior 3er piso (1 PTZ)"
                ]
            },
            "dependencias_remotas": {
                "enlace_fibra": "Edificio O → Gabinete subterráneo Francisco Salazar",
                "equipos_remotos": [
                    "Switch remoto (8 puertos)",
                    "POE adicional para PTZ",
                    "Cámara PTZ Francisco Salazar"
                ]
            },
            "analisis_impacto": {
                "durante_mantenimiento": "11 cámaras locales en riesgo por 2.5 horas",
                "si_falla_ups": "12 cámaras afectadas (11 locales + 1 remota por fibra)",
                "si_falla_switch": "12 cámaras afectadas + pérdida enlace remoto",
                "tiempo_autonomia_ups": "45 minutos con 2 baterías"
            }
        }
        
        print("📋 RACK PRINCIPAL:")
        print(f"   Ubicación: {dependencias['rack_principal']['ubicacion']}")
        for equipo in dependencias['rack_principal']['equipos_contenidos']:
            print(f"   • {equipo}")
        
        print("\n📹 CÁMARAS DEPENDIENTES DIRECTAS:")
        print(f"   Total: {dependencias['camaras_dependientes_directas']['cantidad']} cámaras")
        for ubicacion in dependencias['camaras_dependientes_directas']['ubicaciones']:
            print(f"   • {ubicacion}")
        
        print("\n🌐 DEPENDENCIAS REMOTAS:")
        print(f"   Enlace: {dependencias['dependencias_remotas']['enlace_fibra']}")
        for equipo in dependencias['dependencias_remotas']['equipos_remotos']:
            print(f"   • {equipo}")
        
        print("\n⚠️  ANÁLISIS DE IMPACTO:")
        for scenario, impacto in dependencias['analisis_impacto'].items():
            print(f"   • {scenario.replace('_', ' ').title()}: {impacto}")
        
        return dependencias
    
    def consulta_riesgo_puntos_unicos_falla(self):
        """Identifica otros puntos únicos de falla como CFT Prat"""
        
        print("\n\n🚨 IDENTIFICACIÓN DE PUNTOS ÚNICOS DE FALLA")
        print("=" * 50)
        
        # Datos simulados basados en el análisis
        puntos_criticos = [
            {
                "ubicacion": "CFT Prat",
                "camaras_dependientes": 13,
                "punto_critico": "Cable NVR-Internet",
                "falla_registrada": "14-10-2024 (26.5 horas caída)",
                "riesgo": "ALTO"
            },
            {
                "ubicacion": "Edificio O",
                "camaras_dependientes": 12,
                "punto_critico": "UPS único",
                "falla_registrada": "Mantenimiento preventivo",
                "riesgo": "MEDIO-ALTO"
            },
            {
                "ubicacion": "Francisco Salazar (remoto)",
                "camaras_dependientes": 1,
                "punto_critico": "Enlace fibra desde Edificio O",
                "falla_registrada": "Dependiente de Edificio O",
                "riesgo": "MEDIO"
            }
        ]
        
        print("📊 RANKING DE RIESGO:")
        for i, punto in enumerate(puntos_criticos, 1):
            print(f"\n{i}. {punto['ubicacion']} ({punto['riesgo']})")
            print(f"   Cámaras afectadas: {punto['camaras_dependientes']}")
            print(f"   Punto crítico: {punto['punto_critico']}")
            print(f"   Historial: {punto['falla_registrada']}")
        
        return puntos_criticos
    
    def generar_recomendaciones_preventivas(self):
        """Genera recomendaciones basadas en el análisis de casos"""
        
        print("\n\n💡 RECOMENDACIONES PREVENTIVAS")
        print("=" * 40)
        
        recomendaciones = [
            {
                "prioridad": "ALTA",
                "titulo": "Implementar redundancia en CFT Prat",
                "descripcion": "Instalar conexión backup o doble NVR",
                "justificacion": "26.5 horas de caída por cable suelto",
                "costo_estimado": "$150,000 - $200,000",
                "fecha_limite": "2024-11-30"
            },
            {
                "prioridad": "MEDIA",
                "titulo": "Auditoría de baterías UPS", 
                "descripcion": "Revisar todas las baterías instaladas hace 18+ meses",
                "justificacion": "Caso Edificio O muestra necesidad de cambio preventivo",
                "costo_estimado": "$200,000 - $300,000",
                "fecha_limite": "2024-12-15"
            },
            {
                "prioridad": "ALTA",
                "titulo": "Inspección instalaciones subcontratistas",
                "descripcion": "Revisar todas las instalaciones hechas por terceros",
                "justificacion": "CFT Prat (Seguridad Total) presentó falla de instalación",
                "costo_estimado": "$80,000 - $120,000",
                "fecha_limite": "2024-10-31"
            },
            {
                "prioridad": "MEDIA",
                "titulo": "Sistema de monitoreo automático",
                "descripcion": "Implementar alertas por pérdida de conectividad",
                "justificacion": "Detección temprana de fallas como cable suelto",
                "costo_estimado": "$400,000 - $600,000",
                "fecha_limite": "2025-03-31"
            }
        ]
        
        for rec in recomendaciones:
            print(f"\n🔴 {rec['prioridad']} - {rec['titulo']}")
            print(f"   📝 {rec['descripcion']}")
            print(f"   🔍 Justificación: {rec['justificacion']}")
            print(f"   💰 Costo estimado: {rec['costo_estimado']}")
            print(f"   📅 Fecha límite: {rec['fecha_limite']}")
        
        return recomendaciones
    
    def ejecutar_consulta_completa(self):
        """Ejecuta todas las consultas y análisis"""
        
        print("🔍 SISTEMA DE CONSULTAS Y TOPOLOGÍA - CASOS REALES")
        print("=" * 60)
        
        # 1. Insertar casos
        self.insertar_casos_semana_v2()
        
        # 2. Generar consultas
        self.generar_consultas_casos_reales()
        
        # 3. Análisis de dependencias
        self.consulta_dependencias_edificio_o()
        
        # 4. Puntos únicos de falla
        self.consulta_riesgo_puntos_unicos_falla()
        
        # 5. Recomendaciones
        self.generar_recomendaciones_preventivas()
        
        print("\n\n✅ CONSULTA COMPLETA FINALIZADA")
        print("📁 Sistema listo para consultas bidireccionales")

def main():
    """Función principal del integrador v2"""
    integrador = IntegradorCasosRealesV2()
    integrador.ejecutar_consulta_completa()

if __name__ == "__main__":
    main()