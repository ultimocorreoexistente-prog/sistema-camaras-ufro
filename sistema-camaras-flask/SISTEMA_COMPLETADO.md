# Sistema de Gestión de Cámaras UFRO - COMPLETADO

## Resumen del Proyecto

Sistema web fullstack desarrollado con Flask + Jinja2 para gestionar 474 cámaras de seguridad en 4 campus de la Universidad de La Frontera.

## Estado: COMPLETADO ✓

**Fecha de Finalización:** 2025-10-21
**Ubicación:** `/workspace/sistema-camaras-flask/`

## Estructura del Proyecto

```
sistema-camaras-flask/
├── app.py                      # Aplicación Flask principal (500+ líneas)
├── models.py                   # 14 modelos SQLAlchemy
├── migrate_data.py             # Script migración de 13 Excel
├── init_db.py                  # Script inicialización BD
├── requirements.txt            # Dependencias Python
├── Procfile                    # Config Gunicorn
├── railway.json                # Config Railway
├── .env.example                # Variables de entorno
├── .gitignore                  
├── README.md                   # Documentación completa
├── DEPLOYMENT.md               # Guía deployment Railway
├── templates/                  # 16 templates Jinja2
│   ├── base.html              # Layout base con Bootstrap 5
│   ├── login.html             # Autenticación
│   ├── dashboard.html         # Dashboard con gráficos
│   ├── camaras_*              # CRUD cámaras
│   ├── gabinetes_*            # CRUD gabinetes
│   ├── gabinetes_mantencion   # ⚠️ VISTA CRÍTICA mantención
│   ├── fallas_*               # Gestión fallas con workflow
│   ├── mantenimientos_*       # Registro mantenimientos
│   ├── mapa_red.html          # Topología Mermaid.js
│   ├── mapa_geolocalizacion   # Leaflet.js
│   └── informes_avanzados     # Reportes Excel/PNG
├── static/
│   ├── css/
│   │   ├── style.css          # Estilos personalizados
│   │   └── print.css          # @media print
│   └── js/
│       ├── main.js            # Funciones generales
│       ├── fallas_validation  # ⚠️ VALIDACIÓN ANTI-DUPLICADOS
│       ├── maps.js            # Leaflet.js
│       └── charts.js          # Chart.js
└── planillas/                 # 13 archivos Excel fuente
    ├── Ubicaciones.xlsx
    ├── Equipos_Tecnicos.xlsx
    ├── Catalogo_Tipos_Fallas.xlsx
    ├── Gabinetes.xlsx
    ├── Switches.xlsx
    ├── Puertos_Switch.xlsx
    ├── UPS.xlsx
    ├── NVR_DVR.xlsx
    ├── Fuentes_Poder.xlsx
    ├── Listadecámaras_modificada.xlsx (474 cámaras)
    ├── Fallas_Actualizada.xlsx
    ├── Ejemplos_Fallas_Reales.xlsx
    └── Mantenimientos.xlsx
```

## Funcionalidades Implementadas

### 1. Autenticación y Roles
- Flask-Login integrado
- 4 roles: admin, supervisor, tecnico, visualizador
- Usuarios por defecto creados automáticamente
- Decoradores @role_required para control de acceso

### 2. Dashboard Interactivo
- Estadísticas en tiempo real (total cámaras, fallas, mantenimientos)
- Gráficos Chart.js (dona, barras)
- Lista de últimas fallas reportadas
- Cards con indicadores visuales

### 3. CRUD Completo de Equipos (6 tipos)
- **Cámaras (474 unidades)**
- Gabinetes
- Switches
- UPS
- NVR/DVR
- Fuentes de Poder

Cada tipo incluye:
- Listado con filtros (campus, estado, búsqueda)
- Formulario alta/baja
- Vista detalle completa
- Historial de cambios de estado
- Fallas asociadas
- Mantenimientos registrados

### 4. Vista Mantención de Gabinetes (⚠️ CRÍTICA)

Ruta: `/gabinetes/<id>/mantencion`

Muestra de forma organizada:
- Información del gabinete
- **Switches en este gabinete** (tabla con modelo, IP, puertos totales/usados)
- **NVR/DVR en este gabinete** (tabla con tipo, modelo, canales)
- **UPS en este gabinete** (tabla con modelo, capacidad VA, baterías)
- **Fuentes de Poder en este gabinete** (tabla con modelo, voltaje, amperaje)
- Historial completo de mantenimientos y reparaciones
- Botón para registrar nuevo mantenimiento/reparación

### 5. Sistema de Fallas - Workflow 6 Estados

**Estados:**
1. Pendiente (reportada, sin asignar)
2. Asignada (técnico asignado, sin iniciar)
3. En Proceso (técnico trabajando)
4. Reparada (reparación completada)
5. Cerrada (verificada y cerrada por supervisor)
6. Cancelada (cancelada por admin/supervisor)

**Transiciones:**
- Pendiente → Asignada (admin/supervisor asigna técnico)
- Asignada → En Proceso (técnico inicia trabajo)
- En Proceso → Reparada (técnico completa, OBLIGATORIO registrar solución)
- Reparada → Cerrada (supervisor verifica)
- Cualquier estado → Cancelada (admin/supervisor)

### 6. Validación Anti-Duplicados (⚠️ REQUISITO CRÍTICO)

