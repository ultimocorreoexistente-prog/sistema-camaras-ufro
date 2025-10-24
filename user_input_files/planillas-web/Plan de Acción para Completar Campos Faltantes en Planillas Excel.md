# Plan de Acción para Completar Campos Faltantes en Planillas Excel

Este plan de acción paso a paso está diseñado para guiarle en el proceso de completar los campos faltantes en las planillas Excel, priorizando la información más crítica para asegurar la funcionalidad y precisión del sistema de gestión de cámaras. La consistencia en el llenado de los datos es fundamental.

## Principios de Priorización

1.  **Fundacional:** Completar primero los datos que sirven de base para otras planillas (ej. ubicaciones, gabinetes).
2.  **Relacional:** Establecer las relaciones clave entre los diferentes componentes (ej. switch en gabinete, cámara en puerto de switch).
3.  **Detalle:** Añadir los detalles específicos de cada elemento una vez que sus relaciones principales estén establecidas.

## Pasos del Plan de Acción

### Paso 1: Definir Ubicaciones Físicas (`Ubicaciones.xlsx`)

Esta es la base de toda la infraestructura. Complete esta planilla con todas las ubicaciones relevantes.

*   **Acción:** Abra `Ubicaciones.xlsx`.
*   **Campos a Completar:**
    *   `ID Ubicación`: Cree un identificador único para cada ubicación (ej. UBI-001, UBI-002).
    *   `Campus`, `Edificio`, `Piso/Nivel`, `Zona`: Describa la jerarquía de la ubicación.
    *   `Gabinetes en Ubicación`: (Opcional en este paso) Puede listar los IDs de gabinetes que estarán en esta ubicación más adelante.
    *   `Cantidad de Cámaras`: (Opcional en este paso) Puede estimar o dejar en blanco por ahora.

### Paso 2: Registrar Gabinetes (`Gabinetes.xlsx`)

Defina cada gabinete y su ubicación precisa, utilizando los IDs de `Ubicaciones.xlsx`.

*   **Acción:** Abra `Gabinetes.xlsx`.
*   **Campos a Completar:**
    *   `ID Gabinete`: Cree un identificador único (ej. GAB-001, GAB-002).
    *   `Nombre de Gabinete`: Nombre descriptivo.
    *   `Tipo de Ubicación General`, `Tipo de Ubicación Detallada`, `Campus/Edificio`, `Piso/Nivel`, `Ubicación Detallada`, `Referencia de Ubicación`: **Estos campos son CRÍTICOS.** Utilice la información definida en `Ubicaciones.xlsx` y sea lo más preciso posible.
    *   `Tiene UPS`, `Tiene Switch`, `Tiene NVR/DVR`, `Conexión Fibra Óptica`: Indique "Sí" o "No" según corresponda.

### Paso 3: Registrar Switches y Equipos Técnicos (`Switches.xlsx`, `Equipos_Tecnicos.xlsx`)

Asocie cada switch y equipo técnico (NVRs, UPS, POE externos) a su respectivo gabinete.

*   **Acción:** Abra `Switches.xlsx`.
*   **Campos a Completar:**
    *   `ID Switch`: Identificador único (ej. SW-001, SW-002).
    *   `Nombre/Modelo`, `Marca`, `Número de Serie`: Información del dispositivo.
    *   `Gabinete Asociado`: **CRÍTICO.** Ingrese el `ID Gabinete` (ej. GAB-001) donde está físicamente instalado el switch. Debe coincidir con un ID de `Gabinetes.xlsx`.
    *   `Número Total de Puertos`, `Puertos Usados`, `Puertos Disponibles`, `Soporta PoE`, `Estado`, `Fecha de Instalación`.

*   **Acción:** Abra `Equipos_Tecnicos.xlsx`.
*   **Campos a Completar:**
    *   `ID Equipo`: Identificador único (ej. NVR-001, UPS-001, POE-001).
    *   `Tipo de Equipo`, `Marca`, `Modelo`, `Número de Serie`, `Capacidad`, `Número de Baterías`.
    *   `Gabinete Asociado`: **CRÍTICO.** Ingrese el `ID Gabinete` donde está instalado el equipo. Debe coincidir con un ID de `Gabinetes.xlsx`.
    *   `Alimenta a`: (Para UPS/POE) Describa qué dispositivos alimenta.

