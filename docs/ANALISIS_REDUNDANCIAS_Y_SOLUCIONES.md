# Análisis Completo de Redundancias de Datos - Sistema Cámaras UFRO

**Fecha:** 2025-10-20  
**Autor:** MiniMax Agent

## Resumen Ejecutivo

Se identificaron **múltiples redundancias críticas** tanto en la base de datos SQLite como en las planillas Excel que pueden causar:
- **Inconsistencia de datos** (misma información en múltiples lugares)
- **Duplicados** (registros repetidos)
- **Información fragmentada** (datos relacionados en tablas/archivos separados)
- **Complejidad en el mantenimiento** (cambios requieren actualizar múltiples lugares)

---

## 🔴 REDUNDANCIAS CRÍTICAS IDENTIFICADAS

### 1. BASE DE DATOS SQLite

#### 1.1. Tres Tablas de Fallas con Información Superpuesta

**Problema:**  
Existen 3 tablas que almacenan información de fallas/incidentes con **campos redundantes**:

| Tabla | Registros | Propósito Original | Problemas |
|-------|-----------|-------------------|----------|
| `fallas` | 0 | Fallas de cámaras | Vacía, no se usa |
| `fallas_especificas` | 8 | Fallas de componentes | Datos reales, algunos duplicados |
| `casos_reales` | 5 | Casos de estudio | Datos reales, información similar |

**Campos Redundantes:**
```
fallas:               casos_reales:           fallas_especificas:
- descripcion         - descripcion           - descripcion_falla
- fecha_reporte       - fecha_caso            - fecha_falla
- fecha_resolucion    - (calculado)           - fecha_resolucion
- tiempo_resolucion   - tiempo_resolucion_h   - tiempo_downtime_horas
- tecnico_asignado    - (implícito)           - tecnico_reparador
- solucion            - solucion_aplicada     - solucion_aplicada
- costo               - (no tiene)            - costo_reparacion
- estado              - (no tiene)            - estado
- prioridad           - (no tiene)            - prioridad
```

**Datos Duplicados Detectados:**
- **Caso CFT Prat** (cable suelto NVR): Aparece en `casos_reales` (id=7) y `fallas_especificas` (id=1 y id=3 duplicado)
- **Mantenimiento UPS Edificio O**: Aparece en `casos_reales` (id=6) y `mantenimientos_realizados` (id=1 y id=2 duplicado)

---

#### 1.2. Tabla `tecnicos` con 16 Registros (Debería Tener 4)

**Problema:**  
La tabla `tecnicos` tiene **4x duplicados**:

```sql
SELECT COUNT(*) FROM tecnicos;  -- Resultado: 16

Datos únicos esperados: 4 técnicos
- Oliver Carrasco
- Marcos Altamirano  
- Charles Jélvez
- Marco Contreras
```

**Causa:**  
Ejecución múltiple del script `task_2_crear_tabla_tecnicos.py` sin validación de duplicados.

---

#### 1.3. Tabla `mantenimientos_realizados` con Registros Duplicados

**Problema:**  
2 registros idénticos del mismo mantenimiento:

```
Registro 1 y 2 (DUPLICADOS):
- fecha_mantenimiento: 2024-10-13
- componente_id: ups-edificio-o-p3
- descripcion: Cambio preventivo de 1 batería...
- costo_total: $45,000
```

---

#### 1.4. Campos de Ubicación Redundantes en Múltiples Tablas

**Problema:**  
Información de ubicación **repetida** en lugar de normalizada:

```
Tabla camaras:          Tabla infraestructura_red:    Tabla fallas_especificas:
- ubicacion             - ubicacion                   - (no tiene ubicación directa)
- edificio              - campus                      - campus
- piso
- campus
```

**Consecuencia:**  
Cambiar la ubicación de un campus/edificio requiere actualizar múltiples tablas.

---

#### 1.5. Campos de Estado Inconsistentes

**Problema:**  
Campo `estado` con **valores no estandarizados**:

```
fallas_especificas.estado:
- "Resuelto" (algunos registros)

Valores esperados (según especificación):
- Pendiente
- Asignada
- En Proceso
- Reparada
- Cerrada
- Cancelada
```

---

### 2. PLANILLAS EXCEL

#### 2.1. Duplicación de Información de Cámaras

**Problema:**  
2 archivos con datos de cámaras:

