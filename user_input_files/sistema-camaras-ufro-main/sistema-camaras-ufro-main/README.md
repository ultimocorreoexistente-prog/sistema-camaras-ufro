# 🎯 Sistema de Gestión de Cámaras UFRO

## 📋 Descripción
Sistema completo de gestión de fallas y mantenimiento de cámaras de seguridad para la Universidad de la Frontera.

## ✨ Características Principales
- 🔐 **Autenticación** con roles y permisos
- 📊 **Dashboard interactivo** con estadísticas en tiempo real
- 🗺️ **Mapas de red** jerárquicos con visualización Mermaid
- 🏫 **Gestión por campus** con filtros avanzados
- 📱 **Responsive design** para dispositivos móviles
- 📈 **Reportes avanzados** con exportación Excel/PNG
- 🔧 **Gestión completa de fallas** y mantenimientos

## 🚀 Deployment Rápido (15 minutos)

### Opción 1: Railway (Recomendado - GRATIS)
1. Sube todos los archivos a GitHub
2. Ve a [railway.app](https://railway.app) → "New Project"
3. Conecta tu repositorio GitHub
4. Agrega PostgreSQL database
5. Configura `DATABASE_URL` en variables
6. ¡Listo! Tu app estará en línea

### Opción 2: Render.com (También gratis)
1. Sube a GitHub
2. [render.com](https://render.com) → "New Web Service"
3. Conecta GitHub → Start Command: `gunicorn app:app`
4. Agrega PostgreSQL database

## 📁 Estructura del Proyecto
```
sistema-camaras-ufro/
├── app.py                    # Aplicación principal Flask
├── requirements.txt          # Dependencias Python
├── Procfile                 # Configuración deployment
├── railway.json             # Config Railway
├── templates/               # Plantillas HTML
├── static/                  # CSS, JS, imágenes
├── sistema_camaras.db       # Base de datos SQLite
└── docs/                    # Documentación
```

## 🛠️ Instalación Local
```bash
git clone https://github.com/tu-usuario/sistema-camaras-ufro.git
cd sistema-camaras-ufro
pip install -r requirements.txt
python app.py
```

## 🔑 Credenciales por Defecto
- **Usuario:** admin
- **Contraseña:** admin123
- **⚠️ CAMBIAR** después del primer login

## 📊 Funcionalidades

### 🗺️ Mapas de Red
- Mapa completo de la infraestructura
- Mapas en cascada por ubicación
- Visualización jerárquica de componentes
- Filtros por campus

### 📈 Informes Avanzados
- Inventarios por campus (cámaras, gabinetes, switches)
- Análisis de fallas por tipo y frecuencia
- Reportes de mantenimiento preventivo
- Estadísticas de tiempo de resolución

### 🔧 Gestión de Fallas
- Registro manual y automático de incidentes
- Seguimiento de estado y resolución
- Asignación de técnicos
- Historial completo de intervenciones

## 📱 URLs Principales
- `/` - Dashboard principal
- `/login` - Autenticación
- `/informes-avanzados` - Reportes y mapas
- `/fallas` - Gestión de fallas
- `/mantenimientos` - Registro de mantenimientos

## 🏫 Campus Incluidos
- Andrés Bello (Principal)
- Pucón
- Angol  
- Medicina

## 🆕 Última Actualización
- **Fecha:** 2025-10-19
- **Cuarto caso real** documentado (17-10-2025)
- **Corrección horarios** de reparación
- **Mapas de red** implementados
- **Filtros por campus** habilitados

## 📞 Soporte
Para reportar problemas o solicitar funcionalidades, crear un issue en GitHub.

## 📄 Licencia
Desarrollado para Universidad de la Frontera - Uso interno

---
**⚡ Tiempo de deployment: 15 minutos**  
**💰 Costo: GRATIS con Railway/Render**  
**🌍 Acceso: 24/7 desde cualquier dispositivo**
