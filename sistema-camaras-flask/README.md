# Sistema de Gestión de Cámaras UFRO

Sistema web fullstack para gestión de 474 cámaras de seguridad distribuidas en 4 campus de la Universidad de La Frontera (UFRO).

## Características Principales

- Gestión completa de equipos (Cámaras, Gabinetes, Switches, UPS, NVR/DVR, Fuentes de Poder)
- Sistema de gestión de fallas con workflow de 6 estados
- Validación anti-duplicados de fallas
- Registro de mantenimientos preventivos y correctivos
- Visualización de topología de red con Mermaid.js
- Geolocalización de equipos con Leaflet.js
- Reportes avanzados con exportación Excel/PNG
- Sistema de autenticación con 4 roles de usuario
- Responsive design para móviles

## Stack Tecnológico

- **Backend:** Flask 3.0 + SQLAlchemy
- **Frontend:** Jinja2 Templates + Bootstrap 5
- **Base de Datos:** PostgreSQL (producción) / SQLite (desarrollo)
- **Visualización:** Mermaid.js, Leaflet.js, Chart.js
- **Deployment:** Railway + gunicorn

## Instalación Local

### Requisitos Previos

- Python 3.9+
- uv pip

### Pasos de Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro.git
cd sistema-camaras-flask
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
uv pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Inicializar base de datos:
```bash
flask init-db
```

6. Migrar datos desde Excel:
```bash
python migrate_data.py
```

7. Ejecutar servidor de desarrollo:
```bash
python app.py
```

El sistema estará disponible en `http://localhost:5000`

## Usuarios por Defecto

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Administrador |
| supervisor | super123 | Supervisor |
| tecnico1 | tecnico123 | Técnico |
| visualizador | viz123 | Visualizador |

## Estructura del Proyecto

```
sistema-camaras-flask/
├── app.py                  # Aplicación Flask principal
├── models.py               # 14 modelos SQLAlchemy
├── migrate_data.py         # Script migración Excel → DB
├── requirements.txt
├── Procfile
├── railway.json
├── templates/              # Templates Jinja2
├── static/                 # CSS, JavaScript, imágenes
└── planillas/              # Archivos Excel fuente
```

## Funcionalidades Principales

### Gestión de Equipos
- CRUD completo para 6 tipos de equipos
- Registro de altas y bajas con motivo
- Historial de cambios de estado
- Geolocalización con latitud/longitud

### Vista Especial de Mantención de Gabinetes
Muestra todos los equipos contenidos en cada gabinete:
- Switches (con puertos totales/usados)
- NVR/DVR (con canales)
- UPS (con capacidad VA)
- Fuentes de Poder
- Historial completo de mantenimientos y reparaciones

### Sistema de Fallas

**Workflow de 6 Estados:**
1. Pendiente
2. Asignada
3. En Proceso
4. Reparada
5. Cerrada
6. Cancelada

**Validación Anti-Duplicados (CRÍTICO):**
El sistema NO permite reportar una nueva falla si existe una falla previa con estado Pendiente, Asignada o En Proceso para el mismo equipo.

### Mapas y Visualización
- Topología de red con Mermaid.js
- Geolocalización con Leaflet.js
- Gráficos Chart.js en dashboard

### Reportes
- Exportación a Excel
- Impresión optimizada con CSS @media print
- Estadísticas por campus y tipo

## Deployment en Railway

Consultar [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas.

## Tecnologías Utilizadas

- Flask 3.0.0
- SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Bootstrap 5.3.0
- Chart.js 4.4.0
- Leaflet.js 1.9.4
- Mermaid.js 10
- pandas 2.1.3
- openpyxl 3.1.2
- gunicorn 21.2.0
- psycopg2-binary 2.9.9

## Contribución

Este es un proyecto de gestión interna de la UFRO. Para contribuir, contactar al equipo de TI.

## Licencia

Uso interno UFRO - 2025

## Contacto

Sistema desarrollado para la Universidad de La Frontera (UFRO)