| Archivo | Filas | Columnas | Diferencias |
|---------|-------|----------|-------------|
| `Listadecámaras.xlsx` | 467 | 12 | Datos originales del sistema |
| `Listadecámaras_modificada.xlsx` | 467 | 25 | Datos enriquecidos con relaciones |

**Campos Duplicados:**
```
Listadecámaras.xlsx:        Listadecámaras_modificada.xlsx:
- Nombre de cámara          - Nombre de Cámara
- Dirección IP              - IP de Cámara
- Área                      - Ubicación Específica / Campus/Edificio
```

**Recomendación:**  
Usar **solo** `Listadecámaras_modificada.xlsx` (más completo).

---

#### 2.2. Información de Fallas en Múltiples Archivos

**Problema:**  
3 archivos con información de fallas:

| Archivo | Filas | Propósito | Estado |
|---------|-------|-----------|--------|
| `Fallas_Actualizada.xlsx` | 1 | Fallas reportadas | Casi vacío |
| `Ejemplos_Fallas_Reales.xlsx` | 5 | Casos de ejemplo | Casos reales |
| `Catalogo_Tipos_Fallas.xlsx` | 17 | Catálogo de tipos | Referencia |

**Campos Redundantes:**
```
Fallas_Actualizada.xlsx:        Ejemplos_Fallas_Reales.xlsx:
- Tipo de Falla                 - Tipo de Falla / Subtipo
- Descripción                   - Descripción
- Cámara Afectada               - Cámara Afectada
- Ubicación                     - Ubicación
- Estado                        - Estado de Reparación
```

---

#### 2.3. Información de Equipos Técnicos Duplicada

**Problema:**  
Archivo `Equipos_Tecnicos.xlsx` contiene datos de **UPS/NVR/DVR**, que también podrían estar en planillas específicas de esos equipos.

**Contenido:**
- UPS (tipo de equipo)
- NVR/DVR (grabadores)
- Capacidades, baterías, etc.

**Conflicto:**  
No existe una planilla única de UPS, NVR, Fuentes de Poder → Datos fragmentados.

---

#### 2.4. Información de Ubicación Redundante

**Problema:**  
Múltiples planillas incluyen información de ubicación:

```
Listadecámaras_modificada.xlsx:
- Campus/Edificio, Ubicación Específica

Gabinetes.xlsx:
- Campus/Edificio, Piso/Nivel, Ubicación Detallada, Referencia de Ubicación

Ubicaciones.xlsx:
- Campus, Edificio, Piso/Nivel, Zona
```

**Consecuencia:**  
Información de campus/edificios **no normalizada**. Cambiar nombre de un edificio requiere actualizar 3+ archivos.

---

#### 2.5. Falta de Archivos para Equipos Críticos

**Problema:**  
No existen planillas dedicadas para:

- ❌ **UPS.xlsx** (solo está en `Equipos_Tecnicos.xlsx` mezclado)
- ❌ **NVR_DVR.xlsx** (mismo problema)
- ❌ **Fuentes_Poder.xlsx** (no existe)

**Consecuencia:**  
Datos de equipos críticos **dispersos** en múltiples archivos o ausentes.

---

## ✅ PROPUESTAS DE SOLUCIÓN

### FASE 1: Reestructuración de Base de Datos SQLite

#### Solución 1.1: Consolidar Tablas de Fallas en una Sola Tabla `fallas`

**Acción:**  
Crear una **nueva tabla `fallas` unificada** que reemplace a:
- `fallas` (vacía → rediseñar)
- `fallas_especificas` (8 registros → migrar)
- `casos_reales` (5 registros → migrar)

**Nueva Estructura Propuesta:**

