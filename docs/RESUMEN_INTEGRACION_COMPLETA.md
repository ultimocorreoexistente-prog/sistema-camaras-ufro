# Integración Completa del Sistema de Cámaras UFRO

**Fecha:** 2025-10-20
**Estado:** ✅ COMPLETADO EXITOSAMENTE

---

## 🎯 Objetivo

Crear un script único que integre:
1. Lógica de `actualizar_db_campus.py` (soporte de campus e infraestructura de red)
2. Lógica de `integrador_casos_reales_v2.py` (inserción de casos reales)
3. Nuevo **Caso 4** proporcionado (Caída cámaras ZM - Falla Eléctrica)
4. Tipos de fallas estándar del sistema

---

## 💾 Archivos Generados

### 1. Script Principal
- **Archivo:** `code/integracion_completa_sistema_camaras.py`
- **Descripción:** Script unificado que ejecuta toda la integración
- **Funcionalidades:**
  - Creación automática de 8 tablas base
  - Inserción de tipos de fallas, casos reales, fallas específicas
  - Inserción de mantenimientos e infraestructura de red
  - Reporte final con estadísticas
  - Soporte para SQLite (desarrollo) y PostgreSQL (producción)

### 2. Base de Datos
- **Archivo:** `sistema_camaras.db`
- **Tipo:** SQLite 3.x
- **Tamaño:** ~20 KB
- **Estado:** Operativa con datos de prueba

---

## 📋 Estructura de Tablas Creadas

### Tablas Principales

1. **camaras**
   - Información de las cámaras del sistema
   - Campos: nombre, ubicación, edificio, piso, tipo, modelo, IP, estado, campus

2. **fallas**
   - Registro general de fallas
   - Campos: camara_id, tipo_falla, descripción, fecha_reporte, estado, prioridad, campus

3. **tipos_fallas**
   - Catálogo de tipos de fallas (10 tipos insertados)
   - Categorías: LIMPIEZA (2), REPARACION (2), AJUSTE (2), TECNICA (4)

4. **casos_reales**
   - Casos reales documentados (4 casos insertados)
   - Incluye componentes involucrados, dependencias, soluciones, lecciones aprendidas

5. **fallas_especificas**
   - Fallas detalladas con información técnica (2 fallas insertadas)
   - Campos: tipo, componente afectado, cámaras afectadas, tiempo downtime, costo

6. **mantenimientos_realizados**
   - Registro de mantenimientos (1 mantenimiento insertado)
   - Campos: tipo, componente, materiales, técnico, duración, costo

7. **infraestructura_red**
   - Topología de red del sistema (15 componentes insertados)
   - Tipos: Core_Switch, Switch, Gabinete, UPS, NVR
   - Campus: Andrés Bello (9), Pucón (2), Angol (2), Medicina (2)

8. **relaciones_componentes**
   - Relaciones jerárquicas entre componentes de red
   - Campos: componente_padre, componente_hijo, tipo_relacion

---

## 📚 Casos Reales Insertados

### Caso 1: Telas de araña - Bunker
- **Fecha:** 2024-10-12
- **Tipo:** Problemas de Limpieza
- **Tiempo resolución:** 1.0 hora
- **Cámara:** Bunker_EX_costado
- **Lección:** Programar limpieza preventiva trimestral para cámaras exteriores

### Caso 2: Mantenimiento UPS Edificio O
- **Fecha:** 2024-10-13
- **Tipo:** Mantenimiento Preventivo UPS
- **Tiempo resolución:** 2.5 horas
- **Equipo:** UPS APC Smart-UPS SC 1500VA
- **Acción:** Cambio de 1 batería RBC7
- **Cámaras afectadas:** 11 locales + 1 PTZ remota
- **Costo:** $45,000
- **Lección:** Importancia de baterías redundantes para mantenimiento sin corte total

### Caso 3: Falla Cable NVR CFT Prat
- **Fecha:** 2024-10-14
- **Tipo:** Falla de Conectividad (Cable suelto)
- **Tiempo resolución:** 26.5 horas
- **Cámaras afectadas:** 13 cámaras sin servicio
- **Causa:** Cable ethernet suelto entre NVR e internet
- **Costo:** $0 (solo reconexión)
- **Lección:** Necesidad de redundancia y revisión de instalaciones de subcontratistas

### Caso 4: Caída cámaras ZM - Falla Eléctrica ⭐ NUEVO
- **Fecha:** 2025-10-17
- **Tipo:** Falla de Alimentación Eléctrica
- **Tiempo resolución:** 2.67 horas (2h 40min)
- **Cámaras afectadas:** 
  - ZM-container_Ciclovia
  - ZM-Ciclovia a AM
  - ZM-Bodega_Ciclovia
- **Ubicación:** Zona ZM - Ciclovia, Campus Andrés Bello
- **Causa:** Automático desconectado en caseta guardia frente a taller
- **Solución:** Subir automático en caseta guardia
- **Responsable:** Marco Contreras (Encargado Seguridad)
- **Horario:**
  - Reporte: 15:45
  - Resolución: 18:25
- **Prioridad:** Alta
- **Impacto:** Medio
- **Observación:** Automático ubicado fuera de gabinetes principales
- **Lección:** Automáticos en lugares no convencionales requieren señalización y documentación clara. Considerar centralización de protecciones eléctricas.