**Regla:** No permitir reportar nueva falla si existe una falla con estado Pendiente, Asignada o En Proceso para el mismo equipo.

**Implementación en 4 niveles:**

1. **Backend (app.py):**
```python
def validar_falla_duplicada(equipo_tipo, equipo_id):
    falla_activa = Falla.query.filter_by(
        equipo_tipo=equipo_tipo,
        equipo_id=equipo_id
    ).filter(
        Falla.estado.in_(['Pendiente', 'Asignada', 'En Proceso'])
    ).order_by(Falla.fecha_reporte.desc()).first()
    
    if falla_activa:
        return {'permitir': False, 'mensaje': '...', 'falla_existente': falla_activa}
    return {'permitir': True, 'mensaje': 'OK', 'falla_existente': None}
```

2. **API REST:**
- Endpoint: `GET /api/fallas/validar?equipo_tipo=Camara&equipo_id=123`
- Retorna JSON con resultado de validación

3. **Frontend (fallas_validation.js):**
- Validación AJAX en tiempo real
- Al seleccionar equipo, consulta API
- Muestra alerta si hay falla duplicada
- Deshabilita botón submit si no se permite

4. **Script Migración (migrate_data.py):**
- Valida cada falla antes de insertar desde Excel
- Rechaza duplicados
- Log detallado de fallas rechazadas

### 7. Gestión de Mantenimientos
- Tipos: Preventivo, Correctivo, Predictivo
- Asociación a cualquier tipo de equipo
- Registro de materiales, tiempo, costo
- Historial completo por equipo

### 8. Mapas y Visualización

**Topología de Red (Mermaid.js):**
- Diagrama jerárquico: Core → Gabinete → Switch → Equipos
- Filtros por campus
- Generación dinámica desde BD

**Geolocalización (Leaflet.js):**
- Marcadores de cámaras (azul)
- Marcadores de gabinetes (rojo)
- Popups con información
- Filtros por tipo y estado

### 9. Reportes y Exportación
- Estadísticas por campus
- Análisis de fallas por tipo
- Reportes de mantenimientos
- Exportación a Excel (openpyxl)
- Impresión optimizada (CSS @media print)

### 10. Responsive Design
- Bootstrap 5 mobile-first
- Menú hamburguesa en móviles
- Tablas con scroll horizontal
- Formularios optimizados para táctil

## Archivos de Configuración

### requirements.txt
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

### Procfile
```
web: gunicorn app:app
```

### railway.json
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Deployment en Railway

### Pasos:

1. **Crear proyecto en Railway:**
   - New Project → Deploy from GitHub repo
   - Seleccionar repositorio

2. **Agregar PostgreSQL:**
   - + New → Database → PostgreSQL

3. **Configurar variables de entorno:**
   ```
   DATABASE_URL=postgresql://... (auto)
   SECRET_KEY=<generar-clave-secreta>
   FLASK_ENV=production
   ```

4. **Inicializar BD (Railway CLI):**
   ```bash
   railway run flask init-db
   railway run python migrate_data.py
   ```

5. **Verificar deployment:**
   - Login con admin/admin123
   - Verificar datos migrados

## Usuarios por Defecto

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| admin | admin123 | admin | Acceso completo |
| supervisor | super123 | supervisor | Ver todo, asignar, cerrar fallas |
| tecnico1 | tecnico123 | tecnico | Fallas asignadas, reparar |
| visualizador | viz123 | visualizador | Solo lectura |

## Tecnologías Utilizadas

- **Backend:** Flask 3.0, SQLAlchemy 3.1, Flask-Login 0.6
- **Frontend:** Jinja2, Bootstrap 5.3
- **Visualización:** Chart.js 4.4, Leaflet.js 1.9, Mermaid.js 10
- **Base de Datos:** PostgreSQL (producción), SQLite (desarrollo)
- **Procesamiento Datos:** pandas 2.1, openpyxl 3.1
- **Servidor:** gunicorn 21.2
- **Deployment:** Railway

## Características Destacadas

✅ Sistema completo de gestión de equipos
✅ Workflow de fallas con 6 estados
✅ **Validación anti-duplicados en 4 niveles**
✅ **Vista especial de mantención de gabinetes**
✅ Mapas de topología y geolocalización
✅ Reportes avanzados con exportación
✅ Responsive design
✅ Autenticación con 4 roles
✅ Script de migración de 13 Excel
✅ Documentación completa

## Próximos Pasos

1. Desplegar en Railway
2. Ejecutar migración de datos
3. Pruebas funcionales con usuario
4. Cambiar contraseñas por defecto
5. Configurar backups periódicos

## Notas Importantes

⚠️ **VALIDACIÓN ANTI-DUPLICADOS:** Esta es la funcionalidad más crítica del sistema. Está implementada en backend, API, frontend y script de migración.

⚠️ **VISTA MANTENCIÓN GABINETES:** Permite ver de forma organizada todos los equipos contenidos en cada gabinete para facilitar tareas de mantención y reparación.

⚠️ **SOLUCIÓN OBLIGATORIA:** Al marcar una falla como "Reparada", el campo solución_aplicada es OBLIGATORIO.

## Repositorio GitHub

https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro

## Contacto

Sistema desarrollado para la Universidad de La Frontera (UFRO) - 2025
