import pandas as pd

# Crear planilla de fallas actualizada con tipos reales reportados por la central
df_fallas = pd.DataFrame({
    "ID Falla": [],
    "Fecha de Reporte": [],
    "Reportado Por": [],  # Central de Monitoreo, Técnico, Usuario
    "Tipo de Falla": [],  # Categorías actualizadas
    "Subtipo": [],  # Detalle específico
    "Cámara Afectada": [],
    "Nombre de Cámara": [],
    "IP de Cámara": [],
    "Ubicación": [],
    "Gabinete Relacionado": [],
    "Switch Relacionado": [],
    "Puerto Afectado": [],
    "Descripción": [],
    "Impacto en Visibilidad": [],  # Alto, Medio, Bajo
    "Afecta Visión Nocturna": [],  # Sí/No
    "Estado": [],  # Reportada, En proceso, Resuelta, Cerrada
    "Prioridad": [],  # Alta, Media, Baja
    "Técnico Asignado": [], # Técnico Propio, Oliver Carrasco, Marco Altamirano, ConectaSur
    "Fecha de Resolución": [],
    "Solución Aplicada": [],
    "Materiales Utilizados": [],
    "Observaciones": []
})

df_fallas.to_excel("Fallas_Actualizada.xlsx", index=False)
print("✓ Planilla de Fallas actualizada creada")

# Crear catálogo de tipos de fallas basado en reportes reales
df_tipos_fallas = pd.DataFrame({
    "Categoría Principal": [
        "Problemas de Limpieza",
        "Problemas de Limpieza",
        "Problemas de Limpieza",
        "Daño Físico",
        "Daño Físico",
        "Daño Físico",
        "Problemas de Conectividad",
        "Problemas de Conectividad",
        "Problemas de Conectividad",
        "Problemas Ambientales",
        "Problemas Ambientales",
        "Problemas de Hardware",
        "Problemas de Hardware",
        "Problemas de Hardware",
        "Problemas de Hardware",
        "Problemas de Hardware",
        "Problemas de Hardware"
    ],
    "Tipo de Falla": [
        "Telas de araña",
        "Mancha en lente",
        "Suciedad en carcasa",
        "Mica rallada/dañada",
        "Cámara vandalizada",
        "Poste dañado",
        "Sin conexión",
        "Intermitencia",
        "Cable roto",
        "Empañada/Humedad",
        "Franjas negras visión nocturna",
        "Cámara que se quema",
        "Switch que se quema",
        "Fuente que se quema",
        "POE averiado",
        "UPS averiado",
        "NVR/DVR averiado"
    ],
    "Impacto Típico": [
        "Medio - Visibilidad reducida en visión nocturna",
        "Medio - Calidad de imagen reducida",
        "Bajo - Estética afectada",
        "Alto - No se visualiza con visión nocturna",
        "Alto - Cámara inoperativa",
        "Alto - Múltiples cámaras afectadas",
        "Alto - Cámara completamente inoperativa",
        "Alto - Servicio no confiable",
        "Alto - Pérdida de conexión",
        "Medio - Imagen borrosa",
        "Medio - Visión nocturna comprometida",
        "Alto - Cámara inoperativa",
        "Alto - Múltiples cámaras sin servicio",
        "Alto - Switch sin alimentación",
        "Alto - Cámara PTZ sin alimentación extra",
        "Alto - Pérdida de respaldo eléctrico",
        "Alto - Pérdida de grabaciones"
    ],
    "Tipo de Mantenimiento": [
        "Preventivo - Limpieza",
        "Correctivo - Limpieza especializada",
        "Preventivo - Limpieza",
        "Correctivo - Reemplazo de mica",
        "Correctivo - Reparación/Reemplazo",
        "Correctivo - Reparación estructural",
        "Correctivo - Revisión de conexión",
        "Correctivo - Revisión de conexión/alimentación",
        "Correctivo - Reemplazo de cable",
        "Correctivo - Revisión de sellado",
        "Correctivo - Limpieza o revisión sensor IR",
        "Correctivo - Reemplazo de cámara",
        "Correctivo - Reemplazo de switch",
        "Correctivo - Reemplazo de fuente",
        "Correctivo - Reemplazo de POE",
        "Correctivo - Reparación/Reemplazo UPS",
        "Correctivo - Reparación/Reemplazo NVR"
    ],
    "Prioridad Sugerida": [
        "Baja",
        "Media",
        "Baja",
        "Media",
        "Alta",
        "Alta",
        "Alta",
        "Alta",
        "Alta",
        "Media",
        "Media",
        "Alta",
        "Alta",
        "Alta",
        "Alta",
        "Alta",
        "Alta"
    ],
    "Frecuencia Observada": [
        "Muy Alta (40+ casos)",
        "Baja (1 caso)",
        "Media",
        "Media (6 casos en Ed. O)",
        "Baja",
        "Baja",
        "Media (6 casos)",
        "Media (4 casos)",
        "Baja",
        "Baja (2 casos en Mantenimiento)",
        "Baja (2 casos)",
        "Baja",
        "Baja",
        "Baja",
        "Baja",
        "Baja",
        "Baja"
    ]
})

