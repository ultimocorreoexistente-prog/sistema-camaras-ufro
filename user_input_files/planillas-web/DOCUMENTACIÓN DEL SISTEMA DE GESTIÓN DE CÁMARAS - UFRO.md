# DOCUMENTACIÓN DEL SISTEMA DE GESTIÓN DE CÁMARAS - UFRO

## CAMBIOS REALIZADOS EN LA PLANILLA ORIGINAL

### Archivo: Listadecámaras_modificada.xlsx

**Columnas agregadas:**
1. Ubicación Específica - Detalle exacto de dónde está la cámara
2. Gabinete Asociado - ID del gabinete/rack al que se conecta
3. Switch Asociado - ID del switch que la conecta
4. Puerto Switch - Número de boca/puerto del switch
5. NVR Asociado (Cámara) - NVR al que la cámara envía señal
6. Puerto NVR (Cámara) - Puerto del NVR al que la cámara está conectada
7. Tipo de Cámara - Domo, PTZ, Bullet, etc.
8. Requiere POE Adicional - Para cámaras PTZ que necesitan POE externo
9. Tipo de Conexión - Directa, Fibra Óptica, etc.
10. Estado de Funcionamiento - Funcionando, Averiada, etc.
11. Instalador - Técnico propio o empresa subcontratista
12. Fecha de Instalación
13. Observaciones

**Columnas renombradas para mayor claridad:**
- "Nombre de cámara" → "Nombre de Cámara"
- "Dirección IP del dispositivo" → "IP de Cámara" (DATO MUY IMPORTANTE)
- "Nombre de dispositivo" → "NVR/DVR Asociado (Original)" (para evitar conflicto con el nuevo campo de NVR asociado a la cámara)
- Otras columnas técnicas renombradas para consistencia

**Manejo de Cámaras PTZ con 'Área' genérica:**
- Para cámaras donde el campo 'Área' original es genérico (ej. "CAM-PTZ"), se ha implementado una lógica para intentar inferir el `Tipo de Cámara` (PTZ). Los campos de ubicación y conectividad (`Ubicación Específica`, `Gabinete Asociado`, `Switch Asociado`, `Puerto Switch`, `NVR Asociado (Cámara)`, `Puerto NVR (Cámara)`) se dejarán en blanco si no se pueden inferir de forma fiable, para que puedan ser completados manualmente con la información precisa.
- Se prioriza el uso de `Ubicación Específica`, `Gabinete Asociado`, `Switch Asociado` y `Puerto Switch` para la localización y conectividad detallada.

## PLANILLAS NUEVAS CREADAS

### 1. Gabinetes.xlsx
Registra todos los gabinetes/racks del sistema con:
- **Tipo de Ubicación General:** Interior, Subterráneo, Exterior
- **Tipo de Ubicación Detallada:** Dentro de Edificio (Piso), Cámara Subterránea, En Poste, Adosado a Construcción
- Ubicación física detallada (Ej: Sala técnica 3er piso, Cámara subterránea acceso norte, Poste de luz principal)
- Referencia de Ubicación (Ej: Cercano a estacionamiento, Junto a sala de servidores)
- Equipamiento que contiene (UPS, Switch, NVR/DVR)
- Estado y fecha de última revisión
- Conexiones de fibra óptica

### 2. Switches.xlsx
Información de todos los switches con:
- Modelo, marca, número de serie
- **Gabinete donde está instalado**
- Cantidad de puertos (total, usados, disponibles)
- Capacidad PoE
- Fecha de mantenimiento

### 3. Puertos_Switch.xlsx
Detalle de cada puerto de cada switch:
- Qué dispositivo está conectado en cada puerto
- IP del dispositivo conectado
- Estado del puerto (En uso, Disponible, Averiado)
- Tipo de conexión (PoE, Fibra, etc.)
- **NVR Asociado (Puerto):** NVR al que la cámara conectada a este puerto envía señal
- **Puerto NVR (Puerto):** Puerto específico del NVR al que la cámara está conectada

### 4. Equipos_Tecnicos.xlsx
Registro de UPS, POE externos, Fuentes de poder, **NVR/DVRs**:
- Marca, modelo, capacidad (o canales para NVR)
- Número de baterías (para UPS)
- Gabinete asociado
- Qué equipos alimenta
- Historial de mantenimiento

### 5. Fallas.xlsx
Sistema de registro de fallas con:
- Tipos: Cables rotos, Cámaras quemadas, Vandalismo, Switches quemados, 
  Fuentes quemadas, POE averiado, UPS averiado, NVR averiado, Postes dañados
- Relación con gabinete, switch y puerto afectado
- Impacto en el sistema
- Seguimiento de resolución
- **Técnicos Asignables:** Técnico Propio, Oliver Carrasco, Marco Altamirano, Empresa Subcontratista (ej. ConectaSur)

### 6. Mantenimientos.xlsx
Historial de mantenimientos con:
- Tipo: Preventivo, Correctivo, Predictivo
- Equipo/gabinete intervenido
- Materiales utilizados
- Equipos/cámaras afectadas durante el mantenimiento
- Tiempo de ejecución y costo
- **Técnicos Responsables:** Técnico Propio, Oliver Carrasco, Marco Altamirano, Empresa Subcontratista (ej. ConectaSur)

### 7. Ubicaciones.xlsx
Catálogo de ubicaciones físicas:
- Campus, Edificio, Piso
- Gabinetes presentes
- Cantidad de cámaras por ubicación

## RELACIONES ENTRE PLANILLAS

```
UBICACIONES
    ↓
GABINETES (contienen)
    ↓
EQUIPOS TÉCNICOS (UPS, Switch, NVR/DVR)
    ↓
SWITCHES (tienen)
    ↓
PUERTOS SWITCH (conectan)
    ↓
CÁMARAS (con IP específica)
    ↓
NVRs (reciben señal de cámaras conectadas a puertos específicos)
```

## EJEMPLO DE CASO REAL (13/10/2025)

**Mantenimiento en Edificio O:**
- Ubicación: Edificio O - 3er Piso (Sala técnica)
- Gabinete: GAB-001 (Rack Edificio O - 3P)
- Equipo: UPS-001 (APC Smart-UPS 1500)
- Acción: Cambio de 1 batería
- Switch: SW-001 (24 puertos)
- Cámaras afectadas: 10 domo + 1 PTZ
- Conexión adicional: Enlace por fibra óptica a gabinete subterráneo (Cámara PTZ Francisco Salazar)

**Conexión de Cámara PTZ Francisco Salazar:**
- Ubicación: Subterráneo Francisco Salazar
- Gabinete: GAB-002
- Switch: SW-002 (8 puertos)
- Puerto: 1
- POE adicional: Sí (POE-001)
- Conexión: Fibra óptica desde GAB-001
- NVR Asociado: NVR-002
- Puerto NVR: 1

## DATOS IMPORTANTES

- **IP de Cámara**: Campo crítico para identificación y acceso
- **Puerto Switch**: Esencial para troubleshooting de conectividad
- **Gabinete Asociado**: Permite ubicar físicamente el problema
- **Fecha de Mantenimiento**: Control de historial de equipos
- **NVR Asociado (Cámara) y Puerto NVR (Cámara)**: Crucial para el seguimiento de grabaciones y visualización.

## USO DEL SISTEMA WEB

El sitio web integra todas estas planillas permitiendo:
- Visualización de relaciones entre componentes
- Búsqueda por IP, ubicación, gabinete o switch
- Registro rápido de fallas y mantenimientos
- Exportación de reportes
- Dashboard con estado general del sistema
