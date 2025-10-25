# INSTRUCCIONES DE DEPLOYMENT - 4 Prioridades CRÍTICAS

**Fecha:** 2025-10-25
**Sistema:** Gestión de Cámaras UFRO

## ✅ CAMBIOS IMPLEMENTADOS

### 1. Modelo Enlaces (PRIORIDAD 1)
- Gestión completa de conectividad
- Campos: tipo_enlace, latencia_ms, porcentaje_perdida_paquetes, estado_conexion, ancho_banda_mbps
- CRUD completo + Dashboard de métricas

### 2. Firmware en Cámaras (PRIORIDAD 2)
- Campos: version_firmware, fecha_actualizacion_firmware, proxima_revision_firmware
- Integrado en formularios de cámaras

### 3. VLAN en Switches (PRIORIDAD 3)
- Modelo VLAN completo
- Campos: vlan_id, vlan_nombre, red, mascara, gateway
- Relación con Switch y Puerto_Switch

### 4. Autonomía UPS (PRIORIDAD 4)
- Campos: autonomia_minutos, porcentaje_carga_actual, alertas_bateria_baja, alertas_sobrecarga
- Dashboard de monitoreo energético

## 📋 PASOS PARA DEPLOYMENT EN RAILWAY

### PASO 1: Verificar que el código está en GitHub ✅
```bash
cd sistema-camaras-flask
git status  # Debe mostrar "nothing to commit, working tree clean"
```

### PASO 2: Railway detectará automáticamente el push
- Railway ejecutará build automático
- El nuevo código se desplegará automáticamente
- Tiempo estimado: 2-3 minutos

### PASO 3: Ejecutar migración SQL en Railway

**Opción A: Desde Railway CLI (recomendado)**
```bash
# Conectarse a PostgreSQL
railway connect postgres

# Ejecutar el script de migración
\i migration_prioridades_criticas.sql
```

**Opción B: Desde Python (script incluido)**
```bash
# Configurar DATABASE_URL en Railway
# Variables → DATABASE_URL (ya debe estar configurada)

# Ejecutar script de migración
python ejecutar_migracion_prioridades.py
```

**Opción C: Desde Railway Dashboard**
1. Ir a: https://railway.app → tu proyecto → PostgreSQL
2. Click en "Data" → "Query"
3. Copiar y pegar el contenido de `migration_prioridades_criticas.sql`
4. Ejecutar

### PASO 4: Verificar que la migración fue exitosa

**Verificar tablas creadas:**
```sql
-- Verificar tabla enlace
SELECT COUNT(*) FROM enlace;

-- Verificar tabla vlan
SELECT COUNT(*) FROM vlan;

-- Verificar columnas nuevas en camaras
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'camaras' AND column_name LIKE '%firmware%';

-- Verificar columnas nuevas en ups
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'ups' AND column_name LIKE '%autonomia%' OR column_name LIKE '%alertas%';
```

### PASO 5: Verificar funcionalidad en la aplicación web

1. Ir a: https://gestion-camaras-ufro.up.railway.app/
2. Login con credenciales de superadmin
3. Verificar nuevas opciones en navegación:
   - **Inventario** → Enlaces
   - **Inventario** → VLANs
   - **Mapas** → Dashboard Conectividad

4. Probar CRUD de Enlaces:
   - Ir a `/enlaces`
   - Crear nuevo enlace
   - Verificar formulario completo

5. Probar CRUD de VLANs:
   - Ir a `/vlans`
   - Crear nueva VLAN
   - Verificar formulario completo

6. Verificar Dashboard de Conectividad:
   - Ir a `/dashboard-conectividad`
   - Verificar métricas de latencia y pérdida de paquetes

7. Verificar formularios actualizados:
   - **Cámaras**: Verificar campos de firmware en formulario
   - **UPS**: Verificar campos de autonomía en formulario

## 🔍 VALIDACIÓN FINAL

### Checklist de Funcionalidades:
- [ ] Modelo Enlaces implementado con CRUD completo
- [ ] Modelo VLAN implementado con CRUD completo
- [ ] Campos firmware en Cámaras funcionando
- [ ] Campos autonomía en UPS funcionando
- [ ] Dashboard de Conectividad mostrando métricas
- [ ] Navegación actualizada con nuevos enlaces
- [ ] Sin errores en logs de Railway
- [ ] Todas las rutas accesibles

### Success Criteria (del requerimiento original):
- [x] Modelo Enlaces implementado con CRUD completo
- [x] Campos firmware agregados a Cámara con formularios
- [x] Modelo VLAN implementado y relacionado con Switch
- [x] Campos autonomía/alertas agregados a UPS con dashboard
- [x] Todas las interfaces actualizadas y funcionales
- [ ] Sistema deployado y funcional en Railway (pendiente verificación post-deployment)
- [x] Validaciones e integridad de datos aseguradas

## 📊 ESTADÍSTICAS DEL SISTEMA ACTUALIZADO

**Rutas totales:** 84 (62 → 84 rutas)
**Modelos:** 16 (14 → 16: +Enlace, +VLAN)
**Templates:** 49 (39 → 49)
**Líneas de código:**
- app.py: 2042 líneas (1843 → 2042: +199)
- models.py: 328 líneas (274 → 328: +54)

## 🚨 NOTAS IMPORTANTES

1. **Compatibilidad con datos existentes:** 
   - La migración usa `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`
   - No afectará datos existentes
   - Los campos nuevos aceptan NULL por defecto

2. **No se implementaron alertas automáticas:**
   - Según requerimiento, usuario NO necesita alertas automáticas
   - Sistema enfocado en funcionalidad manual y reportes

3. **Próximos pasos sugeridos:**
   - Poblar tablas Enlaces con datos reales
   - Configurar VLANs según topología de red actual
   - Actualizar firmware de cámaras existentes
   - Configurar autonomía de UPS existentes

## 📞 SOPORTE

Si hay problemas durante el deployment:
1. Verificar logs de Railway: `railway logs`
2. Verificar estado de PostgreSQL en Railway Dashboard
3. Revisar que DATABASE_URL está configurada correctamente
4. Verificar que todas las dependencias están en requirements.txt

---

**Última actualización:** 2025-10-25 09:45
**Estado:** ✅ Listo para deployment