df_tipos_fallas.to_excel("Catalogo_Tipos_Fallas.xlsx", index=False)
print("✓ Catálogo de Tipos de Fallas creado")

# Crear ejemplos de fallas reales del informe
df_ejemplos_fallas = pd.DataFrame({
    "ID Falla": ["F-2025-001", "F-2025-002", "F-2025-003", "F-2025-004", "F-2025-005"],
    "Fecha de Reporte": ["12/10/2025", "12/10/2025", "12/10/2025", "12/10/2025", "12/10/2025"],
    "Reportado Por": ["Central de Monitoreo", "Central de Monitoreo", "Técnico", "Central de Monitoreo", "Central de Monitoreo"],
    "Tipo de Falla": ["Problemas de Limpieza", "Daño Físico", "Daño Físico", "Problemas de Conectividad", "Problemas de Conectividad"],
    "Subtipo": ["Telas de araña", "Mica rallada/dañada", "Mica rallada/dañada", "Sin conexión", "Intermitencia"],
    "Cámara Afectada": ["Bunker_EX_costado", "ED-O_3P_Salida_Emergencia", "ED-O_1P_Entrada", "Cancha Tenis04", "HOGARES-costado_1"],
    "Ubicación": ["Bunker - Exterior costado", "Edificio O - 3er Piso - Salida Emergencia", "Edificio O - 1er Piso - Entrada", "GORE - Cancha Tenis 04", "Hogares - Costado 1"],
    "Descripción": [
        "Telas de araña en lente, se visualiza con visión nocturna",
        "Mica rallada, informada por técnico. No se visualiza imagen con visión nocturna",
        "Mica rallada. No se visualiza imagen con visión nocturna",
        "Cámara sin conexión",
        "Funciona con intermitencia. Sin conexión"
    ],
    "Impacto en Visibilidad": ["Medio", "Alto", "Alto", "Alto", "Alto"],
    "Afecta Visión Nocturna": ["Sí", "Sí", "Sí", "Sí", "Sí"],
    "Estado": ["Reportada", "Reportada", "Reportada", "Reportada", "Reportada"],
    "Prioridad": ["Baja", "Media", "Media", "Alta", "Alta"],
    "Técnico Asignado": ["Técnico Propio", "Oliver Carrasco", "Marco Altamirano", "ConectaSur", "Técnico Propio"],
    "Observaciones": [
        "Problema frecuente en cámaras exteriores",
        "Parte de 6 cámaras con mismo problema en Edificio O",
        "Parte de 6 cámaras con mismo problema en Edificio O",
        "Verificar conexión de red y alimentación",
        "Posible problema de switch o cable"
    ]
})

df_ejemplos_fallas.to_excel("Ejemplos_Fallas_Reales.xlsx", index=False)
print("✓ Ejemplos de Fallas Reales creados")

print("\n=== RESUMEN ===")
print("Total de tipos de fallas catalogados:", len(df_tipos_fallas))
print("Fallas más frecuentes: Telas de araña (40+ casos)")
print("Problema sistemático detectado: Edificio O - 6 cámaras con mica rallada")