### Paso 4: Detallar Conexiones de Puertos (`Puertos_Switch.xlsx`)

Este es un paso fundamental para la trazabilidad de la red. Detalle cada conexión de cada puerto de switch.

*   **Acción:** Abra `Puertos_Switch.xlsx`.
*   **Campos a Completar:**
    *   `ID Switch`: **CRÍTICO.** El ID del switch al que pertenece el puerto. Debe coincidir con un ID de `Switches.xlsx`.
    *   `Número de Puerto`: El número físico del puerto.
    *   `Estado Puerto`: "En uso", "Disponible", "Averiado".
    *   `Dispositivo Conectado`: **CRÍTICO.** Nombre del dispositivo conectado (ej. "Cámara Domo 1P-01", "Enlace Fibra Óptica a GAB-002").
    *   `IP Dispositivo`: IP del dispositivo conectado (si aplica).
    *   `Tipo de Conexión`: "PoE", "Fibra Óptica", "Uplink".
    *   `NVR Asociado (Puerto)`: **CRÍTICO.** Si el dispositivo conectado es una cámara, ingrese el `ID Equipo` del NVR al que envía la señal. Debe coincidir con un ID de NVR en `Equipos_Tecnicos.xlsx`.
    *   `Puerto NVR (Puerto)`: El puerto específico del NVR al que la cámara envía la señal.

### Paso 5: Completar Detalles de Cámaras (`Listadecámaras_modificada.xlsx`)

Con la información de los pasos anteriores, ahora puede completar los detalles de cada cámara.

*   **Acción:** Abra `Listadecámaras_modificada.xlsx`.
*   **Campos a Completar:**
    *   `Ubicación Específica`: **CRÍTICO.** Detalle exacto de la ubicación física de la cámara.
    *   `Campus/Edificio`: Utilice los valores de `Ubicaciones.xlsx`.
    *   `Gabinete Asociado`: **CRÍTICO.** `ID Gabinete` donde está el switch de la cámara. Debe coincidir con un ID de `Gabinetes.xlsx`.
    *   `Switch Asociado`: **CRÍTICO.** `ID Switch` al que está conectada la cámara. Debe coincidir con un ID de `Switches.xlsx`.
    *   `Puerto Switch`: **CRÍTICO.** Número de puerto del switch. Debe coincidir con `Puertos_Switch.xlsx`.
    *   `NVR Asociado (Cámara)`: **CRÍTICO.** `ID Equipo` del NVR al que envía la señal. Debe coincidir con un ID de NVR en `Equipos_Tecnicos.xlsx`.
    *   `Puerto NVR (Cámara)`: Puerto específico del NVR.
    *   `Tipo de Cámara`: Ej. "Domo", "PTZ", "Bullet".
    *   `Requiere POE Adicional`, `Tipo de Conexión`, `Instalador`, `Fecha de Instalación`.

### Paso 6: Llenar Fallas y Mantenimientos (`Fallas_Actualizada.xlsx`, `Mantenimientos.xlsx`)

Estas planillas se llenarán a medida que ocurran eventos, utilizando los IDs y nombres de los componentes ya definidos.

*   **Acción:** Abra `Fallas_Actualizada.xlsx` y `Mantenimientos.xlsx`.
*   **Campos a Completar:** Utilice los `ID Falla`, `ID Mantenimiento` y asocie las entradas con los `ID Cámara`, `ID Gabinete`, `ID Switch` y `ID NVR` correspondientes, así como los `Técnico Asignado` (Técnico Propio, Oliver Carrasco, Marco Altamirano, ConectaSur).

## Siguientes Pasos después de Completar las Planillas

Una vez que haya completado las planillas siguiendo este plan:

1.  **Notifíqueme:** Indíqueme que ha terminado de rellenar las planillas.
2.  **Actualización del Sistema:** Volveré a procesar las planillas, generaré los archivos JSON y redesplegaré la aplicación web para que refleje todos los datos actualizados.
3.  **Verificación:** Podrá verificar la información en el sitio web y confirmar que todo esté correcto.

Este proceso garantizará que su sistema de gestión de cámaras sea una herramienta poderosa y precisa para la administración de su infraestructura.
