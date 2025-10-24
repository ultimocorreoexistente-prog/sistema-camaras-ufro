# Flujo de Trabajo para Gestión de Fallas - Sistema Cámaras UFRO

**Fecha:** 2025-10-20  
**Versión:** 1.0

## 🎯 Objetivo

Este documento define el flujo de trabajo estandarizado para el registro, seguimiento y documentación de fallas en el sistema de cámaras UFRO, utilizando las 3 planillas Excel consolidadas.

---

## 📁 Arquitectura de Archivos de Fallas

### **1. Catalogo_Tipos_Fallas.xlsx** 📘

**Propósito:** Catálogo de referencia de tipos de fallas estándar  
**Uso:** Solo lectura (no modificar durante operaciones diarias)  
**Actualización:** Cuando se descubre un nuevo tipo de falla recurrente

**Contenido:**
- Categoría Principal (LIMPIEZA, REPARACION, TÉCNICA, etc.)
- Tipo de Falla
- Impacto Típico
- Tipo de Mantenimiento
- Prioridad Sugerida
- Frecuencia Observada

**Cuándo actualizar:**
- ✅ Cuando un tipo de falla se repite 3+ veces
- ✅ Cuando se identifica un patrón nuevo
- ❌ NO para fallas únicas o casos aislados

---

### **2. Fallas_Actualizada.xlsx** 📝

**Propósito:** Registro operativo de fallas en curso y recientes  
**Uso:** **ESCRITURA ACTIVA** - Aquí se registran todas las fallas nuevas  
**Actualización:** Diaria / En tiempo real

**Contenido:**
- ID Falla (auto-incremental)
- Fecha de Reporte
- Reportado Por
- Tipo de Falla (usar catálogo)
- Cámara Afectada
- Ubicación
- Descripción
- Estado de Reparación (Pendiente, Asignada, En Proceso, Reparada, Cerrada, Cancelada)
- Técnico Asignado
- Solución Aplicada
- Costo

**Flujo de trabajo:**

```
1. REPORTE DE FALLA
   → Usuario/Supervisor detecta falla
   → Registra en Fallas_Actualizada.xlsx
   → Estado: "Pendiente"
   → Asigna prioridad (Baja/Media/Alta/Crítica)

2. ASIGNACIÓN
   → Supervisor asigna técnico
   → Actualiza "Técnico Asignado"
   → Estado: "Asignada"
   → Fecha de Asignación

3. TRABAJO EN CURSO
   → Técnico inicia reparación
   → Estado: "En Proceso"
   → Fecha Inicio Reparación

4. REPARACIÓN COMPLETADA
   → Técnico completa trabajo
   → Registra "Solución Aplicada"
   → Registra materiales y costo
   → Estado: "Reparada"
   → Fecha Fin Reparación

5. VERIFICACIÓN Y CIERRE
   → Supervisor verifica solución
   → Estado: "Cerrada"
   → Fecha de Cierre
   
   → SI ES CASO RELEVANTE → Migrar a Ejemplos_Fallas_Reales.xlsx
```

---

### **3. Ejemplos_Fallas_Reales.xlsx** 📖

**Propósito:** Casos de estudio y documentación de lecciones aprendidas  
**Uso:** Solo escritura de casos RELEVANTES ya cerrados  
**Actualización:** Mensual o cuando hay casos significativos

**Contenido:**
- Casos de fallas complejas o instructivas
- Fallas que afectaron múltiples cámaras
- Incidentes que generaron lecciones aprendidas
- Problemas de infraestructura crítica

**Criterios para migrar una falla desde Fallas_Actualizada.xlsx:**

✅ **SÍ migrar si:**
- Falla afectó 3+ cámaras
- Tiempo de downtime > 4 horas
- Costo de reparación > $30,000
- Reveló problema de diseño o infraestructura
- Generó lecciones aprendidas valiosas
- Requirió solución innovadora o no estándar

❌ **NO migrar si:**
- Falla simple y rutinaria
- Un solo equipo afectado
- Resolución estándar (ej: limpieza de lente)
- Sin impacto significativo

**Formato de documentación:**
- Título descriptivo del caso
- Descripción completa del problema
- Componentes involucrados
- Dependencias en cascada
- Solución aplicada (paso a paso)
- Tiempo total de resolución
- Lecciones aprendidas
- Recomendaciones preventivas

