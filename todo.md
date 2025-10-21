# Plan de Implementación - Eliminación de Redundancias Sistema Cámaras UFRO

**Fecha:** 2025-10-20
**Estado:** Pendiente aprobación usuario

## FASE 1: REESTRUCTURACIÓN BASE DE DATOS SQLITE

### [PENDIENTE] Tarea 1: Backup Completo del Sistema
- Crear backup de `sistema_camaras.db`
- Crear backup de todas las planillas Excel
- Guardar en carpeta `backups/`

### [PENDIENTE] Tarea 2: Consolidar Tablas de Fallas (CRÍTICO)
- Crear nueva tabla `fallas` unificada con todos los campos necesarios
- Migrar 8 registros de `fallas_especificas`
- Migrar 5 registros de `casos_reales`
- Eliminar duplicados durante migración (Caso CFT Prat)
- DROP TABLE `fallas_especificas`, `casos_reales`
- Verificar integridad de datos migrados

### [PENDIENTE] Tarea 3: Limpiar Duplicados en Tabla `tecnicos` (CRÍTICO)
- DELETE todos los registros actuales (16 duplicados)
- INSERT 4 técnicos únicos:
  * Oliver Carrasco
  * Marcos Altamirano
  * Charles Jélvez
  * Marco Contreras
- Verificar count = 4

### [PENDIENTE] Tarea 4: Eliminar Duplicados en `mantenimientos_realizados`
- Identificar registros duplicados
- Mantener solo 1 registro por mantenimiento único
- Verificar integridad

### [PENDIENTE] Tarea 5: Normalizar Ubicaciones en BD
- Crear tabla `ubicaciones` con estructura completa
- Extraer ubicaciones únicas de tablas existentes
- Agregar columna `ubicacion_id` (FK) a tablas:
  * `camaras`
  * `infraestructura_red`
  * `fallas` (nueva tabla consolidada)
- Migrar datos de ubicación
- Eliminar columnas redundantes (campus, edificio, piso)

### [PENDIENTE] Tarea 6: Estandarizar Estados de Fallas
- Crear tabla `estados_falla` con 6 estados del workflow
- Agregar constraint a tabla `fallas`
- Actualizar registros existentes con estados válidos

---

## FASE 2: CONSOLIDACIÓN PLANILLAS EXCEL

### [PENDIENTE] Tarea 7: Eliminar Archivo Redundante de Cámaras (CRÍTICO)
- Verificar que `Listadecámaras_modificada.xlsx` contiene toda la info
- Mover `Listadecámaras.xlsx` a carpeta `archivos_obsoletos/`
- Documentar cambio

### [PENDIENTE] Tarea 8: Crear Planilla `UPS.xlsx`
- Estructura: ID UPS, Modelo, Marca, Capacidad (VA), Nº Baterías, Gabinete, Ubicación, Campus, Estado, Fecha Instalación, Equipos que Alimenta, Observaciones
- Extraer datos de `Equipos_Tecnicos.xlsx`
- Agregar datos del mantenimiento UPS Edificio O documentado

### [PENDIENTE] Tarea 9: Crear Planilla `NVR_DVR.xlsx`
- Estructura: ID NVR, Tipo (NVR/DVR), Modelo, Marca, Nº Canales, Cámaras Conectadas, IP, Ubicación, Campus, Estado, Observaciones
- Extraer datos de `Equipos_Tecnicos.xlsx`
- Relacionar con `Listadecámaras_modificada.xlsx`

### [PENDIENTE] Tarea 10: Crear Planilla `Fuentes_Poder.xlsx`
- Estructura: ID Fuente, Modelo, Voltaje, Amperaje, Equipos que Alimenta, Gabinete, Ubicación, Campus, Estado, Observaciones
- Crear estructura base (datos a completar por usuario)

