-- SCRIPT PARA ELIMINAR FOREIGN KEY DEPENDENCIES Y TABLAS DUPLICADAS
-- Sistema de Gestión de Cámaras UFRO
-- Autor: MiniMax Agent
-- Fecha: 2025-10-25

-- ===============================================================
-- PARTE 1: ELIMINACIÓN DE FOREIGN KEY CONSTRAINTS
-- ===============================================================

-- Dependencias de la tabla 'usuario':
ALTER TABLE falla DROP CONSTRAINT IF EXISTS falla_reportado_por_id_fkey;
ALTER TABLE falla DROP CONSTRAINT IF EXISTS falla_tecnico_asignado_id_fkey;
ALTER TABLE historial_estado_equipo DROP CONSTRAINT IF EXISTS historial_estado_equipo_usuario_id_fkey;
ALTER TABLE mantenimiento DROP CONSTRAINT IF EXISTS mantenimiento_tecnico_id_fkey;

-- Dependencias de la tabla 'camara':
ALTER TABLE puertos_switch DROP CONSTRAINT IF EXISTS fk_puerto_switch_camara;

-- Dependencias de la tabla 'ubicacion':
ALTER TABLE camara DROP CONSTRAINT IF EXISTS camara_ubicacion_id_fkey;
ALTER TABLE fuente_poder DROP CONSTRAINT IF EXISTS fuente_poder_ubicacion_id_fkey;
ALTER TABLE gabinete DROP CONSTRAINT IF EXISTS gabinete_ubicacion_id_fkey;
ALTER TABLE nvr_dvr DROP CONSTRAINT IF EXISTS nvr_dvr_ubicacion_id_fkey;
ALTER TABLE ups DROP CONSTRAINT IF EXISTS ups_ubicacion_id_fkey;

-- ===============================================================
-- PARTE 2: ELIMINACIÓN DE TABLAS DUPLICADAS
-- ===============================================================

-- Verificar que las tablas plurales existen (usando datos reales)
SELECT 'Verificando tablas principales...' AS status;
SELECT COUNT(*) FROM usuarios;
SELECT COUNT(*) FROM camaras;
SELECT COUNT(*) FROM ubicaciones;

-- Eliminar tablas singulares (duplicadas)
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS camara CASCADE;
DROP TABLE IF EXISTS ubicacion CASCADE;

-- ===============================================================
-- PARTE 3: VERIFICACIÓN FINAL
-- ===============================================================

SELECT 'Estado final de la base de datos' AS status;
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
