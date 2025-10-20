# Especificación Completa - Sistema de Gestión de Cámaras UFRO

**Última actualización**: 2025-10-20
**Estado**: Plan aprobado por usuario, listo para desarrollo

## Resumen Ejecutivo
Sistema web fullstack Flask + Jinja2 para gestionar 474 cámaras de seguridad distribuidas en 61 ubicaciones de la Universidad de La Frontera (UFRO), con 4 campus principales: Andrés Bello, Pucón, Angol y Medicina.

## Stack Tecnológico
- **Backend**: Flask (Python)
- **Frontend**: Jinja2 (server-side rendering) + Bootstrap/Tailwind
- **Base de Datos**: PostgreSQL (Railway) / SQLite (desarrollo local)
- **ORM**: SQLAlchemy
- **Deployment**: Railway (gunicorn)
- **Visualización**: Mermaid.js (topología de red), Chart.js (gráficos dashboard), Leaflet.js (geolocalización)
- **Reportes**: openpyxl (Excel), CSS @media print (impresión)

## Equipos a Gestionar (con Altas/Bajas)
1. **Cámaras** (474 unidades)
2. **Gabinetes**
3. **Switches**
4. **UPS**
5. **NVR/DVR**
6. **Fuentes de Poder**

## Modelos de Base de Datos (14 tablas)

### Usuario
- id, username, password_hash, rol, nombre_completo, email, telefono
- Roles: admin, supervisor, tecnico, visualizador

### Ubicacion
- id, campus, edificio, piso, descripcion, latitud, longitud

### Camara
- id, codigo, nombre, ip, modelo, fabricante, ubicacion_id, gabinete_id, switch_id, puerto_switch_id, nvr_id
- estado, fecha_alta, fecha_baja, motivo_baja, latitud, longitud

### Gabinete
- id, codigo, nombre, ubicacion_id, capacidad, estado, fecha_alta, fecha_baja, motivo_baja, latitud, longitud

### Switch
- id, codigo, nombre, ip, modelo, marca, gabinete_id, puertos_totales, estado, fecha_alta, fecha_baja, motivo_baja, latitud, longitud

### UPS
- id, codigo, modelo, marca, capacidad_va, ubicacion_id, gabinete_id, estado, fecha_alta, fecha_baja, motivo_baja, latitud, longitud

### NVR_DVR
- id, codigo, tipo, modelo, marca, canales, ubicacion_id, ip, estado, fecha_alta, fecha_baja, motivo_baja, latitud, longitud

### Fuente_Poder
- id, codigo, modelo, voltaje, amperaje, ubicacion_id, estado, fecha_alta, fecha_baja, motivo_baja, latitud, longitud

### Puerto_Switch
- id, switch_id, numero_puerto, camara_id, estado

### Falla
- id, equipo_tipo, equipo_id, tipo_falla_id, descripcion, fecha_reporte, reportado_por_id
- estado, fecha_asignacion, tecnico_asignado_id, fecha_inicio_reparacion, fecha_fin_reparacion
- solucion_aplicada, costo_reparacion, materiales_utilizados

### Catalogo_Tipo_Falla
- id, nombre, descripcion, gravedad
- Tipos: Telas de araña, Borrosa, Mica rallada, Desconectada, Mancha en lente, Empañada, Intermitencia, etc.

### Mantenimiento
- id, equipo_tipo, equipo_id, tipo, fecha, tecnico_id, descripcion, observaciones, costo

### Equipo_Tecnico
- id, nombre, especialidad, telefono, email, estado

### Historial_Estado_Equipo
- id, equipo_tipo, equipo_id, estado_anterior, estado_nuevo, fecha_cambio, motivo, usuario_id

## Sistema de Estados de Fallas (Workflow)

1. **Pendiente** → Falla reportada, esperando asignación
2. **Asignada** → Técnico asignado pero aún no comienza
3. **En Proceso** → Técnico trabajando activamente en la reparación
4. **Reparada** → Técnico completó la reparación (registra: solución, materiales, costo)
5. **Cerrada** → Supervisor verificó y cerró la falla
6. **Cancelada** → Falla duplicada o reportada por error

**Transiciones permitidas**:
- Pendiente → Asignada (admin/supervisor asigna técnico)
- Asignada → En Proceso (técnico inicia trabajo)
- En Proceso → Reparada (técnico completa, registra solución)
- Reparada → Cerrada (supervisor verifica y cierra)
- Cualquier estado → Cancelada (admin/supervisor)

## Funcionalidades Principales

### 1. Autenticación y Autorización
- Login con roles y permisos
- Usuarios por defecto: admin/admin123, tecnico1/tecnico123, supervisor/super123

### 2. Dashboard Interactivo
- Total cámaras operativas/no operativas
- Fallas pendientes/en proceso/reparadas
- Mantenimientos del mes
- Gráficos en tiempo real (Chart.js)

### 3. Gestión de Equipos (CRUD Completo)
- Lista con filtros por campus, edificio, estado
- Formularios de alta (con geolocalización)
- Formularios de baja (con motivo)
- Vista detalle con historial completo

### 4. Gestión de Fallas
- Registro manual y automático de incidentes
- Doble entrada: carga desde Excel + formularios web
- Seguimiento de estado (workflow de 6 estados)
- Asignación de técnicos
- Registro de reparación con solución aplicada
- Historial completo de intervenciones

