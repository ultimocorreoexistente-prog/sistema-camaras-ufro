# Cómo Cambiar el Nombre del Dominio en Railway

## Situación Actual
URL actual: `https://web-production-d78b7.up.railway.app/`

## Objetivo
Cambiar a: `https://gestion-camaras-ufro.up.railway.app/`

## Pasos para Cambiar el Nombre (desde Dashboard de Railway)

### Opción 1: Desde la Web (MAS FÁCIL)

1. **Ingresar a Railway**: https://railway.app/
2. **Seleccionar el proyecto**: Buscar el proyecto "sistema-camaras-ufro" o similar
3. **Ir a Settings del Servicio**:
   - Click en el servicio web
   - Click en la pestaña "Settings"
4. **Cambiar el nombre del servicio**:
   - Buscar la sección "Service Name"
   - Cambiar de `web-production-d78b7` a `gestion-camaras-ufro`
   - Guardar cambios
5. **Resultado**: El dominio cambiará automáticamente a:
   - `https://gestion-camaras-ufro.up.railway.app/`

### Opción 2: Dominio Personalizado (OPCIONAL)

Si deseas un dominio completamente personalizado (sin `.railway.app`):

1. **Ir a Settings del Servicio**
2. **Buscar "Networking" o "Domains"**
3. **Click en "Generate Domain" o "Custom Domain"**
4. **Agregar tu dominio personalizado**:
   - Ejemplo: `gestion-camaras.ufro.cl`
   - Configurar DNS según instrucciones de Railway

## Notas Importantes

- El cambio de nombre del servicio NO afecta el funcionamiento de la aplicación
- NO requiere redeployment
- El cambio es instantáneo
- La URL antigua (`web-production-d78b7.up.railway.app`) dejará de funcionar

## ¿Necesitas Railway API Token?

Si prefieres que haga el cambio automáticamente mediante la API de Railway, necesitaré:
- **Railway API Token** (diferente al GitHub Token)
- Se obtiene desde: Railway Dashboard → Account Settings → Tokens → Create New Token

## Estado Actual de la Reparación
- ✅ Endpoints administrativos seguros agregados
- 🔄 Push a GitHub en progreso
- ⏳ Esperando redeployment automático de Railway
