# Sistema de Gestión de Cámaras UFRO

Sistema fullstack para gestión de cámaras de seguridad, fallas, mantenimientos y visualización de red.

## Tecnologías

- **Backend:** Flask + SQLAlchemy + PostgreSQL/SQLite
- **Frontend:** React + TypeScript + Tailwind CSS + Vite
- **Deployment:** Railway (PostgreSQL automático)

## Estructura del Proyecto

```
sistema-camaras/
├── app.py                 # Aplicación Flask con API REST
├── models.py              # Modelos SQLAlchemy
├── migrate_data.py        # Script de migración de datos Excel
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración Railway
├── railway.json          # Configuración Railway
├── planillas/            # Archivos Excel con datos
├── src/                  # Frontend React
│   ├── App.tsx
│   ├── main.tsx
│   └── components/
│       ├── Dashboard.tsx
│       ├── CamerasModule.tsx
│       ├── GabinetesModule.tsx
│       ├── SwitchesModule.tsx
│       ├── FallasModule.tsx
│       └── MantenimientosModule.tsx
├── dist/                 # Build del frontend (generado)
└── package.json          # Dependencias Node.js
```

## Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro
cd sistema-camaras-ufro
```

### 2. Configurar entorno Python

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Migrar datos desde Excel

```bash
python migrate_data.py
```

Esto creará `sistema_camaras.db` (SQLite) y poblará todas las tablas.

### 4. Construir frontend

```bash
pnpm install
pnpm run build
```

### 5. Ejecutar aplicación

```bash
# Desarrollo
python app.py

# Producción local
gunicorn app:app
```

Abrir http://localhost:5000

## Deployment en Railway

### Opción 1: Desde GitHub (Recomendado)

1. Push del código a GitHub
2. En Railway: New Project > Deploy from GitHub
3. Seleccionar el repositorio
4. Railway detectará automáticamente:
   - `Procfile` → `web: gunicorn app:app`
   - `requirements.txt` → Instalará dependencias
   - Creará PostgreSQL automáticamente
5. Agregar variable de entorno:
   ```
   SECRET_KEY=tu_clave_secreta_aquí
   ```
6. El deployment se ejecutará automáticamente

### Opción 2: Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Agregar PostgreSQL
railway add
# Seleccionar: PostgreSQL

# Deploy
railway up
```

### Variables de Entorno en Railway

Railway configura automáticamente:
- `DATABASE_URL` → PostgreSQL connection string
- `PORT` → Puerto asignado

Agregar manualmente:
- `SECRET_KEY` → Generar con: `python -c "import secrets; print(secrets.token_hex(32))"`

## Migración de Datos en Producción

Después del primer deployment:

```bash
# Conectarse al proyecto Railway
railway link

# Ejecutar migración
railway run python migrate_data.py
```

O usar la interfaz de Railway:
1. Ir a la pestaña "Settings"
2. En "Deploy Triggers" agregar comando: `python migrate_data.py && gunicorn app:app`

## API Endpoints

### Autenticación
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/logout` - Logout
- `GET /api/auth/user` - Usuario actual

### Cámaras
- `GET /api/camaras` - Listar todas
- `GET /api/camaras/<id>` - Obtener una

### Gabinetes
- `GET /api/gabinetes` - Listar todos

### Switches
- `GET /api/switches` - Listar todos
- `GET /api/puertos_switch` - Listar puertos

### Fallas
- `GET /api/fallas` - Listar todas
- `POST /api/fallas` - Crear nueva

### Mantenimientos
- `GET /api/mantenimientos` - Listar todos

### Estadísticas
- `GET /api/estadisticas` - Dashboard stats
- `GET /api/mapa_red` - Datos para visualización

## Usuarios por Defecto

| Username | Password | Rol |
|----------|----------|-----|
| admin | admin123 | administrador |
| tecnico1 | tecnico123 | tecnico |
| supervisor | super123 | supervisor |

## Datos Migrados

El script `migrate_data.py` lee los siguientes archivos Excel de la carpeta `planillas/`:

- Listadecámaras_modificada.xlsx
- Gabinetes.xlsx
- Switches.xlsx
- Puertos_Switch.xlsx
- Equipos_Tecnicos.xlsx
- Fallas_Actualizada.xlsx
- Ejemplos_Fallas_Reales.xlsx (4 casos reales)
- Mantenimientos.xlsx
- Ubicaciones.xlsx
- Catalogo_Tipos_Fallas.xlsx

## Desarrollo

### Backend (Flask)

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Frontend (React)

```bash
pnpm run dev
```

Esto iniciará Vite en http://localhost:5173 con hot reload.

Para desarrollo fullstack:
1. Backend en puerto 5000
2. Frontend en puerto 5173
3. Configurar proxy en `vite.config.ts` para API calls

## Troubleshooting

### Error: "No module named 'models'"
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python app.py
```

### Error: "Database not found"
```bash
python migrate_data.py
```

### Error en Railway: "Application failed to respond"
- Verificar que `Procfile` existe: `web: gunicorn app:app`
- Verificar que `gunicorn` está en `requirements.txt`
- Revisar logs en Railway dashboard

### PostgreSQL connection issues
- Railway provee `DATABASE_URL` automáticamente
- El código detecta PostgreSQL y convierte `postgres://` a `postgresql://`

## Licencia

Universidad de la Frontera - 2025
