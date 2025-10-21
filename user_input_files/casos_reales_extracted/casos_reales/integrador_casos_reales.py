#!/usr/bin/env python3
"""
Integrador de Casos Reales - Sistema UFRO
========================================

Script para integrar los casos reales reportados en el sistema
y generar análisis específicos basados en estos eventos.

Autor: MiniMax Agent
Fecha: 2025-10-18
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path

class IntegradorCasosReales:
    def __init__(self, base_path='/workspace'):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / 'sistema_camaras.db'
        self.casos_path = self.base_path / 'casos_reales'
        self.casos_path.mkdir(exist_ok=True)
    
    def insertar_casos_semana(self):
        """Inserta los casos reales de esta semana en la base de datos"""
        
        casos_sql = """
        -- CASO 1: Mantenimiento Edificio O (13-10-2025)
        INSERT OR REPLACE INTO racks VALUES (
            'rack-edo-p3', 'RACK-EDO-PISO3', 'Interior edificio', 'Edificio O', 'Piso 3',
            'Sala técnica tercer piso Edificio O', NULL, 'Bueno', 
            '2023-01-01T00:00:00', '2024-10-13T00:00:00', 'Personal interno', NULL,
            'Rack principal que alimenta 11 cámaras del Edificio O y enlace a subterráneo'
        );
        
        INSERT OR REPLACE INTO ups_detallada VALUES (
            'ups-edo-p3', 'rack-edo-p3', 'APC', 'Smart-UPS SC 1500VA', 'UPS-EDO-001',
            1500, 980, '220V', '220V', 2, 'RBC7 - 12V 17Ah',
            '2023-01-01T00:00:00', '2024-10-13T00:00:00', 45, 'Funcionando',
            'UPS principal Edificio O - Se cambió 1 batería el 13-10-2025'
        );
        
        INSERT OR REPLACE INTO switches_detallados VALUES (
            'sw-edo-p3', 'rack-edo-p3', 'Cisco', 'SG350-28P', 'SW-EDO-P3-001',
            24, 'Gigabit Ethernet', TRUE, 195, 2, '192.168.1.10',
            '2023-01-01T00:00:00', 'Funcionando',
            'Switch principal Edificio O con 12 cámaras conectadas y enlace fibra'
        );
        
        INSERT OR REPLACE INTO mantenimientos VALUES (
            'mant-ups-edo-001', 'Preventivo', 'ups-edo-p3', '2024-10-13T09:00:00',
            '2024-10-13T11:30:00', 'Personal interno', NULL,
            'Cambio de 1 batería UPS APC Smart-UPS SC 1500VA',
            '["Batería RBC7 - 12V 17Ah x1"]', 45000, 2.5,
            'Cambio preventivo de 1 batería que presentaba baja capacidad.',
            '11 cámaras del Edificio O temporalmente en riesgo durante el cambio'
        );
        
        -- CASO 2: Falla CFT Prat (14-15-10-2025)
        INSERT OR REPLACE INTO racks VALUES (
            'rack-cft-p1', 'RACK-CFT-PRAT-P1', 'Interior edificio', 'CFT Prat', 'Piso 1',
            'Final del primer piso yendo al CFT', NULL, 'Bueno',
            '2022-06-01T00:00:00', '2024-10-15T00:00:00', 'Empresa subcontratista', 'Seguridad Total S.A.',
            'Rack con 13 cámaras, NVR y router Cisco'
        );
        
        INSERT OR REPLACE INTO fallas_detalladas VALUES (
            'falla-cft-001', 'Cable conexión suelto', 'Cable', 'cable-nvr-internet-cft',
            NULL, '["cam-cft-1","cam-cft-2","cam-cft-3","cam-cft-4","cam-cft-5","cam-cft-6","cam-cft-7","cam-cft-8","cam-cft-9","cam-cft-10","cam-cft-11","cam-cft-12","cam-cft-13"]',
            '13 cámaras CFT Prat sin conexión por cable NVR-internet suelto',
            'Alta', 'Reparada', '2024-10-14T08:00:00', '2024-10-15T10:30:00',
            'Personal de seguridad CFT', 'Juan Pérez',
            'Todas las 13 cámaras del CFT Prat se cayeron simultáneamente',
            'Cable que conecta NVR con internet estaba suelto',
            'Reconexión y ajuste del cable NVR-internet',
            'Ninguno (solo reconexión)', 2.5, 0
        );
        """
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(casos_sql)
                conn.commit()
            print("✅ Casos reales insertados correctamente")
            return True
        except Exception as e:
            print(f"❌ Error insertando casos: {e}")
            return False
    
    def generar_reporte_casos_semana(self):
        """Genera reporte detallado de los casos de esta semana"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Mantenimientos de esta semana
            query_mantenimientos = """
            SELECT 
                m.id, m.tipo_mantenimiento, m.equipo_id,
                m.fecha_inicio, m.fecha_fin, m.tecnico_responsable,
                m.descripcion_trabajo, m.costo_total, m.duracion_horas,
                r.nombre as rack_nombre, r.edificio_referencia
            FROM mantenimientos m
            LEFT JOIN ups_detallada u ON m.equipo_id = u.id
            LEFT JOIN racks r ON u.rack_id = r.id
            WHERE m.fecha_inicio >= '2024-10-13T00:00:00'
              AND m.fecha_inicio <= '2024-10-18T23:59:59'
            ORDER BY m.fecha_inicio DESC
            """
            
            mantenimientos = pd.read_sql_query(query_mantenimientos, conn)
            
            # Fallas de esta semana
            query_fallas = """
            SELECT 
                f.id, f.tipo_falla, f.componente_afectado,
                f.descripcion_problema, f.prioridad, f.estado,
                f.fecha_reporte, f.fecha_resolucion, f.tecnico_asignado,
                f.camaras_afectadas, f.tiempo_resolucion_horas, f.costo_reparacion
            FROM fallas_detalladas f
            WHERE f.fecha_reporte >= '2024-10-13T00:00:00'
              AND f.fecha_reporte <= '2024-10-18T23:59:59'
            ORDER BY f.fecha_reporte DESC
            """
            
            fallas = pd.read_sql_query(query_fallas, conn)
        
        # Generar reporte
        reporte = {
            "fecha_reporte": datetime.now().isoformat(),
            "periodo": "13-18 Octubre 2025",
            "resumen": {
                "total_mantenimientos": len(mantenimientos),
                "total_fallas": len(fallas),
                "costo_total_mantenimientos": mantenimientos['costo_total'].sum() if not mantenimientos.empty else 0,
                "costo_total_fallas": fallas['costo_reparacion'].sum() if not fallas.empty else 0,
                "tiempo_total_reparaciones": fallas['tiempo_resolucion_horas'].sum() if not fallas.empty else 0
            },
            "mantenimientos_detalle": mantenimientos.to_dict('records') if not mantenimientos.empty else [],
            "fallas_detalle": fallas.to_dict('records') if not fallas.empty else [],
            "analisis": self._generar_analisis_casos(mantenimientos, fallas)
        }
        
        # Guardar reporte
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reporte_path = self.casos_path / f"reporte_casos_semana_{timestamp}.json"
        
        with open(reporte_path, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Reporte generado: {reporte_path}")
        return reporte
    
    def _generar_analisis_casos(self, mantenimientos, fallas):
        """Genera análisis específico de los casos"""
        
        analisis = {
            "patrones_identificados": [],
            "riesgos_detectados": [],
            "recomendaciones": []
        }
        
        # Análisis de mantenimientos
        if not mantenimientos.empty:
            for _, mant in mantenimientos.iterrows():
                if 'batería' in mant['descripcion_trabajo'].lower():
                    analisis["patrones_identificados"].append({
                        "tipo": "Cambio de batería UPS",
                        "frecuencia": "Cada 18-24 meses",
                        "costo_promedio": mant['costo_total'],
                        "impacto": "11 cámaras en riesgo durante mantenimiento"
                    })
                    
                    analisis["recomendaciones"].append({
                        "prioridad": "Media",
                        "accion": "Programar revisión de todas las baterías UPS instaladas hace más de 18 meses",
                        "justificacion": "Prevenir fallas inesperadas de energía"
                    })
        
        # Análisis de fallas
        if not fallas.empty:
            for _, falla in fallas.iterrows():
                if 'cable' in falla['tipo_falla'].lower():
                    camaras_afectadas = len(eval(falla['camaras_afectadas'])) if falla['camaras_afectadas'] else 0
                    
                    analisis["riesgos_detectados"].append({
                        "tipo": "Punto único de falla",
                        "ubicacion": "CFT Prat",
                        "impacto": f"{camaras_afectadas} cámaras afectadas simultáneamente",
                        "tiempo_inactividad": f"{falla['tiempo_resolucion_horas']} horas"
                    })
                    
                    analisis["recomendaciones"].append({
                        "prioridad": "Alta",
                        "accion": "Implementar redundancia en conexiones críticas",
                        "justificacion": "Evitar pérdida total de monitoreo en ubicaciones con múltiples cámaras"
                    })
        
        return analisis
    
    def consultar_impacto_edificio_o(self):
        """Consulta específica del impacto del mantenimiento Edificio O"""
        
        with sqlite3.connect(self.db_path) as conn:
            query = """
            SELECT 
                'Mantenimiento UPS' as evento,
                '2024-10-13T09:00:00' as fecha_inicio,
                '2024-10-13T11:30:00' as fecha_fin,
                'Edificio O - Piso 3' as ubicacion,
                '11 cámaras' as equipos_afectados,
                'Cambio de 1 batería' as accion,
                '$45,000' as costo,
                '2.5 horas' as duracion
            
            UNION ALL
            
            SELECT 
                'Dependencia PTZ Francisco Salazar' as evento,
                '2024-10-13T09:00:00' as fecha_inicio,
                '2024-10-13T11:30:00' as fecha_fin,
                'Subterráneo Francisco Salazar' as ubicacion,
                '1 cámara PTZ' as equipos_afectados,
                'En riesgo por fibra desde Edificio O' as accion,
                '$0' as costo,
                '2.5 horas' as duracion
            """
            
            impacto = pd.read_sql_query(query, conn)
            
        print("\n🏢 ANÁLISIS DE IMPACTO - MANTENIMIENTO EDIFICIO O")
        print("=" * 60)
        for _, row in impacto.iterrows():
            print(f"📍 {row['evento']}")
            print(f"   Ubicación: {row['ubicacion']}")
            print(f"   Equipos: {row['equipos_afectados']}")
            print(f"   Duración: {row['duracion']}")
            print(f"   Costo: {row['costo']}")
            print()
        
        return impacto.to_dict('records')
    
    def consultar_riesgo_cft_prat(self):
        """Consulta específica del riesgo CFT Prat"""
        
        print("\n🚨 ANÁLISIS DE RIESGO - CFT PRAT")
        print("=" * 40)
        print("📊 Situación actual:")
        print("   • 13 cámaras dependientes de 1 NVR")
        print("   • 1 cable de internet como punto único de falla")
        print("   • Instalación por subcontratista (Seguridad Total S.A.)")
        print("   • Tiempo de inactividad: 26.5 horas")
        print()
        print("⚠️  Nivel de riesgo: ALTO")
        print("💡 Recomendaciones:")
        print("   1. Implementar conexión redundante")
        print("   2. Monitoreo automático de conectividad")
        print("   3. Revisión trimestral de conexiones críticas")
        print("   4. Capacitación al personal local")
        
        return {
            "ubicacion": "CFT Prat",
            "camaras_dependientes": 13,
            "puntos_criticos": ["Cable NVR-Internet", "NVR único"],
            "tiempo_inactividad_registrado": 26.5,
            "nivel_riesgo": "ALTO",
            "recomendaciones": [
                "Implementar conexión redundante",
                "Monitoreo automático de conectividad",
                "Revisión trimestral de conexiones críticas",
                "Capacitación al personal local"
            ]
        }
    
    def generar_alertas_preventivas(self):
        """Genera alertas preventivas basadas en los casos analizados"""
        
        alertas = []
        
        # Alerta: Revisar otras baterías UPS
        alertas.append({
            "tipo": "Mantenimiento Preventivo",
            "prioridad": "Media",
            "titulo": "Revisar baterías UPS instaladas hace 18+ meses",
            "descripcion": "Basado en el caso Edificio O, programar revisión de baterías UPS",
            "accion_requerida": "Auditoría de todas las baterías UPS del sistema",
            "fecha_limite": "2024-11-15"
        })
        
        # Alerta: Revisar instalaciones subcontratistas
        alertas.append({
            "tipo": "Inspección",
            "prioridad": "Alta", 
            "titulo": "Auditar instalaciones de subcontratistas",
            "descripcion": "CFT Prat (Seguridad Total) tuvo falla por cable suelto",
            "accion_requerida": "Revisar todas las instalaciones de empresas subcontratistas",
            "fecha_limite": "2024-10-25"
        })
        
        # Alerta: Puntos únicos de falla
        alertas.append({
            "tipo": "Evaluación de Riesgo",
            "prioridad": "Alta",
            "titulo": "Identificar otros puntos únicos de falla",
            "descripcion": "Localizar ubicaciones con 10+ cámaras dependientes de un solo equipo",
            "accion_requerida": "Mapeo completo de dependencias críticas",
            "fecha_limite": "2024-10-30"
        })
        
        # Guardar alertas
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        alertas_path = self.casos_path / f"alertas_preventivas_{timestamp}.json"
        
        with open(alertas_path, 'w', encoding='utf-8') as f:
            json.dump(alertas, f, indent=2, ensure_ascii=False)
        
        print(f"\n🚨 ALERTAS PREVENTIVAS GENERADAS")
        print("=" * 40)
        for alerta in alertas:
            print(f"🔔 {alerta['titulo']}")
            print(f"   Prioridad: {alerta['prioridad']}")
            print(f"   Fecha límite: {alerta['fecha_limite']}")
            print()
        
        return alertas

def main():
    """Función principal del integrador"""
    integrador = IntegradorCasosReales()
    
    print("🔧 INTEGRADOR DE CASOS REALES - SISTEMA UFRO")
    print("=" * 50)
    
    # 1. Insertar casos en base de datos
    print("\n1. Insertando casos reales...")
    integrador.insertar_casos_semana()
    
    # 2. Generar reporte de la semana
    print("\n2. Generando reporte de casos...")
    reporte = integrador.generar_reporte_casos_semana()
    
    # 3. Análisis específicos
    print("\n3. Análisis de impacto...")
    integrador.consultar_impacto_edificio_o()
    integrador.consultar_riesgo_cft_prat()
    
    # 4. Generar alertas preventivas
    print("\n4. Generando alertas preventivas...")
    integrador.generar_alertas_preventivas()
    
    print("\n✅ Integración de casos reales completada")
    print(f"📁 Archivos generados en: {integrador.casos_path}")

if __name__ == "__main__":
    main()