-- MIGRACIÓN: Implementación 4 Prioridades CRÍTICAS
-- Fecha: 2025-10-25
-- Descripción: Agregar modelos Enlaces y VLAN + campos firmware y autonomía

-- PRIORIDAD 4: Agregar campos de autonomía y alertas a UPS
ALTER TABLE ups ADD COLUMN IF NOT EXISTS autonomia_minutos INTEGER;
ALTER TABLE ups ADD COLUMN IF NOT EXISTS porcentaje_carga_actual FLOAT;
ALTER TABLE ups ADD COLUMN IF NOT EXISTS alertas_bateria_baja BOOLEAN DEFAULT FALSE;
ALTER TABLE ups ADD COLUMN IF NOT EXISTS alertas_sobrecarga BOOLEAN DEFAULT FALSE;

-- PRIORIDAD 2: Agregar campos de firmware a Cámaras
ALTER TABLE camaras ADD COLUMN IF NOT EXISTS version_firmware VARCHAR(50);
ALTER TABLE camaras ADD COLUMN IF NOT EXISTS fecha_actualizacion_firmware DATE;
ALTER TABLE camaras ADD COLUMN IF NOT EXISTS proxima_revision_firmware DATE;

-- PRIORIDAD 3: Crear tabla VLAN
CREATE TABLE IF NOT EXISTS vlan (
    id SERIAL PRIMARY KEY,
    vlan_id INTEGER UNIQUE NOT NULL,
    vlan_nombre VARCHAR(100) NOT NULL,
    vlan_descripcion TEXT,
    red VARCHAR(45),
    mascara VARCHAR(45),
    gateway VARCHAR(45),
    switch_id INTEGER REFERENCES switch(id),
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion DATE,
    observaciones TEXT
);

-- PRIORIDAD 3: Agregar relación VLAN a Puerto_Switch
ALTER TABLE puertos_switch ADD COLUMN IF NOT EXISTS vlan_id INTEGER REFERENCES vlan(id);

-- PRIORIDAD 1: Crear tabla Enlace
CREATE TABLE IF NOT EXISTS enlace (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200),
    tipo_enlace VARCHAR(50) NOT NULL,
    origen_ubicacion_id INTEGER REFERENCES ubicaciones(id),
    destino_ubicacion_id INTEGER REFERENCES ubicaciones(id),
    switch_origen_id INTEGER REFERENCES switch(id),
    switch_destino_id INTEGER REFERENCES switch(id),
    latencia_ms FLOAT,
    porcentaje_perdida_paquetes FLOAT,
    estado_conexion VARCHAR(20) DEFAULT 'Activo',
    ancho_banda_mbps INTEGER,
    proveedor VARCHAR(200),
    fecha_instalacion DATE,
    fecha_ultimo_testeo DATE,
    observaciones TEXT
);

-- Comentarios explicativos
COMMENT ON TABLE vlan IS 'Gestión de VLANs para segmentación de red';
COMMENT ON TABLE enlace IS 'Gestión de enlaces de conectividad entre ubicaciones';
COMMENT ON COLUMN ups.autonomia_minutos IS 'Autonomía del UPS en minutos';
COMMENT ON COLUMN ups.porcentaje_carga_actual IS 'Porcentaje de carga actual del UPS';
COMMENT ON COLUMN camaras.version_firmware IS 'Versión del firmware instalado en la cámara';
COMMENT ON COLUMN camaras.proxima_revision_firmware IS 'Fecha programada para próxima revisión de firmware';
