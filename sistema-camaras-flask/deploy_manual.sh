#!/bin/bash
# Script de deployment manual para Railway
# Este script debe ejecutarse en el entorno local y luego subirse a Railway

echo "🚀 Iniciando deployment manual del Sistema Cámaras UFRO..."

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py en el directorio actual"
    exit 1
fi

echo "✅ Directorio verificado"

# Crear directorio temporal para deployment
mkdir -p deploy_temp
cp -r * deploy_temp/ 2>/dev/null || true

# Crear archivo de despliegue
cat > deploy_temp/DEPLOY_GUIDE.md << 'EOF'
# 🚀 GUÍA DE DEPLOYMENT - SISTEMA CÁMARAS UFRO

## 📋 PASOS PARA DEPLOYMENT EN RAILWAY

### 1. Preparación del Proyecto
```bash
# Comprimir todos los archivos
tar -czf sistema-camaras-ufro.tar.gz .
```

### 2. Upload a Railway
1. Ir a: https://railway.app/dashboard
2. Seleccionar proyecto: gestion-camaras-ufro
3. Ir a "Settings" > "Variables"
4. Verificar variables configuradas:
   - DATABASE_URL
   - SECRET_KEY
   - FLASK_ENV

### 3. Deploy desde Railway Dashboard
1. En Railway Dashboard, ir a "Deployments"
2. "New Deployment" > "From GitHub"
3. Conectar repositorio
4. Seleccionar rama master
5. Deploy

### 4. Configuración Post-Deployment
```bash
# Ejecutar inicialización (desde la aplicación web)
curl https://gestion-camaras-ufro.up.railway.app/init-usuarios-railway

# O acceder directamente:
# https://gestion-camaras-ufro.up.railway.app/init-usuarios-railway
```

### 5. Verificación Final
```yaml
URL: https://gestion-camaras-ufro.up.railway.app/
Usuario: charles.jelvez
Contraseña: charles123
Rol: SUPERADMIN
```

## 🎯 FUNCIONALIDADES IMPLEMENTADAS

### Sistema de Usuarios (NUEVO)
- ✅ 5 roles: SUPERADMIN, ADMIN, SUPERVISOR, TÉCNICO, VISUALIZADOR
- ✅ Gestión completa de usuarios
- ✅ Panel de administración
- ✅ Modo Demo/Real
- ✅ Tema claro/oscuro

### Sistema Base (EXISTENTE)
- ✅ Gestión de equipos (cámaras, switches, UPS, etc.)
- ✅ Sistema de fallas
- ✅ Mantenimientos
- ✅ Mapas de red
- ✅ Reportes

## 🔧 SCRIPTS DE UTILIDAD

### Crear Charles como SUPERADMIN
```bash
python3 crear_superadmin_charles.py
```

### Verificar usuarios en Railway
```bash
python3 verificacion_final_railway.py
```

### Inicializar todos los usuarios
```bash
python3 init_railway_usuarios.py
```

EOF

# Mostrar información del proyecto
echo "📊 INFORMACIÓN DEL PROYECTO:"
echo "================================"
echo "Directorio: $(pwd)"
echo "Archivos principales:"
ls -la | head -10

echo ""
echo "🎯 ARCHIVOS CLAVE PARA DEPLOYMENT:"
echo "=================================="
echo "✅ app.py - Aplicación Flask principal"
echo "✅ models.py - Modelos de base de datos" 
echo "✅ requirements.txt - Dependencias Python"
echo "✅ Procfile - Configuración Railway"
echo "✅ templates/ - Plantillas HTML"
echo "✅ static/ - Archivos CSS/JS"

echo ""
echo "📦 ARCHIVO CREADO: deploy_temp/"
echo "✅ Listo para subir a Railway"
echo ""
echo "🚀 Para completar el deployment:"
echo "1. Comprimir: tar -czf sistema-camaras-ufro.tar.gz deploy_temp/"
echo "2. Subir a Railway desde dashboard"
echo "3. Ejecutar: https://gestion-camaras-ufro.up.railway.app/init-usuarios-railway"