```sql
CREATE TABLE fallas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Clasificación
    tipo_falla_id INTEGER,  -- FK a tipos_fallas
    categoria TEXT,  -- CAMARA, SWITCH, UPS, NVR, GABINETE, CABLE, ELECTRICO, RED
    
    -- Componente Afectado (polimórfico)
    equipo_tipo TEXT,  -- 'camara', 'switch', 'ups', 'nvr', 'gabinete', 'cable'
    equipo_id TEXT,  -- ID del equipo afectado (puede ser texto o número)
    
    -- Detalles de la Falla
    descripcion TEXT NOT NULL,
    fecha_reporte TIMESTAMP NOT NULL,
    reportado_por_id INTEGER,  -- FK a usuarios (futuro)
    
    -- Ubicación
    campus TEXT,
    ubicacion TEXT,
    
    -- Workflow
    estado TEXT DEFAULT 'Pendiente',  -- Pendiente, Asignada, En Proceso, Reparada, Cerrada, Cancelada
    prioridad TEXT DEFAULT 'Media',  -- Baja, Media, Alta, Crítica
    
    -- Asignación
    fecha_asignacion TIMESTAMP,
    tecnico_asignado_id INTEGER,  -- FK a tecnicos
    
    -- Resolución
    fecha_inicio_reparacion TIMESTAMP,
    fecha_fin_reparacion TIMESTAMP,
    tiempo_resolucion_horas REAL,  -- Calculado: (fin - inicio)
    solucion_aplicada TEXT,
    materiales_utilizados TEXT,  -- JSON array
    costo_reparacion REAL,
    
    -- Impacto
    camaras_afectadas TEXT,  -- JSON array de IDs de cámaras
    tiempo_downtime_horas REAL,
    
    -- Metadatos
    observaciones TEXT,
    lecciones_aprendidas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tipo_falla_id) REFERENCES tipos_fallas(id),
    FOREIGN KEY (tecnico_asignado_id) REFERENCES tecnicos(id)
);
```

**Migración:**

1. Insertar datos de `fallas_especificas` (8 registros)
2. Insertar datos de `casos_reales` (5 registros) adaptando campos
3. Eliminar duplicados durante migración
4. DROP TABLE `fallas_especificas`, `casos_reales`

---

#### Solución 1.2: Limpiar Tabla `tecnicos`

**Acción:**

```sql
-- Eliminar todos los duplicados
DELETE FROM tecnicos;

-- Reinsertar solo los 4 técnicos únicos
INSERT INTO tecnicos (nombre, apellido, nombre_completo, especialidad, rol, estado) VALUES
('Oliver', 'Carrasco', 'Oliver Carrasco', 'Mantenimiento de Cámaras', 'Técnico', 'Activo'),
('Marcos', 'Altamirano', 'Marcos Altamirano', 'Sistemas de Vigilancia', 'Técnico', 'Activo'),
('Charles', 'Jélvez', 'Charles Jélvez', 'Administración de Sistemas', 'SuperAdmin', 'Activo'),
('Marco', 'Contreras', 'Marco Contreras', 'Encargado Seguridad', 'Supervisor', 'Activo');
```

---

#### Solución 1.3: Limpiar Duplicados en `mantenimientos_realizados`

**Acción:**

```sql
-- Identificar duplicados
SELECT fecha_mantenimiento, componente_id, COUNT(*) as duplicados
FROM mantenimientos_realizados
GROUP BY fecha_mantenimiento, componente_id
HAVING COUNT(*) > 1;

-- Eliminar duplicados (mantener solo el ID más bajo)
DELETE FROM mantenimientos_realizados
WHERE id NOT IN (
    SELECT MIN(id)
    FROM mantenimientos_realizados
    GROUP BY fecha_mantenimiento, componente_id, descripcion_trabajo
);
```

---

#### Solución 1.4: Normalizar Ubicaciones

**Acción:**  
Crear una tabla `ubicaciones` centralizada:

```sql
CREATE TABLE ubicaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campus TEXT NOT NULL,
    edificio TEXT,
    piso TEXT,
    zona TEXT,
    descripcion TEXT,
    latitud REAL,
    longitud REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Modificar tablas existentes para usar FK:
ALTER TABLE camaras ADD COLUMN ubicacion_id INTEGER REFERENCES ubicaciones(id);
ALTER TABLE infraestructura_red ADD COLUMN ubicacion_id INTEGER REFERENCES ubicaciones(id);
```

**Migración:**
1. Extraer ubicaciones únicas de `camaras`, `infraestructura_red`, etc.
2. Insertar en tabla `ubicaciones`
3. Actualizar referencias en tablas originales
4. Eliminar columnas redundantes (`campus`, `edificio`, `piso`)

---

#### Solución 1.5: Estandarizar Estados de Fallas

**Acción:**