### [PENDIENTE] Tarea 11: Normalizar Ubicaciones en Planillas Excel
- Usar `Ubicaciones.xlsx` como tabla maestra
- Agregar columna `ID Ubicación` a:
  * `Listadecámaras_modificada.xlsx`
  * `Gabinetes.xlsx`
  * `Switches.xlsx`
  * `UPS.xlsx` (nueva)
  * `NVR_DVR.xlsx` (nueva)
  * `Fuentes_Poder.xlsx` (nueva)
- Eliminar columnas redundantes de campus/edificio
- Poblar IDs de ubicación basándose en coincidencias

### [PENDIENTE] Tarea 12: Organizar Archivos de Fallas
- Mantener 3 archivos con propósitos claros:
  * `Catalogo_Tipos_Fallas.xlsx` → Catálogo de referencia
  * `Ejemplos_Fallas_Reales.xlsx` → Casos de estudio documentados
  * `Fallas_Actualizada.xlsx` → Registro operativo (plantilla)
- Documentar flujo de trabajo para registro de fallas

---

## FASE 3: VALIDACIONES Y SCRIPTS

### [PENDIENTE] Tarea 13: Implementar Validación Anti-Duplicados
- Crear función `validar_falla_antes_insertar()`
- Verificar fallas previas por cámara
- Permitir inserción solo si última falla está cerrada/cancelada
- Integrar en script de migración

### [PENDIENTE] Tarea 14: Script de Migración Excel → BD Unificado
- Crear `migrate_excel_to_db_unificado.py`
- Leer planillas Excel consolidadas
- Validar datos (sin duplicados, estados válidos)
- Insertar en SQLite con transacciones
- Generar log detallado de operaciones

### [PENDIENTE] Tarea 15: Verificación Final
- Verificar counts de todas las tablas
- Ejecutar queries de prueba
- Verificar integridad referencial (FK)
- Generar informe de validación

---

## FASE 4: AGREGAR FALLAS DEL INFORME WORD

### [PENDIENTE] Tarea 16: Extraer y Agregar Casos del INFORME DE CAMARAS.docx
- Procesar archivo Word
- Aplicar validación anti-duplicados
- Insertar fallas en tabla consolidada
- Actualizar planillas Excel correspondientes

---

## FASE 5: DOCUMENTACIÓN

### [PENDIENTE] Tarea 17: Actualizar Documentación del Proyecto
- Actualizar `memory/proyecto_camaras_ufro.md`
- Documentar cambios en estructura de BD
- Documentar nuevas planillas creadas
- Crear guía de uso de planillas normalizadas

### [PENDIENTE] Tarea 18: Generar Informe Final
- Crear `docs/INFORME_ELIMINACION_REDUNDANCIAS.md`
- Incluir estadísticas antes/después
- Documentar beneficios obtenidos
- Incluir recomendaciones de mantenimiento

---

## RESUMEN DE PRIORIDADES

### 🔴 CRÍTICAS (hacer primero)
- Tarea 1: Backup completo
- Tarea 2: Consolidar tablas de fallas
- Tarea 3: Limpiar duplicados técnicos
- Tarea 7: Eliminar archivo redundante cámaras

### 🟡 ALTAS
- Tarea 4: Duplicados mantenimientos
- Tarea 5: Normalizar ubicaciones BD
- Tarea 8-10: Crear planillas faltantes
- Tarea 11: Normalizar ubicaciones Excel
- Tarea 13: Validación anti-duplicados

### 🟢 MEDIAS
- Tarea 6: Estandarizar estados
- Tarea 12: Organizar archivos fallas
- Tarea 14: Script migración
- Tarea 15: Verificación final

### 📝 DOCUMENTACIÓN
- Tarea 16: Agregar fallas INFORME Word
- Tarea 17-18: Documentación final

---

## ESTIMACIÓN DE TIEMPO
- FASE 1: ~2-3 horas
- FASE 2: ~2-3 horas
- FASE 3: ~1-2 horas
- FASE 4: ~1 hora
- FASE 5: ~1 hora

**TOTAL: 7-10 horas de trabajo**

---

## PRÓXIMO PASO
Esperar confirmación del usuario para proceder con la implementación.
