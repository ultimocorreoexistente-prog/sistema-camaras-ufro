#!/usr/bin/env python3
"""
Script de preparación para deployment
Prepara todos los archivos necesarios para subir el proyecto a la web
"""

import os
import shutil
import json
from datetime import datetime

def crear_directorio_deployment():
    """Crea directorio con todos los archivos necesarios para deployment"""
    
    # Crear directorio de deployment
    deploy_dir = f"deployment_sistema_camaras_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(deploy_dir, exist_ok=True)
    
    print(f"📁 Creando directorio de deployment: {deploy_dir}")
    
    # Archivos principales que deben incluirse
    archivos_principales = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'railway.json',
        'gestor_fallas_mantenimientos.py',
        'gestor_fallas_mejorado.py',
        'actualizar_db_campus.py'
    ]
    
    # Copiar archivos principales
    for archivo in archivos_principales:
        if os.path.exists(archivo):
            shutil.copy2(archivo, deploy_dir)
            print(f"✅ Copiado: {archivo}")
        else:
            print(f"⚠️  No encontrado: {archivo}")
    
    # Copiar directorio templates
    if os.path.exists('templates'):
        shutil.copytree('templates', f"{deploy_dir}/templates", dirs_exist_ok=True)
        print(f"✅ Copiado: templates/")
    
    # Crear archivo README para deployment
    readme_content = f"""# Sistema de Gestión de Cámaras UFRO

## Deployment Ready Package
Fecha de preparación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Archivos incluidos:
- ✅ app.py (Aplicación principal)
- ✅ requirements.txt (Dependencias)
- ✅ Procfile (Configuración Heroku/Railway)
- ✅ railway.json (Configuración Railway)
- ✅ templates/ (Plantillas HTML)
- ✅ Gestores de fallas
- ✅ Script de inicialización DB

## Instrucciones de deployment:

### 1. Subir a GitHub:
1. Crear repositorio en GitHub
2. Subir todos estos archivos
3. Commit: "Deployment inicial del sistema"

### 2. Railway (Recomendado):
1. Conectar GitHub a Railway
2. Crear PostgreSQL database
3. Configurar variables de entorno
4. Deploy automático

### 3. Variables de entorno necesarias:
```
DATABASE_URL=postgresql://...
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta
```

## URLs importantes después del deployment:
- Login: /login
- Dashboard: /dashboard  
- Informes: /informes
- Informes Avanzados: /informes-avanzados

## Credenciales por defecto:
- Usuario: admin
- Contraseña: admin123

⚠️ IMPORTANTE: Cambiar credenciales en producción
"""
    
    with open(f"{deploy_dir}/README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Crear archivo de configuración de entorno de ejemplo
    env_example = """# Archivo de ejemplo de variables de entorno
# Copiar como .env y completar con valores reales

DATABASE_URL=postgresql://usuario:password@host:puerto/database
FLASK_ENV=production
SECRET_KEY=genera_una_clave_secreta_segura_de_32_caracteres
ADMIN_USERNAME=admin
ADMIN_PASSWORD=cambia_esta_contraseña
"""
    
    with open(f"{deploy_dir}/.env.example", 'w', encoding='utf-8') as f:
        f.write(env_example)
    
    # Crear archivo .gitignore
    gitignore_content = """# Base de datos local
*.db
*.sqlite3

# Variables de entorno
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# Sistema
.DS_Store
Thumbs.db

# Archivos temporales
temp/
tmp/
uploads/
exports/
"""
    
    with open(f"{deploy_dir}/.gitignore", 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    # Crear script de verificación pre-deployment
    verificacion_script = '''#!/usr/bin/env python3
"""
Script de verificación pre-deployment
Verifica que todos los archivos necesarios estén presentes
"""

import os
import sys

def verificar_archivos():
    """Verifica que todos los archivos necesarios estén presentes"""
    archivos_requeridos = [
        'app.py',
        'requirements.txt', 
        'Procfile',
        'railway.json',
        'templates/dashboard.html',
        'templates/informes_avanzados.html',
        'templates/login.html',
        'templates/operaciones.html'
    ]
    
    print("🔍 Verificando archivos para deployment...")
    
    todos_presentes = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ FALTANTE: {archivo}")
            todos_presentes = False
    
    if todos_presentes:
        print("\\n🎉 ¡Todos los archivos están presentes!")
        print("✅ Listo para deployment")
    else:
        print("\\n⚠️ Faltan archivos necesarios")
        print("❌ NO listo para deployment")
        sys.exit(1)

def verificar_sintaxis():
    """Verifica sintaxis básica de app.py"""
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            compile(content, 'app.py', 'exec')
        print("✅ Sintaxis de app.py correcta")
    except Exception as e:
        print(f"❌ Error en app.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verificar_archivos()
    verificar_sintaxis()
    print("\\n🚀 ¡Proyecto listo para deployment!")
'''
    
    with open(f"{deploy_dir}/verificar_deployment.py", 'w', encoding='utf-8') as f:
        f.write(verificacion_script)
    
    # Crear archivo de comandos rápidos
    comandos_rapidos = """# COMANDOS RÁPIDOS PARA DEPLOYMENT

## Verificar antes de deployment:
python verificar_deployment.py

## Git commands (después de subir a GitHub):
git add .
git commit -m "Deploy inicial del sistema de cámaras UFRO"
git push origin main

## Railway CLI (opcional):
railway login
railway link [PROJECT_ID]
railway up

## Heroku CLI (si usas Heroku):
heroku login
heroku create sistema-camaras-ufro
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main

## Verificar deployment:
curl https://tu-app-url.railway.app/
curl https://tu-app-url.railway.app/login

## Variables de entorno ejemplo:
DATABASE_URL=postgresql://...
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta_super_segura
"""
    
    with open(f"{deploy_dir}/COMANDOS_RAPIDOS.md", 'w', encoding='utf-8') as f:
        f.write(comandos_rapidos)
    
    print(f"\n🎉 ¡Directorio de deployment creado exitosamente!")
    print(f"📁 Ubicación: {deploy_dir}/")
    print(f"📝 Total de archivos: {len(os.listdir(deploy_dir))}")
    
    print(f"\n📋 Próximos pasos:")
    print(f"1. cd {deploy_dir}")
    print(f"2. python verificar_deployment.py")
    print(f"3. Subir todo el contenido a GitHub")
    print(f"4. Seguir la guía de deployment para tu plataforma elegida")
    
    return deploy_dir

def mostrar_checklist():
    """Muestra checklist de deployment"""
    checklist = """
🔥 CHECKLIST DE DEPLOYMENT

📋 PREPARACIÓN:
□ Cuenta GitHub creada
□ Directorio de deployment preparado
□ Archivos verificados con verificar_deployment.py
□ .gitignore configurado

📋 PLATAFORMA (elegir una):
□ Cuenta Railway creada (recomendado)
□ O cuenta Render creada
□ O cuenta Heroku creada

📋 REPOSITORIO:
□ Repositorio GitHub creado
□ Archivos subidos a GitHub
□ README.md incluido

📋 BASE DE DATOS:
□ PostgreSQL database creada en plataforma
□ DATABASE_URL obtenida
□ Variables de entorno configuradas

📋 DEPLOYMENT:
□ Aplicación desplegada
□ URL pública obtenida
□ Login funcionando
□ Dashboard cargando
□ Informes básicos funcionando
□ Informes avanzados funcionando

📋 SEGURIDAD:
□ Credenciales por defecto cambiadas
□ SECRET_KEY configurada
□ HTTPS habilitado (automático)

📋 VERIFICACIÓN FINAL:
□ Todas las URLs funcionando
□ Base de datos poblada
□ Archivos Excel descargándose
□ Mapas de red generándose
"""
    print(checklist)

if __name__ == "__main__":
    print("🚀 PREPARADOR DE DEPLOYMENT - SISTEMA CÁMARAS UFRO")
    print("=" * 60)
    
    # Crear directorio de deployment
    deploy_dir = crear_directorio_deployment()
    
    # Mostrar checklist
    mostrar_checklist()
    
    print("\n" + "=" * 60)
    print("✅ ¡Preparación completada!")
    print(f"📁 Tu directorio de deployment: {deploy_dir}/")
    print("📖 Sigue la GUIA_COMPLETA_DEPLOYMENT.md para continuar")