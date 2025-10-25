# 🚀 Instrucciones para Migración en Railway

## ✅ Estado Actual
- **Código desplegado:** ✅ Actualizado en GitHub
- **Aplicación funcionando:** ✅ https://gestion-camaras-ufro.up.railway.app/
- **Migration script:** ✅ Creado y listo

## 📋 Pasos para Ejecutar la Migración

### Opción A: Desde Railway Dashboard (RECOMENDADO)

1. **Acceder a Railway:**
   - Ir a: https://railway.app
   - Iniciar sesión en tu cuenta

2. **Abrir PostgreSQL:**
   - Seleccionar tu proyecto "sistema-camaras-ufro"
   - Click en "PostgreSQL" en la lista de servicios

3. **Ejecutar Migración:**
   - Click en "Data" → "Query"
   - Abrir archivo: `migration_prioridades_criticas.sql`
   - Copiar todo el contenido
   - Pegar en la consulta de Railway
   - Click "Run Query"

### Opción B: Desde Railway CLI (Si tienes CLI instalada)

```bash
# Conectar a PostgreSQL
railway connect postgres

# Ejecutar el script de migración
\i migration_prioridades_criticas.sql
```

### Opción C: Script Python en Railway

```bash
# Configurar variables de entorno en Railway
# Variables → DATABASE_URL (ya configurada)

# Ejecutar script Python
python migrar_railway.py
```

## 📊 Verificación Post-Migración

Después de ejecutar la migración, verificar que las siguientes funcionalidades estén disponibles:

### ✅ Nuevas URLs:
- **VLANs:** https://gestion-camaras-ufro.up.railway.app/vlans
- **Enlaces:** https://gestion-camaras-ufro.up.railway.app/enlaces
- **Dashboard Conectividad:** https://gestion-camaras-ufro.up.railway.app/dashboard/conectividad

### ✅ Funcionalidades Integradas:
- **Formularios de Cámaras:** Campos de firmware
- **Dashboard UPS:** Información de autonomía
- **Navegación:** Enlaces a nuevas secciones en el menú

## 🔍 Script de Verificación SQL

```sql
-- Verificar tablas creadas
SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'vlan';
SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'enlace';

-- Verificar columnas en cámaras
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'camaras' AND column_name LIKE '%firmware%';

-- Verificar columnas en UPS
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'ups' AND column_name LIKE '%autonomia%';
```

## 🎯 Resultados Esperados

Después de la migración exitosa:
- ✅ **4 Prioridades Críticas** implementadas
- ✅ **84 rutas funcionales** disponibles
- ✅ **49 templates HTML** operativos
- ✅ **16 modelos** en la base de datos

## 🆘 Solución de Problemas

### Si aparece error de permisos:
```sql
-- Verificar permisos del usuario
\du
```

### Si las tablas no se crean:
- Verificar que el script SQL se ejecutó completamente
- Revisar logs de Railway para errores
- Ejecutar individualmente cada statement

### Si faltan columnas:
```sql
-- Agregar columnas manualmente si es necesario
ALTER TABLE camaras ADD COLUMN IF NOT EXISTS version_firmware VARCHAR(50);
ALTER TABLE camaras ADD COLUMN IF NOT EXISTS fecha_actualizacion_firmware DATE;
ALTER TABLE camaras ADD COLUMN IF NOT EXISTS proxima_revision_firmware DATE;
```

## 📞 Contacto
- **URL del Sistema:** https://gestion-camaras-ufro.up.railway.app/
- **Repositorio:** https://github.com/ultimocorreoexistente-prog/sistema-camaras-ufro
- **Código fuente:** `/workspace/sistema-camaras-flask/`