### 5. Mapas de Red (Mermaid.js)
- Mapa completo de la infraestructura
- Mapas en cascada por ubicación
- Visualización jerárquica: Core Switch → Switch → Gabinete → UPS → Cámara
- Filtros por campus

### 6. Geolocalización (Leaflet.js o Google Maps)
- Mapa interactivo mostrando ubicación física de cada equipo
- Marcadores por tipo de equipo (cámara, gabinete, switch, UPS)
- Click en marcador para ver detalles del equipo
- Filtros por campus y tipo de equipo

### 7. Informes Avanzados
- Inventarios por campus (cámaras, gabinetes, switches)
- Análisis de fallas por tipo y frecuencia
- Reportes de mantenimiento preventivo
- Estadísticas de tiempo de resolución por técnico
- Exportación a Excel y PNG
- **Impresión optimizada** (CSS @media print)

### 8. Responsive Design
- Adaptado para móviles y tablets
- Interfaz touch-friendly para técnicos en campo

## URLs Principales del Sistema

- `/` - Dashboard principal
- `/login` - Autenticación
- `/camaras` - Gestión de cámaras
- `/gabinetes` - Gestión de gabinetes
- `/switches` - Gestión de switches
- `/ups` - Gestión de UPS
- `/nvr` - Gestión de NVR/DVR
- `/fuentes` - Gestión de fuentes de poder
- `/fallas` - Gestión de fallas
- `/fallas/nueva` - Formulario reportar falla
- `/fallas/<id>/asignar` - Asignar técnico
- `/fallas/<id>/reparar` - Registrar reparación
- `/mantenimientos` - Registro de mantenimientos
- `/mapa-red` - Topología de red (Mermaid.js)
- `/mapa-geolocalizacion` - Mapa interactivo (Leaflet.js)
- `/informes-avanzados` - Reportes y mapas

## Archivos del Proyecto

### Código Base
- `app.py` - Aplicación Flask principal
- `models.py` - Modelos SQLAlchemy
- `migrate_excel_to_db.py` - Script migración de datos

### Configuración
- `requirements.txt` - Dependencias Python
- `Procfile` - Configuración Railway: `web: gunicorn app:app`
- `railway.json` - Configuración deployment
- `.env.example` - Variables de entorno

### Templates (Jinja2)
- `base.html` - Layout base
- `login.html` - Login
- `dashboard.html` - Dashboard
- Para cada equipo:
  - `{equipo}_list.html`
  - `{equipo}_form_alta.html`
  - `{equipo}_form_baja.html`
  - `{equipo}_detalle.html`
- Fallas:
  - `fallas_list.html`
  - `fallas_form.html`
  - `fallas_workflow.html`
  - `fallas_asignar.html`
  - `fallas_reparar.html`
- Mapas:
  - `mapa_campus.html` (Mermaid.js)
  - `mapa_geolocalizacion.html` (Leaflet.js)
- `informes_avanzados.html`

### Estáticos
- `static/css/style.css` - Estilos personalizados
- `static/css/print.css` - Estilos de impresión
- `static/js/main.js` - JavaScript principal
- `static/js/maps.js` - Integración mapas
- `static/js/charts.js` - Gráficos dashboard

## Datos a Migrar (12 archivos Excel)

1. `Listadecámaras.xlsx` o `Listadecámaras_modificada.xlsx` (474 cámaras)
2. `Ubicaciones.xlsx`
3. `Gabinetes.xlsx`
4. `Switches.xlsx`
5. `Puertos_Switch.xlsx`
6. `Catalogo_Tipos_Fallas.xlsx`
7. `Fallas_Actualizada.xlsx`
8. `Ejemplos_Fallas_Reales.xlsx` (6 casos reales documentados)
9. `Mantenimientos.xlsx`
10. `Equipos_Tecnicos.xlsx`
11-12. Datos adicionales de UPS, NVR/DVR, Fuentes de Poder (crear ejemplos)

## Campus Incluidos

1. **Andrés Bello** (Campus Principal)
2. **Pucón**
3. **Angol**
4. **Medicina**

## Dependencias Python (requirements.txt)

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
pandas==2.1.3
openpyxl==3.1.2
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

## Variables de Entorno (.env.example)

```
DATABASE_URL=postgresql://user:password@localhost/camaras_ufro
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

## Instrucciones de Deployment Railway

1. Crear proyecto en Railway
2. Conectar repositorio GitHub
3. Agregar PostgreSQL database
4. Railway asigna DATABASE_URL automáticamente
5. Deploy automático con `gunicorn app:app`

## Plan de Desarrollo (5 pasos)

1. **Modelos de Base de Datos** (models.py) - 14 modelos SQLAlchemy
2. **Script de Migración** (migrate_excel_to_db.py) - Poblar BD desde Excel
3. **Backend Flask** (app.py) - Rutas, lógica, API
4. **Frontend Jinja2** (templates/) - Todas las vistas
5. **Deployment Railway** - Configuración y pruebas

## Estado Actual

✅ Requisitos recopilados
✅ Plan aprobado por usuario
⏳ Pendiente: Implementación completa

---

**Repositorio GitHub**: https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro
**Directorio de trabajo**: `sistema-camaras-ufro-main/`
