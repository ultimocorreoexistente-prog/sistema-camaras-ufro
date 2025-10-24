# GUÍA DE DEPLOYMENT - Sistema de Cámaras UFRO

## Resumen del Proyecto

Se ha desarrollado un sistema completo de gestión de cámaras de seguridad para la Universidad de la Frontera con las siguientes características:

### Componentes Principales

1. **Backend Flask** (`app.py`)
   - API REST completa con 20+ endpoints
   - Autenticación con sesiones
   - Soporte PostgreSQL (producción) y SQLite (desarrollo)
   - Endpoints para: cámaras, gabinetes, switches, fallas, mantenimientos

2. **Modelos de Datos** (`models.py`)
   - Usuario, Camara, Gabinete, Switch, PuertoSwitch
   - EquipoTecnico, Falla, Mantenimiento
   - Ubicacion, TipoFalla
   - Relaciones completas entre tablas

3. **Migración de Datos** (`migrate_data.py`)
   - Lee 10 archivos Excel de `planillas/`
   - Pobla todas las tablas con datos reales
   - Maneja integridad referencial

4. **Frontend React** (`src/`)
   - Dashboard con estadísticas en tiempo real
   - Módulos para cámaras, gabinetes, switches
   - Gestión de fallas y mantenimientos
   - Diseño responsive con Tailwind CSS

## PASOS PARA DEPLOYMENT

### 1. Preparar el Proyecto Localmente

```bash
cd /workspace/sistema-camaras

# Instalar dependencias Python
pip install -r requirements.txt

# Instalar dependencias Node.js
pnpm install

# Construir el frontend
pnpm run build
```

Esto generará la carpeta `dist/` con el frontend compilado que Flask servirá.

### 2. Probar Localmente

```bash
# Migrar datos (creará SQLite local)
python migrate_data.py

# Ejecutar servidor
gunicorn app:app

# Abrir http://localhost:8000
# Login: admin / admin123
```

### 3. Push a GitHub

```bash
git init
git add .
git commit -m "Sistema completo de gestión de cámaras UFRO"
git remote add origin https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro
git push -u origin main
```

### 4. Deployment en Railway

#### Opción A: Desde la Interfaz Web de Railway

1. Ir a https://railway.app/
2. Click en "New Project"
3. Seleccionar "Deploy from GitHub repo"
4. Autorizar acceso al repositorio
5. Seleccionar `sistema-camaras-ufro`
6. Railway detectará automáticamente Python y usará el `Procfile`
7. Agregar PostgreSQL:
   - Click en "+ New"
   - Seleccionar "Database" > "Add PostgreSQL"
   - Railway creará `DATABASE_URL` automáticamente
8. Configurar variables de entorno:
   - Click en tu servicio > "Variables"
   - Agregar: `SECRET_KEY` = (generar con `python -c "import secrets; print(secrets.token_hex(32))"`)
9. Click en "Deploy"

#### Opción B: Con Railway CLI

```bash
# Instalar CLI
npm i -g @railway/cli

# Login
railway login

# Link al proyecto existente o crear nuevo
railway link
# O: railway init

# Agregar PostgreSQL
railway add
# Seleccionar: PostgreSQL

# Deploy
railway up

# Ver logs
railway logs
```

### 5. Migrar Datos en Producción

Una vez deployed, ejecutar la migración:

```bash
railway run python migrate_data.py
```

O configurar en Railway:
- Settings > Deploy
- Build Command: `pnpm run build`
- Start Command: `python migrate_data.py && gunicorn app:app`

### 6. Verificar Deployment

1. Abrir la URL que Railway provee (ej: `sistema-camaras-production.up.railway.app`)
2. Verificar que carga la página de login
3. Login con: `admin` / `admin123`
4. Verificar dashboard con estadísticas
5. Navegar a Cámaras, Fallas, etc.

## Estructura de Archivos Clave

```
sistema-camaras/
├── app.py                    # Backend Flask [LISTO]
├── models.py                 # Modelos BD [LISTO]
├── migrate_data.py           # Migración [LISTO]
├── requirements.txt          # Python deps [LISTO]
├── Procfile                  # Railway config [LISTO]
├── railway.json              # Railway config [LISTO]
├── package.json              # Node deps [LISTO]
├── vite.config.ts            # Vite config [LISTO]
├── tailwind.config.js        # Tailwind [LISTO]
├── planillas/                # Datos Excel [COPIAR]
│   ├── Listadecámaras_modificada.xlsx
│   ├── Gabinetes.xlsx
│   ├── Switches.xlsx
│   ├── Puertos_Switch.xlsx
│   ├── ... (10 archivos total)
├── src/                      # Frontend React [LISTO]
│   ├── App.tsx
│   ├── main.tsx
│   └── components/
│       ├── Dashboard.tsx
│       ├── CamerasModule.tsx
│       ├── GabinetesModule.tsx
│       ├── SwitchesModule.tsx
│       ├── FallasModule.tsx
│       └── MantenimientosModule.tsx
└── dist/                     # Build [GENERAR]
```

## Troubleshooting

### Error: "No module 'models'"
```bash
export PYTHONPATH=$PYTHONPATH:.
python app.py
```

### Error: "Failed to build"
Verificar que `dist/` existe:
```bash
pnpm run build
ls -la dist/
```

### Error: "Database connection failed"
Railway debe crear `DATABASE_URL` automáticamente. Verificar en Variables.

### Logs en Railway
```bash
railway logs
# O en la interfaz web: Deployments > View Logs
```

## Credenciales de Acceso

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| tecnico1 | tecnico123 | Técnico |
| supervisor | super123 | Supervisor |

## Características Implementadas

- ✓ Sistema de autenticación con roles
- ✓ Dashboard con estadísticas en tiempo real
- ✓ Gestión completa de cámaras con filtros
- ✓ Gestión de gabinetes y switches
- ✓ Registro y seguimiento de fallas
- ✓ Gestión de mantenimientos
- ✓ Diseño responsive
- ✓ API REST completa
- ✓ Migración automática de datos Excel
- ✓ Soporte PostgreSQL y SQLite

## URLs Útiles

- Repositorio GitHub: https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro
- Railway Dashboard: https://railway.app/dashboard
- Documentación Flask: https://flask.palletsprojects.com/
- Documentación SQLAlchemy: https://docs.sqlalchemy.org/

## Contacto y Soporte

Para problemas o consultas sobre el sistema, revisar:
1. Logs de Railway
2. README.md del proyecto
3. Documentación de código (docstrings)

---

**Desarrollado para Universidad de la Frontera - 2025**
