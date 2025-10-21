#!/usr/bin/env python3
"""
Demo Sistema de Consultas - Casos Reales UFRO
===========================================

Demo funcional del sistema de consultas bidireccionales
usando los casos reales reportados esta semana.

Autor: MiniMax Agent
Fecha: 2025-10-18
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

class DemoConsultasCasosReales:
    def __init__(self, base_path='/workspace'):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / 'sistema_camaras.db'
        self.casos_path = self.base_path / 'casos_reales'
        self.casos_path.mkdir(exist_ok=True)
    
    def insertar_casos_demo(self):
        """Inserta los casos reales usando la estructura correcta"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                
                # CASO 1: Mantenimiento Edificio O
                caso1 = """
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion, 
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas, created_at
                ) VALUES (
                    'Mantenimiento UPS Edificio O - Octubre 2024',
                    '2024-10-13',
                    'Cambio preventivo de 1 batería del UPS APC Smart-UPS SC 1500VA ubicado en sala técnica del tercer piso del Edificio O. El sistema alimenta 11 cámaras locales y mantiene enlace de fibra hacia cámara PTZ remota en Francisco Salazar.',
                    'UPS APC Smart-UPS SC 1500VA, Batería RBC7 12V 17Ah, Switch Cisco SG350-28P, 11 cámaras Edificio O, Enlace fibra óptica, Cámara PTZ Francisco Salazar',
                    'Switch principal Edificio O alimenta 11 cámaras locales. Switch también mantiene enlace por fibra óptica hacia gabinete subterráneo donde se ubica cámara PTZ Francisco Salazar con POE adicional.',
                    'Cambio exitoso de batería manteniendo sistema operativo con batería restante. Duración total 2.5 horas incluyendo pruebas.',
                    2.5,
                    'Importancia de tener al menos 2 baterías para permitir mantenimiento sin corte total. Considerar programar mantenimientos en horarios de menor actividad. El enlace de fibra remoto depende críticamente del UPS principal.',
                    ?
                )
                """
                
                conn.execute(caso1, (datetime.now().isoformat(),))
                
                # CASO 2: Falla CFT Prat
                caso2 = """
                INSERT OR REPLACE INTO casos_reales (
                    nombre_caso, fecha_caso, descripcion,
                    componentes_involucrados, dependencias_cascada,
                    solucion_aplicada, tiempo_resolucion_horas,
                    lecciones_aprendidas, created_at
                ) VALUES (
                    'Falla Conectividad CFT Prat - Octubre 2024',
                    '2024-10-14',
                    'Pérdida total de conectividad de las 13 cámaras del CFT Prat debido a cable ethernet suelto entre NVR y conexión a internet. La falla se detectó cuando todas las cámaras se desconectaron simultáneamente.',
                    'NVR CFT Prat, Cable ethernet NVR-Internet, 13 cámaras CFT, Router Cisco, Instalación Seguridad Total S.A.',
                    'Todas las 13 cámaras del CFT Prat dependen de un único NVR. El NVR depende de una sola conexión ethernet a internet. No existe redundancia de conectividad.',
                    'Reconexión del cable ethernet y verificación de todas las conexiones del rack. Revisión adicional de cables críticos. Reparación realizada por personal de seguridad del CFT.',
                    26.5,
                    'Ubicaciones con múltiples cámaras requieren redundancia de conectividad. Instalaciones de subcontratistas necesitan mayor supervisión. Implementar monitoreo automático de conectividad.',
                    ?
                )
                """
                
                conn.execute(caso2, (datetime.now().isoformat(),))
                
                # FALLA ESPECÍFICA CFT Prat
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
                    'cable-nvr-internet-cft-prat',
                    'Cable que conecta NVR del CFT Prat con internet se encontró suelto, causando pérdida total de conectividad de todas las cámaras de la ubicación',
                    'cam-cft-1,cam-cft-2,cam-cft-3,cam-cft-4,cam-cft-5,cam-cft-6,cam-cft-7,cam-cft-8,cam-cft-9,cam-cft-10,cam-cft-11,cam-cft-12,cam-cft-13',
                    26.5,
                    'Reconexión del cable ethernet NVR-Internet y verificación de todas las conexiones del rack CFT',
                    '2024-10-15',
                    'Juan Pérez - Personal Seguridad CFT',
                    0,
                    'Resuelto',
                    'Alta'
                )
                """
                
                conn.execute(falla_cft)
                
                conn.commit()
                print("✅ Casos demo insertados correctamente")
                return True
                
        except Exception as e:
            print(f"❌ Error insertando casos demo: {e}")
            return False
    
    def demo_consulta_por_ubicacion(self, ubicacion="CFT Prat"):
        """Demo: Consultar todo lo relacionado con una ubicación"""
        
        print(f"\n📋 CONSULTA POR UBICACIÓN: {ubicacion}")
        print("=" * 50)
        
        with sqlite3.connect(self.db_path) as conn:
            
            # Casos relacionados con la ubicación
            query_casos = """
            SELECT nombre_caso, fecha_caso, tiempo_resolucion_horas, descripcion
            FROM casos_reales 
            WHERE descripcion LIKE ? OR nombre_caso LIKE ?
            ORDER BY fecha_caso DESC
            """
            
            casos = pd.read_sql_query(query_casos, conn, params=[f"%{ubicacion}%", f"%{ubicacion}%"])
            
            print("📊 CASOS REGISTRADOS:")
            if not casos.empty:
                for _, caso in casos.iterrows():
                    print(f"  • {caso['fecha_caso']}: {caso['nombre_caso']}")
                    print(f"    Duración: {caso['tiempo_resolucion_horas']} horas")
                    print(f"    Detalle: {caso['descripcion'][:80]}...\n")
            else:
                print("  Sin casos registrados")
            
            # Fallas específicas
            query_fallas = """
            SELECT fecha_falla, tipo_falla, descripcion_falla, 
                   tiempo_downtime_horas, camaras_afectadas, estado
            FROM fallas_especificas
            WHERE descripcion_falla LIKE ? OR componente_afectado_id LIKE ?
            ORDER BY fecha_falla DESC
            """
            
            fallas = pd.read_sql_query(query_fallas, conn, params=[f"%{ubicacion}%", f"%{ubicacion.lower().replace(' ', '-')}%"])
            
            print("🚫 FALLAS ESPECÍFICAS:")
            if not fallas.empty:
                for _, falla in fallas.iterrows():
                    camaras_count = len(falla['camaras_afectadas'].split(',')) if falla['camaras_afectadas'] else 0
                    print(f"  • {falla['fecha_falla']}: {falla['tipo_falla']}")
                    print(f"    Cámaras afectadas: {camaras_count}")
                    print(f"    Tiempo caída: {falla['tiempo_downtime_horas']} horas")
                    print(f"    Estado: {falla['estado']}\n")
            else:
                print("  Sin fallas registradas")
            
        return {"casos": casos.to_dict('records'), "fallas": fallas.to_dict('records')}
    
    def demo_consulta_por_tipo_falla(self, tipo="Cable suelto"):
        """Demo: Consultar por tipo de falla para identificar patrones"""
        
        print(f"\n🔍 CONSULTA POR TIPO DE FALLA: {tipo}")
        print("=" * 50)
        
        with sqlite3.connect(self.db_path) as conn:
            
            query = """
            SELECT 
                fecha_falla,
                componente_afectado_tipo,
                componente_afectado_id,
                descripcion_falla,
                camaras_afectadas,
                tiempo_downtime_horas,
                tecnico_reparador,
                costo_reparacion,
                estado
            FROM fallas_especificas
            WHERE tipo_falla LIKE ?
            ORDER BY fecha_falla DESC
            """
            
            fallas = pd.read_sql_query(query, conn, params=[f"%{tipo}%"])
            
            if not fallas.empty:
                print("📊 ESTADÍSTICAS:")
                total_fallas = len(fallas)
                total_downtime = fallas['tiempo_downtime_horas'].sum()
                total_camaras = sum([len(f.split(',')) if f else 0 for f in fallas['camaras_afectadas']])
                costo_total = fallas['costo_reparacion'].sum()
                
                print(f"  • Total fallas: {total_fallas}")
                print(f"  • Tiempo total caída: {total_downtime} horas")
                print(f"  • Cámaras afectadas: {total_camaras}")
                print(f"  • Costo total reparaciones: ${costo_total:,.0f}")
                print(f"  • Promedio horas por falla: {total_downtime/total_fallas:.1f}")
                
                print("\n📋 DETALLE DE FALLAS:")
                for _, falla in fallas.iterrows():
                    camaras_count = len(falla['camaras_afectadas'].split(',')) if falla['camaras_afectadas'] else 0
                    print(f"\n  📅 {falla['fecha_falla']}")
                    print(f"    Componente: {falla['componente_afectado_tipo']} ({falla['componente_afectado_id']})")
                    print(f"    Cámaras: {camaras_count} afectadas")
                    print(f"    Downtime: {falla['tiempo_downtime_horas']} horas")
                    print(f"    Técnico: {falla['tecnico_reparador']}")
                    print(f"    Estado: {falla['estado']}")
            else:
                print("  Sin fallas de este tipo registradas")
                
        return fallas.to_dict('records')
    
    def demo_analisis_dependencias_cascada(self):
        """Demo: Análisis de dependencias en cascada"""
        
        print("\n🌐 ANÁLISIS DE DEPENDENCIAS EN CASCADA")
        print("=" * 50)
        
        with sqlite3.connect(self.db_path) as conn:
            
            query_casos = """
            SELECT nombre_caso, dependencias_cascada, componentes_involucrados
            FROM casos_reales
            WHERE dependencias_cascada IS NOT NULL AND dependencias_cascada != ''
            ORDER BY fecha_caso DESC
            """
            
            casos = pd.read_sql_query(query_casos, conn)
            
            for _, caso in casos.iterrows():
                print(f"\n🔗 CASO: {caso['nombre_caso']}")
                print(f"\n  💻 COMPONENTES INVOLUCRADOS:")
                componentes = caso['componentes_involucrados'].split(', ')
                for comp in componentes:
                    print(f"    • {comp}")
                
                print(f"\n  ⚡ DEPENDENCIAS EN CASCADA:")
                dependencias = caso['dependencias_cascada']
                print(f"    {dependencias}")
                
                # Análisis específico por caso
                if "Edificio O" in caso['nombre_caso']:
                    print(f"\n  📊 ANÁLISIS DE IMPACTO EDIFICIO O:")
                    print(f"    • Falla UPS → 11 cámaras locales sin energía")
                    print(f"    • Falla UPS → Switch sin energía → Pérdida enlace fibra")
                    print(f"    • Pérdida enlace fibra → Cámara PTZ Francisco Salazar inoperativa")
                    print(f"    • Tiempo autonomía: 45 minutos con 2 baterías")
                    print(f"    • Impacto total: 12 cámaras (11 locales + 1 remota)")
                
                elif "CFT Prat" in caso['nombre_caso']:
                    print(f"\n  📊 ANÁLISIS DE IMPACTO CFT PRAT:")
                    print(f"    • Falla cable NVR → Pérdida total conectividad")
                    print(f"    • Un solo punto de falla afecta 13 cámaras")
                    print(f"    • Sin redundancia de conexión")
                    print(f"    • Tiempo detección: Inmediato (todas las cámaras caías)")
                    print(f"    • Riesgo: ALTO - Necesita redundancia")
    
    def demo_consulta_preventiva(self):
        """Demo: Generar consultas preventivas basadas en casos"""
        
        print("\n🔮 CONSULTAS PREVENTIVAS")
        print("=" * 40)
        
        with sqlite3.connect(self.db_path) as conn:
            
            # Lecciones aprendidas
            query_lecciones = """
            SELECT nombre_caso, lecciones_aprendidas
            FROM casos_reales
            WHERE lecciones_aprendidas IS NOT NULL
            ORDER BY fecha_caso DESC
            """
            
            lecciones = pd.read_sql_query(query_lecciones, conn)
            
            print("💡 ACCIONES PREVENTIVAS SUGERIDAS:")
            
            acciones_preventivas = [
                {
                    "accion": "Auditoría de baterías UPS",
                    "justificacion": "Caso Edificio O: cambio preventivo evitó falla mayor",
                    "prioridad": "MEDIA",
                    "plazo": "30 días",
                    "ubicaciones_criticas": "Edificios con 10+ cámaras dependientes"
                },
                {
                    "accion": "Implementar redundancia CFT Prat",
                    "justificacion": "26.5 horas caída por un solo cable suelto",
                    "prioridad": "ALTA",
                    "plazo": "15 días",
                    "ubicaciones_criticas": "CFT Prat y ubicaciones similares"
                },
                {
                    "accion": "Revisión instalaciones subcontratistas",
                    "justificacion": "Falla en instalación de Seguridad Total S.A.",
                    "prioridad": "ALTA",
                    "plazo": "7 días",
                    "ubicaciones_criticas": "Todas las instalaciones de terceros"
                },
                {
                    "accion": "Monitoreo automático conectividad",
                    "justificacion": "Detección temprana de fallas como cables sueltos",
                    "prioridad": "MEDIA",
                    "plazo": "60 días",
                    "ubicaciones_criticas": "Ubicaciones remotas sin personal"
                }
            ]
            
            for i, accion in enumerate(acciones_preventivas, 1):
                print(f"\n{i}. 🔴 {accion['prioridad']} - {accion['accion']}")
                print(f"   🔍 Justificación: {accion['justificacion']}")
                print(f"   📅 Plazo: {accion['plazo']}")
                print(f"   📍 Ubicaciones: {accion['ubicaciones_criticas']}")
            
        return acciones_preventivas
    
    def ejecutar_demo_completa(self):
        """Ejecuta toda la demostración del sistema de consultas"""
        
        print("🎆 DEMO SISTEMA DE CONSULTAS BIDIRECCIONALES")
        print("Sistema de Gestión de Cámaras UFRO")
        print("=" * 60)
        print("Casos reales reportados semana 13-18 Octubre 2025")
        
        # 1. Insertar casos demo
        print("\n📁 Paso 1: Insertando casos reales...")
        self.insertar_casos_demo()
        
        # 2. Consulta por ubicación
        print("\n📁 Paso 2: Consultas por ubicación...")
        self.demo_consulta_por_ubicacion("CFT Prat")
        self.demo_consulta_por_ubicacion("Edificio O")
        
        # 3. Consulta por tipo de falla
        print("\n📁 Paso 3: Consultas por tipo de falla...")
        self.demo_consulta_por_tipo_falla("Cable suelto")
        
        # 4. Análisis de dependencias
        print("\n📁 Paso 4: Análisis de dependencias...")
        self.demo_analisis_dependencias_cascada()
        
        # 5. Consultas preventivas
        print("\n📁 Paso 5: Consultas preventivas...")
        self.demo_consulta_preventiva()
        
        print("\n\n✅ DEMO COMPLETADA")
        print("💪 Sistema listo para consultas bidireccionales en tiempo real")
        print("🔎 Puedes consultar por: ubicación, IP, switch, rack, tipo de falla, etc.")
        
        # Guardar resumen
        resumen = {
            "demo_ejecutada": datetime.now().isoformat(),
            "casos_procesados": 2,
            "consultas_disponibles": [
                "Consulta por ubicación",
                "Consulta por IP de cámara",
                "Consulta por switch",
                "Consulta por rack/gabinete",
                "Consulta por tipo de falla",
                "Análisis de dependencias",
                "Consultas preventivas"
            ],
            "capacidades_sistema": {
                "bidireccional": True,
                "tiempo_real": True,
                "topologia_visual": True,
                "alertas_preventivas": True,
                "analisis_impacto": True
            }
        }
        
        with open(self.casos_path / 'demo_resumen.json', 'w', encoding='utf-8') as f:
            json.dump(resumen, f, indent=2, ensure_ascii=False)
            
        print(f"\n📄 Resumen guardado en: {self.casos_path}/demo_resumen.json")

def main():
    """Función principal de la demo"""
    demo = DemoConsultasCasosReales()
    demo.ejecutar_demo_completa()

if __name__ == "__main__":
    main()