#!/usr/bin/env python3
"""
Generador de Informe Completo de Casos Reales
Sistema de Gestión de Cámaras UFRO
"""

import sqlite3
import json
from datetime import datetime

def generar_informe_casos_reales():
    """Genera un informe detallado de todos los casos reales"""
    
    db_path = 'sistema_camaras.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener todos los casos reales con sus detalles
    cursor.execute("""
        SELECT 
            id,
            nombre_caso,
            fecha_caso,
            descripcion,
            componentes_involucrados,
            dependencias_cascada,
            solucion_aplicada,
            tiempo_resolucion_horas,
            lecciones_aprendidas
        FROM casos_reales
        ORDER BY fecha_caso
    """)
    
    casos = cursor.fetchall()
    
    # Obtener fallas específicas relacionadas
    cursor.execute("""
        SELECT 
            fecha_falla,
            tipo_falla,
            componente_afectado_tipo,
            componente_afectado_id,
            descripcion_falla,
            camaras_afectadas,
            tiempo_downtime_horas,
            solucion_aplicada,
            fecha_resolucion,
            tecnico_reparador,
            costo_reparacion,
            estado,
            prioridad,
            campus,
            observaciones
        FROM fallas_especificas
        ORDER BY fecha_falla
    """)
    
    fallas = cursor.fetchall()
    
    # Crear diccionario de fallas por fecha
    fallas_dict = {}
    for falla in fallas:
        fecha = falla[0]
        if fecha not in fallas_dict:
            fallas_dict[fecha] = []
        fallas_dict[fecha].append(falla)
    
    # Generar informe en Markdown
    informe = []
    informe.append("# Informe Completo de Casos Reales Documentados")
    informe.append("## Sistema de Gestión de Cámaras UFRO\n")
    informe.append(f"**Fecha del informe:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    informe.append(f"**Total de casos documentados:** {len(casos)}\n")
    informe.append("---\n")
    
    # Resumen ejecutivo
    informe.append("## 📊 Resumen Ejecutivo\n")
    
    total_horas = sum([caso[7] for caso in casos if caso[7]])
    informe.append(f"- **Total casos documentados:** {len(casos)}")
    informe.append(f"- **Tiempo total de resolución:** {total_horas:.2f} horas")
    informe.append(f"- **Promedio de resolución:** {total_horas/len(casos):.2f} horas por caso")
    informe.append(f"- **Fallas específicas registradas:** {len(fallas)}\n")
    
    # Tabla resumen
    informe.append("### Tabla Resumen de Casos\n")
    informe.append("| # | Fecha | Caso | Tiempo (h) | Estado |")
    informe.append("|---|-------|------|------------|--------|")
    
    for i, caso in enumerate(casos, 1):
        fecha = caso[2]
        nombre = caso[1]
        tiempo = caso[7] if caso[7] else 0
        informe.append(f"| {i} | {fecha} | {nombre[:40]}... | {tiempo:.2f} | Resuelto |")
    
    informe.append("\n---\n")
    
    # Detalles de cada caso
    informe.append("## 📋 Detalles de Cada Caso\n")
    
    for i, caso in enumerate(casos, 1):
        caso_id, nombre, fecha, desc, componentes, dependencias, solucion, tiempo, lecciones = caso
        
        informe.append(f"### Caso {i}: {nombre}\n")
        informe.append(f"**📅 Fecha:** {fecha}")
        informe.append(f"**⏱️ Tiempo de resolución:** {tiempo if tiempo else 'N/A'} horas\n")
        
        # Descripción
        informe.append("#### 📝 Descripción")
        informe.append(f"{desc}\n")
        
        # Componentes involucrados
        informe.append("#### 📦 Componentes Involucrados")
        try:
            comp_list = json.loads(componentes) if componentes else []
            for comp in comp_list:
                informe.append(f"- {comp}")
        except:
            informe.append(f"- {componentes}")
        informe.append("")
        
        # Cámaras afectadas (buscar en fallas específicas)
        if fecha in fallas_dict:
            informe.append("#### 📹 Cámaras Afectadas")
            for falla in fallas_dict[fecha]:
                try:
                    camaras = json.loads(falla[5]) if falla[5] else []
                    if isinstance(camaras, list):
                        if len(camaras) > 0 and 'Todas' in str(camaras[0]):
                            informe.append(f"- **{camaras[0]}**")
                        else:
                            informe.append(f"- **Total:** {len(camaras)} cámaras")
                            for cam in camaras[:5]:  # Mostrar primeras 5
                                informe.append(f"  - {cam}")
                            if len(camaras) > 5:
                                informe.append(f"  - ... y {len(camaras)-5} cámaras más")
                    else:
                        informe.append(f"- {camaras}")
                except:
                    informe.append(f"- {falla[5]}")
            informe.append("")
        
        # Dependencias en cascada
        informe.append("#### 🔗 Dependencias en Cascada")
        try:
            dep_list = json.loads(dependencias) if dependencias else []
            for dep in dep_list:
                informe.append(f"- {dep}")
        except:
            informe.append(f"- {dependencias}")
        informe.append("")
        
        # Solución aplicada
        informe.append("#### ✅ Solución Aplicada")
        informe.append(f"{solucion}\n")
        
        # Información adicional de falla específica
        if fecha in fallas_dict:
            for falla in fallas_dict[fecha]:
                informe.append("#### 👨‍🔧 Detalles Técnicos")
                informe.append(f"- **Técnico:** {falla[9]}")
                informe.append(f"- **Costo de reparación:** ${falla[10]:,.0f}")
                informe.append(f"- **Prioridad:** {falla[12]}")
                informe.append(f"- **Campus:** {falla[13]}")
                if falla[14]:
                    informe.append(f"- **Observaciones:** {falla[14]}")
                informe.append("")
        
        # Lecciones aprendidas
        informe.append("#### 💡 Lecciones Aprendidas")
        informe.append(f"{lecciones}\n")
        
        informe.append("---\n")
    
    # Análisis de tipos de fallas
    informe.append("## 📊 Análisis de Tipos de Fallas\n")
    
    cursor.execute("""
        SELECT 
            tipo_falla,
            COUNT(*) as cantidad,
            AVG(tiempo_downtime_horas) as promedio_horas,
            SUM(costo_reparacion) as costo_total
        FROM fallas_especificas
        GROUP BY tipo_falla
        ORDER BY cantidad DESC
    """)
    
    tipos_fallas = cursor.fetchall()
    
    informe.append("| Tipo de Falla | Cantidad | Promedio Horas | Costo Total |")
    informe.append("|---------------|----------|----------------|-------------|")
    
    for tipo, cant, prom, costo in tipos_fallas:
        informe.append(f"| {tipo} | {cant} | {prom:.2f}h | ${costo:,.0f} |")
    
    informe.append("\n---\n")
    
    # Recomendaciones
    informe.append("## 🚨 Recomendaciones Preventivas\n")
    informe.append("### Basadas en los casos documentados:\n")
    
    recomendaciones = [
        "1. **Redundancia en enlaces críticos de fibra óptica**",
        "   - El Bicicletero y CFT Prat han presentado fallas por cables sueltos",
        "   - Implementar enlaces redundantes en ubicaciones con múltiples cámaras\n",
        
        "2. **Revisión de instalaciones de subcontratistas**",
        "   - Caso CFT Prat evidenció problemas de instalación",
        "   - Auditoría completa de todas las instalaciones externas\n",
        
        "3. **Mantenimiento preventivo de UPS**",
        "   - Caso Edificio O: cambio exitoso de baterías",
        "   - Programar cambios preventivos cada 18 meses\n",
        
        "4. **Documentación de puntos eléctricos no convencionales**",
        "   - Caso ZM: automático en caseta guardia",
        "   - Señalizar y documentar todas las protecciones eléctricas\n",
        
        "5. **Limpieza preventiva de cámaras exteriores**",
        "   - Caso Bunker: telarañas en lente",
        "   - Programa trimestral de limpieza\n",
        
        "6. **Monitoreo de conectividad en tiempo real**",
        "   - Múltiples casos de fallas detectadas tardíamente",
        "   - Sistema de alertas automáticas\n",
        
        "7. **Topología de red documentada**",
        "   - Caso Bicicletero evidenció cadena de 3 enlaces",
        "   - Mapeo completo de dependencias de fibra óptica\n"
    ]
    
    for rec in recomendaciones:
        informe.append(rec)
    
    informe.append("\n---\n")
    
    # Footer
    informe.append("## 📝 Información del Documento\n")
    informe.append(f"- **Base de datos:** {db_path}")
    informe.append(f"- **Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    informe.append(f"- **Sistema:** Sistema de Gestión de Cámaras UFRO")
    informe.append(f"- **Total casos:** {len(casos)}")
    informe.append(f"- **Total fallas:** {len(fallas)}\n")
    
    conn.close()
    
    return "\n".join(informe)

if __name__ == "__main__":
    informe = generar_informe_casos_reales()
    
    # Guardar informe
    output_file = 'docs/INFORME_CASOS_REALES_COMPLETO.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(informe)
    
    print(f"\n✅ Informe generado exitosamente: {output_file}")
    print(f"\n{informe}")