---

## 🚨 Tipos de Fallas Configurados

### Categoría LIMPIEZA (2 tipos)
1. **Suciedad por telaraña**
   - Prioridad: MEDIA
   - Tiempo estimado: 30 min

2. **Manchas en lente**
   - Prioridad: MEDIA
   - Tiempo estimado: 30 min

### Categoría REPARACION (2 tipos)
1. **Mica rayada**
   - Prioridad: ALTA
   - Tiempo estimado: 120 min

2. **Protección dañada**
   - Prioridad: ALTA
   - Tiempo estimado: 180 min

### Categoría AJUSTE (2 tipos)
1. **Imagen borrosa**
   - Prioridad: MEDIA
   - Tiempo estimado: 45 min

2. **Cámara desalineada**
   - Prioridad: MEDIA
   - Tiempo estimado: 30 min

### Categoría TECNICA (4 tipos)
1. **Cámara sin imagen**
   - Prioridad: CRITICA
   - Tiempo estimado: 60 min

2. **Falla de conectividad**
   - Prioridad: ALTA
   - Tiempo estimado: 90 min

3. **Falla de alimentación**
   - Prioridad: CRITICA
   - Tiempo estimado: 120 min

4. **Falla de grabación**
   - Prioridad: ALTA
   - Tiempo estimado: 90 min

---

## 🌐 Infraestructura de Red por Campus

### Campus Andrés Bello (9 componentes)
- 1 Core Switch (CORE-SW-AB)
- 3 Switches (Edificio O, CFT Prat, Zona ZM)
- 3 Gabinetes (O-P3, CFT-01, ZM-01)
- 1 UPS (Edificio O Piso 3)
- 1 NVR (CFT Prat)

### Campus Pucón (2 componentes)
- 1 Core Switch (CORE-SW-PUCON)
- 1 Switch (Edificio A)

### Campus Angol (2 componentes)
- 1 Core Switch (CORE-SW-ANGOL)
- 1 Switch (Edificio Administrativo)

### Campus Medicina (2 componentes)
- 1 Core Switch (CORE-SW-MED)
- 1 Switch (Hospital Clínico)

---

## 📊 Resumen Estadístico Final

| Tabla | Registros |
|-------|----------:|
| camaras | 0 |
| fallas | 0 |
| tipos_fallas | 10 |
| casos_reales | 4 |
| fallas_especificas | 2 |
| mantenimientos_realizados | 1 |
| infraestructura_red | 15 |
| relaciones_componentes | 0 |
| **TOTAL** | **32** |

---

## ✅ Verificaciones Realizadas

- ✓ Todas las tablas creadas correctamente
- ✓ Campos `campus` agregados a tablas relevantes
- ✓ Caso 4 (ZM) insertado con todos sus detalles
- ✓ Tipos de fallas estándar configurados
- ✓ Infraestructura de red de 4 campus insertada
- ✓ Soporte para SQLite y PostgreSQL implementado
- ✓ Reporte final generado automáticamente

---

## 🚀 Cómo Usar la Base de Datos

### Ejecutar el Script de Integración
```bash
python3 code/integracion_completa_sistema_camaras.py
```

### Consultar la Base de Datos

```bash
# Usando SQLite CLI
sqlite3 sistema_camaras.db

# Ver todas las tablas
.tables

# Ver casos reales
SELECT * FROM casos_reales;

# Ver tipos de fallas
SELECT categoria, nombre, prioridad FROM tipos_fallas;

# Ver infraestructura por campus
SELECT campus, tipo_componente, ubicacion 
FROM infraestructura_red 
ORDER BY campus, nivel_jerarquico;
```

### Consultar desde Python

```python
import sqlite3

conn = sqlite3.connect('sistema_camaras.db')
cursor = conn.cursor()

# Obtener casos reales
cursor.execute("SELECT * FROM casos_reales")
casos = cursor.fetchall()

for caso in casos:
    print(caso)

conn.close()
```

---

## 📝 Próximos Pasos Sugeridos

1. **Migrar datos históricos:** Importar datos desde los archivos Excel existentes
2. **Poblar tabla de cámaras:** Agregar las 474 cámaras del sistema
3. **Completar infraestructura:** Agregar más componentes de red (switches, gabinetes, UPS)
4. **Definir relaciones:** Llenar tabla `relaciones_componentes` con jerarquía de red
5. **Integrar con aplicación Flask:** Conectar esta BD con el backend de la aplicación
6. **Migrar a PostgreSQL:** Para producción en Railway

---

## 🛠️ Información Técnica

### Requisitos
- Python 3.x
- sqlite3 (incluido en Python)
- psycopg2 (opcional, para PostgreSQL)

### Compatibilidad
- ✅ SQLite 3.x (desarrollo local)
- ✅ PostgreSQL (producción)
- ✅ Railway (deployment)

### Variables de Entorno
- `DATABASE_URL`: URL de PostgreSQL (opcional)
  - Si no está definida, usa SQLite por defecto

---

## 📞 Contacto y Soporte

**Desarrollado por:** MiniMax Agent
**Fecha de creación:** 2025-10-20
**Proyecto:** Sistema de Gestión de Cámaras UFRO

---

**✅ INTEGRACIÓN COMPLETADA EXITOSAMENTE**