```sql
-- Crear tabla de estados válidos
CREATE TABLE estados_falla (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    orden INTEGER
);

INSERT INTO estados_falla (nombre, descripcion, orden) VALUES
('Pendiente', 'Falla reportada, sin asignar', 1),
('Asignada', 'Asignada a técnico', 2),
('En Proceso', 'Técnico trabajando', 3),
('Reparada', 'Reparación completada', 4),
('Cerrada', 'Verificada y cerrada', 5),
('Cancelada', 'Duplicada o error', 6);

-- Agregar constraint a tabla fallas
ALTER TABLE fallas ADD CONSTRAINT chk_estado 
CHECK (estado IN ('Pendiente', 'Asignada', 'En Proceso', 'Reparada', 'Cerrada', 'Cancelada'));
```

---

### FASE 2: Consolidación de Planillas Excel

#### Solución 2.1: Usar Única Planilla de Cámaras

**Acción:**

✅ **Usar:** `Listadecámaras_modificada.xlsx` (467 filas, 25 columnas)  
❌ **Eliminar:** `Listadecámaras.xlsx` (archivo obsoleto)

**Justificación:**  
`Listadecámaras_modificada.xlsx` incluye:
- Todos los datos de la versión original
- Relaciones adicionales: Gabinete, Switch, Puerto, NVR

---

#### Solución 2.2: Consolidar Información de Fallas

**Acción:**

✅ **Mantener:**
- `Catalogo_Tipos_Fallas.xlsx` → Para catálogo de referencia
- `Ejemplos_Fallas_Reales.xlsx` → Para casos de estudio documentados

✅ **Usar como Plantilla:**
- `Fallas_Actualizada.xlsx` → Para registro operativo de fallas nuevas

**Flujo de Trabajo:**
1. Nuevas fallas → Registrar en `Fallas_Actualizada.xlsx`
2. Casos relevantes → Migrar a `Ejemplos_Fallas_Reales.xlsx` como documentación
3. Tipos nuevos → Agregar a `Catalogo_Tipos_Fallas.xlsx`

---

#### Solución 2.3: Crear Planillas Faltantes de Equipos

**Acción:**  
Crear 3 nuevos archivos Excel:

1. **`UPS.xlsx`**
```
Columnas:
- ID UPS
- Modelo
- Marca
- Capacidad (VA)
- Número de Baterías
- Gabinete Asociado
- Ubicación
- Campus
- Estado
- Fecha Instalación
- Equipos que Alimenta (lista)
- Observaciones
```

2. **`NVR_DVR.xlsx`**
```
Columnas:
- ID NVR
- Tipo (NVR/DVR)
- Modelo
- Marca
- Número de Canales
- Cámaras Conectadas (lista)
- IP
- Ubicación
- Campus
- Estado
- Observaciones
```

3. **`Fuentes_Poder.xlsx`**
```
Columnas:
- ID Fuente
- Modelo
- Voltaje
- Amperaje
- Equipos que Alimenta
- Gabinete
- Ubicación
- Campus
- Estado
- Observaciones
```

**Migración:**  
Extraer datos relevantes de `Equipos_Tecnicos.xlsx` → Dividir en archivos especializados.

---

#### Solución 2.4: Normalizar Ubicaciones en Excel

**Acción:**

✅ **Mantener:** `Ubicaciones.xlsx` como **tabla maestra** de ubicaciones.

✅ **Estandarizar:** Todas las demás planillas deben referenciar ubicaciones usando **ID Ubicación**.

**Cambios en Planillas:**

```
Listadecámaras_modificada.xlsx:
- Eliminar: Campus/Edificio (columnas redundantes)
- Agregar: ID Ubicación (FK a Ubicaciones.xlsx)

Gabinetes.xlsx:
- Eliminar: Campus/Edificio, Piso/Nivel, Ubicación Detallada
- Agregar: ID Ubicación (FK a Ubicaciones.xlsx)

Switches.xlsx, UPS.xlsx, NVR_DVR.xlsx:
- Agregar: ID Ubicación (FK a Ubicaciones.xlsx)
```

**Beneficio:**  
Cambiar nombre de un campus/edificio → Solo actualizar `Ubicaciones.xlsx`.

---

### FASE 3: Sincronización BD ↔ Excel

#### Solución 3.1: Script de Migración Unidireccional

**Acción:**  
Crear `migrate_excel_to_db_unificado.py` que:

