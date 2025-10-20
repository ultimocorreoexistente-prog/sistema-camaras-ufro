# Guía para el Llenado de Planillas Excel del Sistema de Gestión de Cámaras UFRO

Esta guía tiene como objetivo facilitar el proceso de completado de las planillas Excel generadas para el sistema de gestión de cámaras. Es crucial que la información sea precisa y consistente para asegurar el correcto funcionamiento del sistema web y la trazabilidad de la infraestructura.

## Principios Generales

*   **Consistencia:** Utilice los mismos IDs y nombres para los elementos relacionados (gabinetes, switches, NVRs) en todas las planillas.
*   **Precisión:** La exactitud de los datos es fundamental para el análisis de impacto y la resolución de problemas.
*   **Completitud:** Intente llenar todos los campos relevantes. El informe de campos faltantes (`informe_campos_faltantes.md`) le ayudará a identificar las áreas prioritarias.

## Planillas Clave y Cómo Llenarlas

### 1. `Listadecámaras_modificada.xlsx`

Esta es la planilla central para la información de cada cámara. Preste especial atención a las columnas de ubicación y conectividad.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **Nombre de Cámara** | Nombre único de la cámara. | Debe ser descriptivo y único. |
| **IP de Cámara** | Dirección IP de la cámara. | **DATO CRÍTICO.** Asegúrese de que sea la IP correcta y única. |
| **Ubicación Específica** | Detalle exacto de la ubicación física de la cámara. | Ej: "Edificio O - 3er Piso - Pasillo Norte", "Patio Central - Poste 5", "Estacionamiento Subterráneo - Sector A". |
| **Campus/Edificio** | Campus o Edificio general donde se encuentra la cámara. | Ej: "Edificio O", "Francisco Salazar", "Campus Principal". |
| **Gabinete Asociado** | **ID del Gabinete** (`GAB-XXX`) al que está conectado el switch que alimenta/conecta esta cámara. | Debe coincidir con un `ID Gabinete` en `Gabinetes.xlsx`. |
| **Switch Asociado** | **ID del Switch** (`SW-XXX`) al que está conectada la cámara. | Debe coincidir con un `ID Switch` en `Switches.xlsx`. |
| **Puerto Switch** | Número de puerto/boca del `Switch Asociado` al que está conectada la cámara. | Debe coincidir con un `Número de Puerto` en `Puertos_Switch.xlsx` para el `Switch Asociado`. |
| **NVR Asociado (Cámara)** | **ID del NVR** (`NVR-XXX`) al que esta cámara envía su señal de video. | Debe coincidir con un `ID Equipo` de tipo NVR en `Equipos_Tecnicos.xlsx`. |
| **Puerto NVR (Cámara)** | Número de puerto del `NVR Asociado` al que la cámara envía su señal. | Crucial para la trazabilidad de grabaciones. |
| **Tipo de Cámara** | Tipo físico de la cámara. | Ej: "Domo", "PTZ", "Bullet", "Térmica". |
| **Requiere POE Adicional** | Indique "Sí" si la cámara necesita un inyector PoE externo. | Generalmente para PTZ de alto consumo. |
| **Tipo de Conexión** | Tipo de conexión física. | Ej: "PoE", "Fibra Óptica", "WiFi". |
| **Estado de Funcionamiento** | Estado actual de la cámara. | Ej: "Funcionando", "Averiada", "Desconectada", "En Mantenimiento". |
| **Instalador** | Nombre del técnico o empresa que instaló la cámara. | Ej: "Técnico Propio", "ConectaSur", "Oliver Carrasco". |
| **Fecha de Instalación** | Fecha en que la cámara fue instalada. | Formato: AAAA-MM-DD o DD/MM/AAAA. |
| **Observaciones** | Cualquier nota relevante sobre la cámara. | |

### 2. `Gabinetes.xlsx`

