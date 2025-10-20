# Proyecto: Sistema de Gestión de Cámaras UFRO

## Estado Actual
- **Repositorio GitHub**: https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro
- **Tecnología**: Flask (Python) + SQLite/PostgreSQL
- **Estado**: Código existente con funcionalidades parciales implementadas

## Tareas Completadas
- ✓ Analizado código base existente
- ✓ Revisado estructura de archivos Excel

## Tareas en Progreso
- Desarrollo completo Flask + React para Railway
- Migración de datos desde Excel
- Sistema fullstack con PostgreSQL

## Información Crítica del Sistema
- **Total cámaras**: 474 (según INFORME DE CAMARAS.docx)
- **Ubicaciones**: 61 edificios/áreas diferentes
- **Tipos de fallas**: Telas de araña, borrosa, mica rallada, desconectada, mancha en lente, empañada, intermitencia, etc.

## Requisito Clave: Doble Entrada de Fallas
1. **Carga inicial**: Migración desde archivos Excel (datos históricos)
2. **Registro en tiempo real**: Formularios web para reportar nuevas fallas

## Equipos a Gestionar (con Altas/Bajas)
1. **Cámaras** (474 unidades)
2. **Gabinetes**
3. **Switches**
4. **UPS**
5. **NVR/DVR**
6. **Fuentes de poder**

## Requisitos de Ubicación
- Cada equipo debe tener ubicación precisa (Campus, Edificio, Piso, Descripción exacta)
- Sistema debe mostrar dónde está cada equipo físicamente

## Historial de Altas y Bajas
- Registrar fecha de alta de cada equipo
- Registrar fecha de baja con motivo (falla, vandalismo, obsolescencia)
- Estado del equipo: Activo, Inactivo, Baja Temporal, Baja Definitiva

## Sistema de Gestión de Fallas
**Estados propuestos:**
1. **Pendiente** - Falla reportada, sin asignar
2. **Asignada** - Asignada a técnico, sin iniciar
3. **En Proceso** - Técnico trabajando en la reparación
4. **Reparada** - Falla resuelta exitosamente
5. **Cerrada** - Falla verificada y cerrada
6. **Cancelada** - Falla cancelada (duplicada, error)

**Registro de reparación:**
- Técnico que reparó (obligatorio al marcar como reparada)
- Fecha/hora de inicio de reparación
- Fecha/hora de finalización
- Solución aplicada (descripción)
- Costo de reparación (opcional)
- Materiales utilizados

## Desarrollo en Curso
Sistema Flask + Jinja2 para Railway con:
- Backend Flask con API REST y SQLAlchemy
- Frontend con Jinja2 (server-side rendering)
- Script migración desde 12 archivos Excel
- PostgreSQL en Railway
- CRUD completo para: Cámaras, Gabinetes, Switches, UPS, NVR/DVR, Fuentes Poder
- Sistema de altas/bajas con historial completo
- Gestión de fallas con workflow completo y asignación de técnicos
- Formularios web para registro de fallas en tiempo real
- Mapas de red con Mermaid.js mostrando ubicación de equipos
- Reportes Excel descargables