1. Lea **todas** las planillas Excel consolidadas
2. Valide datos (sin duplicados, estados válidos)
3. Inserte en base de datos SQLite/PostgreSQL
4. Genere log de errores/warnings

**Flujo:**
```
Excel (fuente única de verdad) → SQLite → PostgreSQL (Railway)
```

---

#### Solución 3.2: Regla Anti-Duplicados para Fallas

**Acción:**  
Implementar validación antes de insertar fallas:

```python
def validar_falla_antes_insertar(camara_id):
    """
    Validación ANTI-DUPLICADOS:
    - Buscar fallas previas para esa cámara
    - Verificar estado de la última falla
    - Permitir inserción solo si última falla está 'Cerrada' o 'Cancelada'
    """
    ultima_falla = db.query(
        "SELECT estado FROM fallas WHERE equipo_id = ? ORDER BY fecha_reporte DESC LIMIT 1",
        (camara_id,)
    ).fetchone()
    
    if ultima_falla and ultima_falla['estado'] in ['Pendiente', 'Asignada', 'En Proceso']:
        raise ValueError(f"La cámara {camara_id} ya tiene una falla abierta en estado '{ultima_falla['estado']}'")
    
    return True
```

---

## 📋 RESUMEN DE ACCIONES PRIORITARIAS

### Base de Datos

| # | Acción | Prioridad | Impacto |
|---|--------|-----------|----------|
| 1 | Consolidar 3 tablas de fallas en una sola | 🔴 CRÍTICA | Elimina redundancia masiva |
| 2 | Limpiar duplicados en `tecnicos` (16→4) | 🔴 CRÍTICA | Datos corruptos |
| 3 | Eliminar duplicados en `mantenimientos` | 🟡 ALTA | Integridad de datos |
| 4 | Normalizar ubicaciones con FK | 🟡 ALTA | Facilita mantenimiento |
| 5 | Estandarizar estados de fallas | 🟢 MEDIA | Mejora validación |

### Planillas Excel

| # | Acción | Prioridad | Impacto |
|---|--------|-----------|----------|
| 1 | Eliminar `Listadecámaras.xlsx` (usar modificada) | 🔴 CRÍTICA | Evita confusión |
| 2 | Crear `UPS.xlsx`, `NVR_DVR.xlsx`, `Fuentes_Poder.xlsx` | 🟡 ALTA | Completa inventario |
| 3 | Normalizar ubicaciones con IDs | 🟡 ALTA | Elimina redundancia |
| 4 | Definir flujo de trabajo para fallas | 🟢 MEDIA | Mejora proceso |

---

## 🚀 PLAN DE IMPLEMENTACIÓN SUGERIDO

### Paso 1: Backup Completo ✅
```bash
cp sistema_camaras.db sistema_camaras.db.backup_20251020
zip -r planillas_backup_20251020.zip user_input_files/planillas-web/
```

### Paso 2: Reestructurar Base de Datos
```bash
python code/task_2_reestructurar_bd.py  # Script ya creado
```

### Paso 3: Consolidar Planillas Excel
- Crear `UPS.xlsx`, `NVR_DVR.xlsx`, `Fuentes_Poder.xlsx`
- Agregar columna `ID Ubicación` a planillas principales
- Eliminar `Listadecámaras.xlsx`

### Paso 4: Migración Excel → BD
```bash
python migrate_excel_to_db_unificado.py
```

### Paso 5: Validación
- Verificar counts de tablas
- Verificar que no hay duplicados
- Probar consultas de reportes

---

## 📊 BENEFICIOS ESPERADOS

✅ **Eliminación de Redundancia:**  
- 3 tablas de fallas → 1 tabla unificada
- 16 técnicos duplicados → 4 técnicos únicos
- 2 archivos de cámaras → 1 archivo maestro

✅ **Integridad de Datos:**  
- Ubicaciones normalizadas (FK)
- Estados estandarizados
- Validación anti-duplicados

✅ **Facilidad de Mantenimiento:**  
- Cambios en un solo lugar
- Menos archivos que gestionar
- Estructura clara y documentada

✅ **Migración Futura a Web:**  
- Base de datos lista para Flask + PostgreSQL
- Planillas limpias para migración inicial
- Validaciones ya implementadas

---

**Siguiente Paso Recomendado:**  
Ejecutar `code/task_2_reestructurar_bd.py` para iniciar la consolidación de la base de datos.