Detalla la ubicación y contenido de cada gabinete.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **ID Gabinete** | Identificador único del gabinete. | Ej: "GAB-001". Debe ser único. |
| **Nombre de Gabinete** | Nombre descriptivo del gabinete. | Ej: "Rack Edificio O - 3P". |
| **Tipo de Ubicación General** | Categoría amplia de la ubicación. | Ej: "Interior", "Subterráneo", "Exterior". |
| **Tipo de Ubicación Detallada** | Descripción más específica de la ubicación. | Ej: "Dentro de Edificio (Piso)", "Cámara Subterránea", "En Poste", "Adosado a Construcción". |
| **Campus/Edificio** | Campus o Edificio donde se encuentra el gabinete. | |
| **Piso/Nivel** | Piso o nivel si está dentro de un edificio. | Dejar en blanco si no aplica. |
| **Ubicación Detallada** | Descripción precisa de la ubicación. | Ej: "Sala técnica 3er piso", "Cámara subterránea acceso norte". |
| **Referencia de Ubicación** | Puntos de referencia cercanos. | Ej: "Junto a sala de servidores", "Cercano a estacionamiento". |
| **Tiene UPS** | "Sí" o "No" si el gabinete contiene una UPS. | |
| **Tiene Switch** | "Sí" o "No" si el gabinete contiene al menos un switch. | |
| **Tiene NVR/DVR** | "Sí" o "No" si el gabinete contiene un NVR/DVR. | |
| **Conexión Fibra Óptica** | "Sí" o "No" si el gabinete tiene una conexión de fibra óptica. | |
| **Observaciones** | Notas relevantes. | |

### 3. `Switches.xlsx`

Información de cada switch y su ubicación.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **ID Switch** | Identificador único del switch. | Ej: "SW-001". Debe ser único. |
| **Nombre/Modelo** | Modelo del switch. | Ej: "Switch PoE 24 puertos". |
| **Marca** | Marca del switch. | |
| **Número de Serie** | Número de serie del switch. | |
| **Gabinete Asociado** | **ID del Gabinete** (`GAB-XXX`) donde está instalado el switch. | Debe coincidir con un `ID Gabinete` en `Gabinetes.xlsx`. |
| **Número Total de Puertos** | Cantidad total de puertos del switch. | |
| **Puertos Usados** | Cantidad de puertos actualmente en uso. | |
| **Puertos Disponibles** | Cantidad de puertos libres. | |
| **Soporta PoE** | "Sí" o "No" si el switch soporta Power over Ethernet. | |
| **Estado** | Estado operativo del switch. | Ej: "Funcionando", "Averiado". |
| **Fecha de Instalación** | Fecha de instalación del switch. | |
| **Observaciones** | Notas relevantes. | |

### 4. `Puertos_Switch.xlsx`

Detalle de cada puerto de cada switch, crucial para la conectividad de las cámaras.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **ID Switch** | **ID del Switch** (`SW-XXX`) al que pertenece el puerto. | Debe coincidir con un `ID Switch` en `Switches.xlsx`. |
| **Número de Puerto** | Número físico del puerto en el switch. | Ej: "1", "24". |
| **Estado Puerto** | Estado actual del puerto. | Ej: "En uso", "Disponible", "Averiado". |
| **Dispositivo Conectado** | Nombre del dispositivo conectado a este puerto. | Ej: "Cámara Domo 1P-01", "Enlace Fibra Óptica a GAB-002". |
| **IP Dispositivo** | Dirección IP del dispositivo conectado. | Si es una cámara, debe coincidir con su IP en `Listadecámaras_modificada.xlsx`. |
| **Tipo de Conexión** | Tipo de conexión utilizada en el puerto. | Ej: "PoE", "Fibra Óptica", "Uplink". |
| **NVR Asociado (Puerto)** | **ID del NVR** (`NVR-XXX`) al que el dispositivo conectado a este puerto envía su señal. | Debe coincidir con un `ID Equipo` de tipo NVR en `Equipos_Tecnicos.xlsx`. |
| **Puerto NVR (Puerto)** | Número de puerto del `NVR Asociado` al que el dispositivo envía su señal. | |
| **Observaciones** | Notas relevantes sobre el puerto o la conexión. | |

