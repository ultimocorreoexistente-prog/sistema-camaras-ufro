# Guía de Deployment en Railway

Esta guía explica cómo desplegar el Sistema de Gestión de Cámaras UFRO en Railway.

## Requisitos Previos

1. Cuenta en Railway (https://railway.app)
2. Repositorio GitHub con el código
3. Archivos Excel de datos en la carpeta `planillas/`

## Paso 1: Preparar el Proyecto

Asegúrate de que tu proyecto tiene estos archivos:

- `requirements.txt`
- `Procfile`
- `railway.json`
- `app.py`
- `models.py`
- `migrate_data.py`

## Paso 2: Crear Proyecto en Railway

1. Ir a https://railway.app
2. Click en "New Project"
3. Seleccionar "Deploy from GitHub repo"
4. Autorizar Railway en GitHub
5. Seleccionar el repositorio del proyecto

## Paso 3: Agregar PostgreSQL

1. En el dashboard de Railway, click en "+ New"
2. Seleccionar "Database"
3. Elegir "PostgreSQL"
4. Railway creará automáticamente la base de datos

## Paso 4: Configurar Variables de Entorno

En el servicio de la aplicación Flask, agregar estas variables:

```
DATABASE_URL=postgresql://... (automáticamente creada por Railway)
SECRET_KEY=tu-clave-secreta-aleatoria-aqui
FLASK_ENV=production
```

Para generar una SECRET_KEY segura:
```python
import secrets
print(secrets.token_hex(32))
```

## Paso 5: Deploy Inicial

Railway desplegará automáticamente la aplicación cuando detecte cambios en el repositorio.

## Paso 6: Inicializar Base de Datos

Una vez desplegada la aplicación, conectarse vía Railway CLI:

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar shell en el contenedor
railway run bash

# Inicializar base de datos
flask init-db

# Migrar datos desde Excel
python migrate_data.py
```

## Paso 7: Verificar Deployment

1. Abrir la URL generada por Railway
2. Intentar login con usuario admin
3. Verificar que aparecen los datos migrados

## Comandos Útiles de Railway CLI

```bash
# Ver logs
railway logs

# Ver variables de entorno
railway variables

# Ejecutar comandos en el contenedor
railway run python migrate_data.py

# Conectar a PostgreSQL
railway connect postgres
```

## Troubleshooting

### Error: "No module named 'xxx'"

Verificar que `requirements.txt` esté actualizado y completo.

### Error: "Database connection failed"

1. Verificar que la variable `DATABASE_URL` esté configurada
2. Verificar que PostgreSQL esté corriendo
3. Revisar logs: `railway logs`

### Error: "Application failed to start"

1. Revisar `Procfile` (debe ser: `web: gunicorn app:app`)
2. Verificar que `app.py` tenga `if __name__ == '__main__':`
3. Revisar logs detallados

### Fallas no se insertan

Verificar que la validación anti-duplicados esté funcionando correctamente:
- Endpoint `/api/fallas/validar` debe responder
- JavaScript `fallas_validation.js` debe estar cargado

## Actualización del Sistema

Para actualizar el sistema desplegado:

1. Hacer commit y push de cambios a GitHub
2. Railway desplegará automáticamente
3. Si hay cambios en la BD, ejecutar migraciones manualmente

## Backup de Base de Datos

```bash
# Exportar base de datos
railway run pg_dump $DATABASE_URL > backup.sql

# Restaurar base de datos
railway run psql $DATABASE_URL < backup.sql
```

## Monitoreo

Railway proporciona:
- Métricas de uso (CPU, RAM, red)
- Logs en tiempo real
- Alertas de errores

## Costos Estimados

- Plan Starter de Railway: $5/mes (incluye PostgreSQL)
- Plan Developer: $20/mes (más recursos)

## Contacto y Soporte

Para problemas con el deployment:
1. Revisar logs: `railway logs`
2. Consultar documentación: https://docs.railway.app
3. Contactar equipo de TI UFRO

## Checklist de Deployment

- [ ] Proyecto creado en Railway
- [ ] PostgreSQL agregado
- [ ] Variables de entorno configuradas
- [ ] Aplicación desplegada correctamente
- [ ] Base de datos inicializada (`flask init-db`)
- [ ] Datos migrados (`python migrate_data.py`)
- [ ] Login funciona con usuarios por defecto
- [ ] Cámaras aparecen en el listado
- [ ] Validación anti-duplicados funciona
- [ ] Mapas se visualizan correctamente

## Seguridad en Producción

1. Cambiar contraseñas de usuarios por defecto
2. Usar SECRET_KEY fuerte y única
3. Habilitar HTTPS (Railway lo hace automáticamente)
4. Configurar backups periódicos
5. Limitar acceso a la aplicación por IP si es necesario

## Escalabilidad

Para manejar más carga:
1. Aumentar recursos en Railway (plan Developer o Pro)
2. Optimizar consultas SQL con índices
3. Implementar caché con Redis si es necesario
4. Considerar CDN para assets estáticos
