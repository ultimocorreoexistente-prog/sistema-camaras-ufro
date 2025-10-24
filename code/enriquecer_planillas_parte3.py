import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

planillas_dir = 'user_input_files/planillas-web'

print("=== ENRIQUECIMIENTO PARTE 3: Fallas y Técnicos ===")
print()

# ============================================================================
# 1. EQUIPOS TÉCNICOS - Añadir más técnicos
# ============================================================================
print("👨‍🔧 Enriqueciendo Equipos_Tecnicos.xlsx...")

tecnicos_path = os.path.join(planillas_dir, 'Equipos_Tecnicos.xlsx')
df_tec = pd.read_excel(tecnicos_path)

nuevos_tecnicos = [
    {'ID Técnico': 'TEC-005', 'Nombre Completo': 'Diego Morales', 'Cargo': 'Técnico Junior', 
     'Especialidad': 'Cámaras IP', 'Email': 'diego.morales@ufro.cl', 
     'Teléfono': '+56 9 8765 4323', 'Campus Asignado': 'Campus Pucón', 
     'Disponibilidad': 'Lunes a Viernes 09:00-18:00', 'Estado': 'Activo', 
     'Fecha Ingreso': '2024-07-01', 'Certificaciones': 'Certificación Hikvision básica', 
     'Número Casos Atendidos': 12, 'Promedio Tiempo Resolución (hrs)': 4.5, 
     'Observaciones': 'Técnico residente campus Pucón'},
    
    {'ID Técnico': 'TEC-006', 'Nombre Completo': 'Claudia Ramírez', 'Cargo': 'Técnico Senior', 
     'Especialidad': 'Infraestructura de Red', 'Email': 'claudia.ramirez@ufro.cl', 
     'Teléfono': '+56 9 7654 3212', 'Campus Asignado': 'Campus Angol', 
     'Disponibilidad': 'Lunes a Viernes 08:00-17:00', 'Estado': 'Activo', 
     'Fecha Ingreso': '2023-03-15', 'Certificaciones': 'CCNA, Certificación Cisco Switching', 
     'Número Casos Atendidos': 45, 'Promedio Tiempo Resolución (hrs)': 2.8, 
     'Observaciones': 'Especialista en redes - campus Angol'},
]

df_tec_nuevos = pd.DataFrame(nuevos_tecnicos)
df_tec_completa = pd.concat([df_tec, df_tec_nuevos], ignore_index=True)
df_tec_completa.to_excel(tecnicos_path, index=False)
print(f"  ✓ Equipos Técnicos: {len(df_tec)} → {len(df_tec_completa)} registros")

# ============================================================================
# 2. FALLAS ACTUALIZADA - Añadir más casos de fallas
# ============================================================================
print("⚠️ Enriqueciendo Fallas_Actualizada.xlsx...")

fallas_path = os.path.join(planillas_dir, 'Fallas_Actualizada.xlsx')
df_fallas = pd.read_excel(fallas_path)

nuevas_fallas = [
    {'ID Falla': 'FALLA-002', 'Fecha Reporte': '2025-10-15', 'Tipo Falla': 'Cámara Borrosa', 
     'Categoría': 'Problemas de Limpieza', 'Equipo Tipo': 'Cámara', 
     'Equipo ID': 'Bunker_EX_costado', 'Ubicación': 'Bunker - Exterior', 
     'Campus': 'Campus Principal', 'Descripción': 'Cámara presenta imagen borrosa por suciedad en lente', 
     'Prioridad': 'Media', 'Estado': 'Asignada', 'Reportado Por': 'Sistema automático', 
     'Asignado A': 'TEC-001', 'Fecha Asignación': '2025-10-15', 
     'Fecha Inicio Reparación': None, 'Fecha Fin Reparación': None, 
     'Solución Aplicada': None, 'Materiales Utilizados': None, 
     'Costo Reparación': None, 'Observaciones': 'Requiere limpieza de lente'},
    
    {'ID Falla': 'FALLA-003', 'Fecha Reporte': '2025-10-18', 'Tipo Falla': 'Sin señal de vídeo', 
     'Categoría': 'Falla de Conectividad', 'Equipo Tipo': 'Cámara', 
     'Equipo ID': 'EdificioL-P2-Bullet-03', 'Ubicación': 'Edificio L - 2do Piso', 
     'Campus': 'Campus Principal', 'Descripción': 'Cámara no envía señal al NVR - posible falla en cable', 
     'Prioridad': 'Alta', 'Estado': 'En Proceso', 'Reportado Por': 'Guardia de seguridad', 
     'Asignado A': 'TEC-002', 'Fecha Asignación': '2025-10-18', 
     'Fecha Inicio Reparación': '2025-10-18', 'Fecha Fin Reparación': None, 
     'Solución Aplicada': None, 'Materiales Utilizados': None, 
     'Costo Reparación': None, 'Observaciones': 'Técnico en terreno verificando cableado'},
    
    {'ID Falla': 'FALLA-004', 'Fecha Reporte': '2025-10-19', 'Tipo Falla': 'Switch no enciende', 
     'Categoría': 'Falla Eléctrica', 'Equipo Tipo': 'Switch', 
     'Equipo ID': 'SW-006', 'Ubicación': 'Edificio L - 2do Piso - Gabinete GAB-006', 
     'Campus': 'Campus Principal', 'Descripción': 'Switch no enciende - posible falla de fuente de alimentación', 
     'Prioridad': 'Crítica', 'Estado': 'Asignada', 'Reportado Por': 'TEC-001', 
     'Asignado A': 'TEC-003', 'Fecha Asignación': '2025-10-19', 
     'Fecha Inicio Reparación': None, 'Fecha Fin Reparación': None, 
     'Solución Aplicada': None, 'Materiales Utilizados': None, 
     'Costo Reparación': None, 'Observaciones': '8 cámaras sin servicio - urgente'},
    
    {'ID Falla': 'FALLA-005', 'Fecha Reporte': '2025-10-20', 'Tipo Falla': 'Imagen intermitente', 
     'Categoría': 'Falla de Conectividad', 'Equipo Tipo': 'Cámara', 
     'Equipo ID': 'Pucon-Recepcion-Dome-02', 'Ubicación': 'Campus Pucón - Recepción', 
     'Campus': 'Campus Pucón', 'Descripción': 'Cámara presenta imagen intermitente - posible problema de alimentación PoE', 
     'Prioridad': 'Media', 'Estado': 'Pendiente', 'Reportado Por': 'Personal administrativo', 
     'Asignado A': None, 'Fecha Asignación': None, 
     'Fecha Inicio Reparación': None, 'Fecha Fin Reparación': None, 
     'Solución Aplicada': None, 'Materiales Utilizados': None, 
     'Costo Reparación': None, 'Observaciones': 'Pendiente asignación a técnico campus Pucón'},
]

df_fallas_nuevas = pd.DataFrame(nuevas_fallas)
df_fallas_completa = pd.concat([df_fallas, df_fallas_nuevas], ignore_index=True)
df_fallas_completa.to_excel(fallas_path, index=False)
print(f"  ✓ Fallas Actualizada: {len(df_fallas)} → {len(df_fallas_completa)} registros")

print("\n✓ Enriquecimiento parte 3 completado")
print("\n=== RESUMEN ===")
print(f"  - Equipos Técnicos: {len(df_tec)} → {len(df_tec_completa)}")
print(f"  - Fallas Actualizada: {len(df_fallas)} → {len(df_fallas_completa)}")
