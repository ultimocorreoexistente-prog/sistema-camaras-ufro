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

## Desarrollo en Curso
Sistema Flask + Jinja2 para Railway con:
- Backend Flask con API REST y SQLAlchemy
- Frontend con Jinja2 (server-side rendering)
- Script migración desde 12 archivos Excel
- PostgreSQL en Railway
- CRUD completo para: Cámaras, Gabinetes, Switches, Fallas, Mantenimientos
- Formularios web para registro de fallas en tiempo real
- Mapas de red con Mermaid.js
- Reportes Excel descargables