### 5. `Equipos_Tecnicos.xlsx`

Registro de equipos como UPS, POE externos, NVRs/DVRs.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **ID Equipo** | Identificador único del equipo. | Ej: "UPS-001", "POE-001", "NVR-001". |
| **Tipo de Equipo** | Categoría del equipo. | Ej: "UPS", "POE Externo", "NVR", "DVR". |
| **Marca** | Marca del equipo. | |
| **Modelo** | Modelo específico del equipo. | |
| **Número de Serie** | Número de serie del equipo. | |
| **Capacidad (VA/W/Canales)** | Capacidad del equipo. | Ej: "1500 VA" (UPS), "24W" (POE), "16 Canales" (NVR). |
| **Número de Baterías** | Cantidad de baterías (para UPS). | |
| **Gabinete Asociado** | **ID del Gabinete** (`GAB-XXX`) donde está instalado el equipo. | Debe coincidir con un `ID Gabinete` en `Gabinetes.xlsx`. |
| **Alimenta a** | Qué otros equipos o cámaras alimenta este dispositivo. | Ej: "Switch SW-001, NVR-001". |
| **Estado** | Estado operativo del equipo. | |
| **Fecha de Instalación** | Fecha de instalación. | |
| **Fecha de Último Mantenimiento** | Fecha del último mantenimiento. | |
| **Tipo de Mantenimiento** | Tipo de mantenimiento realizado. | |
| **Observaciones** | Notas relevantes. | |

### 6. `Fallas_Actualizada.xlsx`

Para registrar y dar seguimiento a las fallas.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **ID Falla** | Identificador único de la falla. | Se recomienda un formato como "F-AAAA-NNN". |
| **Fecha de Reporte** | Fecha en que se reportó la falla. | |
| **Reportado Por** | Quién reportó la falla. | Ej: "Central de Monitoreo", "Técnico Propio". |
| **Tipo de Falla** | Categoría principal de la falla. | Ej: "Problemas de Limpieza", "Daño Físico", "Problemas de Conectividad". |
| **Subtipo** | Subcategoría de la falla. | Ej: "Telas de araña", "Mica rallada/dañada", "Sin conexión". |
| **Cámara Afectada** | Nombre de la cámara afectada. | Debe coincidir con un `Nombre de Cámara` en `Listadecámaras_modificada.xlsx`. |
| **Gabinete Relacionado** | **ID del Gabinete** (`GAB-XXX`) donde se encuentra el equipo afectado. | |
| **Switch Relacionado** | **ID del Switch** (`SW-XXX`) afectado o al que está conectado el equipo afectado. | |
| **Puerto Afectado** | Puerto específico del switch si aplica. | |
| **Descripción** | Descripción detallada del problema. | |
| **Impacto en Visibilidad** | Nivel de impacto en la visibilidad de la cámara. | Ej: "Alto", "Medio", "Bajo". |
| **Afecta Visión Nocturna** | "Sí" o "No" si la falla afecta la visión nocturna. | |
| **Estado** | Estado de la falla. | Ej: "Reportada", "En Proceso", "Resuelta", "Cerrada". |
| **Prioridad** | Nivel de prioridad para la resolución. | Ej: "Alta", "Media", "Baja". |
| **Técnico Asignado** | Nombre del técnico o empresa responsable. | Ej: "Técnico Propio", "Oliver Carrasco", "Marco Altamirano", "ConectaSur". |
| **Fecha de Resolución** | Fecha en que se resolvió la falla. | |
| **Solución Aplicada** | Descripción de la solución implementada. | |
| **Materiales Utilizados** | Materiales usados en la reparación. | |
| **Observaciones** | Notas adicionales. | |

### 7. `Mantenimientos.xlsx`