**Ejemplos actuales documentados:**
1. Telas de araña - Bunker (12/10/2024)
2. Mantenimiento UPS Edificio O (13/10/2024)
3. Falla Cable NVR CFT Prat (14-15/10/2024)
4. Caída cámaras ZM - Falla Eléctrica (17/10/2024)

---

## 🔄 Flujo Operativo Completo

### **DIA A DIA:**

```
NUEVA FALLA
   ↓
Fallas_Actualizada.xlsx ←←← REGISTRO AQUÍ
   ↓
[Workflow: Pendiente → Asignada → En Proceso → Reparada → Cerrada]
   ↓
¿Es caso relevante?
   │
   ├─ NO → Mantener en Fallas_Actualizada.xlsx (archivar después de 6 meses)
   │
   └─ SÍ → Copiar a Ejemplos_Fallas_Reales.xlsx (documentar lecciones)
```

### **MENSUALMENTE:**

1. **Revisar Fallas_Actualizada.xlsx:**
   - Verificar que todas las fallas cerradas tengan solución registrada
   - Identificar casos relevantes para documentar
   - Archivar fallas antiguas (>6 meses) a Excel de archivo histórico

2. **Actualizar Catalogo_Tipos_Fallas.xlsx:**
   - Analizar patrones de fallas recurrentes
   - Agregar nuevos tipos si es necesario
   - Actualizar frecuencias observadas

3. **Documentar casos en Ejemplos_Fallas_Reales.xlsx:**
   - Seleccionar casos cerrados relevantes del mes
   - Escribir documentación completa con lecciones aprendidas
   - Compartir con equipo técnico

---

## ✅ Validación Anti-Duplicados (OBLIGATORIA)

**Antes de registrar una nueva falla:**

1. 🔍 **Buscar en Fallas_Actualizada.xlsx:**
   - Filtrar por "Cámara Afectada"
   - Verificar columna "Estado de Reparación"

2. ⚠️ **Validación:**
   - ❌ **NO INSERTAR** si existe falla en estado:
     * Pendiente
     * Asignada
     * En Proceso
     * Reparada (aún no cerrada)
   
   - ✅ **SÍ INSERTAR** si:
     * No hay falla previa para esa cámara
     * La última falla está "Cerrada" o "Cancelada"

3. 📝 **Acción en caso de duplicado:**
   - Actualizar la falla existente
   - NO crear nuevo registro
   - Agregar nota en "Observaciones"

---

## 📊 Estados del Workflow (6 estados)

| Estado | Descripción | Responsable | Siguiente Estado |
|--------|--------------|-------------|------------------|
| **Pendiente** | Falla reportada, sin asignar | Supervisor | Asignada |
| **Asignada** | Técnico asignado, aún no inicia | Técnico | En Proceso |
| **En Proceso** | Técnico trabajando activamente | Técnico | Reparada |
| **Reparada** | Reparación completada, pendiente verificación | Supervisor | Cerrada |
| **Cerrada** | Verificada y cerrada oficialmente | N/A | (fin) |
| **Cancelada** | Duplicada, error o falsa alarma | Supervisor | (fin) |

---

## 📦 Archivado de Fallas Antiguas

**Cada 6 meses:**

1. Crear archivo: `Fallas_Archivo_YYYYMM.xlsx`
2. Mover fallas cerradas de Fallas_Actualizada.xlsx al archivo
3. Mantener solo fallas de los últimos 6 meses en la planilla activa
4. Guardar archivos históricos en carpeta `historial_fallas/`

---

## 🛠️ Integración con Sistema Web (Futuro)

Cuando se implemente el sistema web Flask:

- **Base de datos:** Tabla `fallas` unificada (ya creada)
- **Formulario web:** Registro de fallas en tiempo real
- **Sincronización:** Script de migración Excel ↔ BD
- **Validación automática:** Anti-duplicados implementado en backend
- **Dashboard:** Visualización de estadísticas y estados

---

## 📌 Resumen de Archivos

| Archivo | Propósito | Frecuencia de Uso | Responsable |
|---------|-----------|-------------------|-------------|
| **Catalogo_Tipos_Fallas.xlsx** | 📘 Referencia | Consulta diaria, actualización mensual | Supervisor |
| **Fallas_Actualizada.xlsx** | 📝 Registro activo | Diario/Tiempo real | Técnicos + Supervisor |
| **Ejemplos_Fallas_Reales.xlsx** | 📖 Casos de estudio | Mensual | Supervisor |

---

**Última actualización:** 2025-10-20  
**Próxima revisión:** 2025-11-20
