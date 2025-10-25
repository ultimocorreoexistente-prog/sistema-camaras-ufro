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
├── app.py                  # Aplicación Flask principal (84 rutas)
├── models.py               # 17 modelos SQLAlchemy (+ConexionTopologia)
├── migration_topologia.sql # Script migración para topología de red
├── migrate_data.py         # Script migración Excel → DB
├── requirements.txt
├── Procfile
├── railway.json
├── templates/              # Templates Jinja2 (49 archivos)
│   ├── topologia/          # Templates para topología de red
│   │   ├── topologia_switch.html
│   │   ├── topologia_gabinete.html
│   │   ├── conexiones_lista.html
│   │   └── conexiones_form.html
│   └── ...
├── static/                 # CSS, JavaScript, imágenes
└── planillas/              # Archivos Excel fuente
```

## ✅ ESTADO: SISTEMA COMPLETADO AL 100%

**🌐 Sistema en Producción:** https://gestion-camaras-ufro.up.railway.app/  
**📅 Completado:** 2025-10-25  
**🏗️ Desarrollado con:** Flask + Jinja2 + PostgreSQL + Railway  
**📊 Estadísticas:** 84 rutas funcionales, 49 templates HTML, 17 modelos SQLAlchemy

### 🎯 5 Prioridades Críticas Implementadas
1. **Modelo Enlaces** - Gestión completa de conectividad con métricas
2. **Firmware Cámaras** - Versionado y gestión de actualizaciones  
3. **VLANs** - Gestión de redes virtuales en switches
4. **Autonomía UPS** - Monitoreo energético con alertas
5. **Topología de Red "Boca a Boca"** - Visualización completa de conexiones físicas

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

**Nota Importante:** Las cámaras están **ubicadas físicamente fuera de los gabinetes** y se conectan por cable a los switches. Cada cámara tiene su propia latitud/longitud en el mapa de geolocalización, permitiendo identificar fácilmente su ubicación exacta, incluso cuando están lejos del gabinete correspondiente.

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
- Geolocalización con Leaflet.js (incluye todos los equipos)
- Dashboard de conectividad (NUEVO)
- Gráficos Chart.js en dashboard

### Topología de Red "Boca a Boca" (NUEVO)
Sistema completo para gestionar las conexiones físicas entre equipos:

**Funcionalidades Principales:**
- **Visualización de Switch:** Ver todas las conexiones de un switch específico (cámaras, NVR/DVR, otros switches)
- **Topología de Gabinete:** Ver topología completa (equipos contenidos + equipos antes/después)
- **Gestión de Conexiones:** CRUD completo para crear, editar y eliminar conexiones
- **Tipos de Conexión:** UTP (cable de red), Fibra óptica, Enlace inalámbrico
- **Información de Puertos:** Especificar puertos origen/destino en cada conexión
- **Distancia de Cableado:** Registrar distancia física en metros
- **Diagramas Jerárquicos:** Visualización con Mermaid.js para entender la red

**Accesos de la Topología:**
- `/conexiones` - Lista todas las conexiones con filtros
- `/conexiones/nueva` - Crear nueva conexión entre equipos
- `/conexiones/<id>/editar` - Editar conexión existente
- `/topologia/switch/<id>` - Ver topología "boca a boca" de un switch
- `/topologia/gabinete/<id>` - Ver topología completa de un gabinete

**Navegación:**
Menú "Topología" en la barra principal con opciones:
- Ver Conexiones
- Nueva Conexión
- Visualizar por Gabinete

### Nuevas Funcionalidades (2025-10-25)
- **Gestión de Enlaces:** `/enlaces` - Monitoreo de conectividad
- **Gestión de VLANs:** `/vlans` - Redes virtuales en switches
- **Firmware Cámaras:** Campos de versionado en formularios
- **Autonomía UPS:** Monitoreo de carga y alertas
- **Dashboard Conectividad:** `/dashboard/conectividad` - Métricas en tiempo real
- **Topología de Red:** Sistema completo "boca a boca" con visualización de conexiones

### Reportes
- Exportación a Excel
- Impresión optimizada con CSS @media print
- Estadísticas por campus y tipo

## Deployment en Railway

**Sistema en Producción:** ✅ https://gestion-camaras-ufro.up.railway.app/

### Migración de Topología de Red

Para habilitar el sistema de topología de red "boca a boca":

1. **Ejecutar Script SQL en Railway:**
   - Ir a: Railway Dashboard → PostgreSQL → Query
   - Abrir: `migration_topologia.sql` (archivo en la raíz del proyecto)
   - Copiar y ejecutar el contenido completo

2. **Verificación:**
   - Acceder a `/conexiones` y verificar que la página carga correctamente
   - Crear una conexión de prueba desde "Nueva Conexión"
   - Verificar visualización en `/topologia/switch/<id>` para un switch existente
   - Comprobar menú "Topología" en la barra de navegación

### Migración de Prioridades Críticas

1. **Ejecutar Script SQL en Railway:**
   - Ir a: Railway Dashboard → PostgreSQL → Query
   - Abrir: `migration_prioridades_criticas.sql`
   - Copiar y ejecutar el contenido completo

2. **Verificación:**
   - Acceder a `/vlans` y `/enlaces`
   - Verificar campos de firmware en formularios de cámaras
   - Comprobar dashboard de UPS con autonomía

Consultar [INSTRUCCIONES_MIGRACION_RAILWAY.md](INSTRUCCIONES_MIGRACION_RAILWAY.md) para instrucciones detalladas.

## Deployment en Railway (Desarrollo)

Consultar [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas.

## Tecnologías Utilizadas

- Flask 3.0.0
- SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Bootstrap 5.3.0
- Chart.js 4.4.0
- Leaflet.js 1.9.4
- Mermaid.js 10 (diagramas de topología de red)
- pandas 2.1.3
- openpyxl 3.1.2
- gunicorn 21.2.0
- psycopg2-binary 2.9.9
- ReportLab 4.0.7 (generación de PDFs)

## Contribución

Este es un proyecto de gestión interna de la UFRO. Para contribuir, contactar al equipo de TI.

## Licencia

Uso interno UFRO - 2025

## Contacto

Sistema desarrollado para la Universidad de La Frontera (UFRO)