Para registrar las actividades de mantenimiento.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **ID Mantenimiento** | Identificador único del mantenimiento. | Ej: "MNT-AAAA-NNN". |
| **Fecha Programada** | Fecha programada para el mantenimiento. | |
| **Fecha de Realización** | Fecha en que se realizó el mantenimiento. | |
| **Tipo de Mantenimiento** | Categoría del mantenimiento. | Ej: "Preventivo", "Correctivo", "Predictivo". |
| **Categoría** | Subcategoría del mantenimiento. | Ej: "Limpieza", "Cambio de batería", "Actualización de firmware". |
| **Equipo/Gabinete** | Equipo o gabinete al que se le realizó el mantenimiento. | Ej: "UPS-001 / GAB-001", "Cámara Domo 1P-01". |
| **Ubicación** | Ubicación del equipo/gabinete. | |
| **Descripción del Trabajo** | Detalle del trabajo realizado. | |
| **Estado** | Estado del mantenimiento. | Ej: "Programado", "En Proceso", "Completado", "Cancelado". |
| **Técnico Responsable** | Nombre del técnico o empresa responsable. | Ej: "Técnico Propio", "Oliver Carrasco", "Marco Altamirano", "ConectaSur". |
| **Materiales Utilizados** | Materiales usados. | |
| **Costo Aproximado** | Costo estimado del mantenimiento. | |
| **Equipos/Cámaras Afectadas** | Equipos o cámaras que fueron afectados o intervenidos. | |
| **Tiempo de Ejecución** | Tiempo que tomó el mantenimiento. | |
| **Observaciones** | Notas adicionales. | |

### 8. `Ubicaciones.xlsx`

Catálogo de ubicaciones para mantener la consistencia.

| Columna | Descripción | Notas Importantes |
|:---|:---|:---|
| **ID Ubicación** | Identificador único de la ubicación. | Ej: "UBI-001". |
| **Campus** | Nombre del campus. | |
| **Edificio** | Nombre del edificio. | |
| **Piso/Nivel** | Piso o nivel. | |
| **Zona** | Zona específica dentro del piso/nivel. | Ej: "Pasillo principal", "Sala técnica". |
| **Gabinetes en Ubicación** | IDs de los gabinetes presentes en esta ubicación. | Separar por comas si hay varios. |
| **Cantidad de Cámaras** | Número de cámaras en esta ubicación. | |
| **Observaciones** | Notas relevantes. | |

## Pasos para Completar los Datos

1.  **Comience por `Gabinetes.xlsx` y `Ubicaciones.xlsx`:** Defina todos sus gabinetes y sus ubicaciones precisas. Esto le dará los IDs y nombres para usar en otras planillas.
2.  **Continúe con `Switches.xlsx` y `Equipos_Tecnicos.xlsx`:** Asocie cada switch y NVR/UPS a su `Gabinete Asociado`.
3.  **Luego, `Puertos_Switch.xlsx`:** Detalle qué dispositivo está conectado a cada puerto de cada switch, incluyendo el `NVR Asociado (Puerto)` y `Puerto NVR (Puerto)`.
4.  **Finalmente, `Listadecámaras_modificada.xlsx`:** Utilice la información de los gabinetes, switches y puertos para completar los campos de ubicación y conectividad de cada cámara. Asegúrese de que los `ID Gabinete`, `ID Switch` y `ID NVR` coincidan con los definidos en las otras planillas.
5.  **`Fallas_Actualizada.xlsx` y `Mantenimientos.xlsx`:** Estas planillas se llenarán a medida que ocurran eventos, utilizando los IDs de cámaras, gabinetes, switches y NVRs ya definidos.

Una vez que haya completado estas planillas, el sistema web estará listo para ofrecerle una visión completa y funcional de su infraestructura de cámaras. Si tiene dudas sobre cómo llenar un campo específico, consulte esta guía o el `DOCUMENTACION_CAMBIOS.md`.
