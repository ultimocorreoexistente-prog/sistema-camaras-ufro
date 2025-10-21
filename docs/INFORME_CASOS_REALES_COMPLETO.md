# Informe Completo de Casos Reales Documentados
## Sistema de Gestión de Cámaras UFRO

**Fecha del informe:** 2025-10-20 21:46:51
**Total de casos documentados:** 5

---

## 📊 Resumen Ejecutivo

- **Total casos documentados:** 5
- **Tiempo total de resolución:** 41.62 horas
- **Promedio de resolución:** 8.32 horas por caso
- **Fallas específicas registradas:** 8

### Tabla Resumen de Casos

| # | Fecha | Caso | Tiempo (h) | Estado |
|---|-------|------|------------|--------|
| 1 | 2024-10-12 | Telas de araña - Bunker... | 1.00 | Resuelto |
| 2 | 2024-10-13 | Mantenimiento UPS Edificio O... | 2.50 | Resuelto |
| 3 | 2024-10-14 | Falla Cable NVR CFT Prat... | 26.50 | Resuelto |
| 4 | 2025-10-16 | Falla Fibra Óptica Bicicletero Principal... | 8.95 | Resuelto |
| 5 | 2025-10-17 | Caída cámaras ZM - Falla Eléctrica... | 2.67 | Resuelto |

---

## 📋 Detalles de Cada Caso

### Caso 1: Telas de araña - Bunker

**📅 Fecha:** 2024-10-12
**⏱️ Tiempo de resolución:** 1.0 horas

#### 📝 Descripción
Cámara Bunker_EX_costado presenta telas de araña que afectan la calidad de imagen

#### 📦 Componentes Involucrados
- Cámara Bunker_EX_costado
- Lente exterior

#### 🔗 Dependencias en Cascada
- Limpieza manual requerida
- Acceso con escalera

#### ✅ Solución Aplicada
Limpieza manual del lente y carcasa exterior

#### 💡 Lecciones Aprendidas
Programar limpieza preventiva trimestral para cámaras exteriores

---

### Caso 2: Mantenimiento UPS Edificio O

**📅 Fecha:** 2024-10-13
**⏱️ Tiempo de resolución:** 2.5 horas

#### 📝 Descripción
Cambio preventivo de 1 batería del UPS APC Smart-UPS SC 1500VA en sala técnica tercer piso Edificio O

#### 📦 Componentes Involucrados
- UPS APC Smart-UPS SC 1500VA
- Batería RBC7 12V 17Ah
- 11 cámaras Edificio O
- 1 cámara PTZ Francisco Salazar vía fibra

#### 🔗 Dependencias en Cascada
- Switch Edificio O
- Enlace fibra óptica
- Gabinete subterráneo Francisco Salazar
- Cámara PTZ remota

#### ✅ Solución Aplicada
Cambio exitoso de batería con sistema funcionando en batería restante

#### 💡 Lecciones Aprendidas
Importancia de tener baterías redundantes para evitar corte total durante mantenimiento. Considerar ventana de mantenimiento para equipos críticos.

---

### Caso 3: Falla Cable NVR CFT Prat

**📅 Fecha:** 2024-10-14
**⏱️ Tiempo de resolución:** 26.5 horas

#### 📝 Descripción
13 cámaras del CFT Prat perdieron conexión simultáneamente por cable suelto entre NVR e internet

#### 📦 Componentes Involucrados
- NVR CFT Prat
- Cable ethernet NVR-Internet
- 13 cámaras CFT Prat
- Router Cisco CFT

#### 📹 Cámaras Afectadas
- **Total:** 13 cámaras
  - cam-cft-1
  - cam-cft-2
  - cam-cft-3
  - cam-cft-4
  - cam-cft-5
  - ... y 8 cámaras más
- **Total:** 13 cámaras
  - cam-cft-1
  - cam-cft-2
  - cam-cft-3
  - cam-cft-4
  - cam-cft-5
  - ... y 8 cámaras más

#### 🔗 Dependencias en Cascada
- Todas las cámaras CFT dependen de un solo NVR
- NVR depende de una sola conexión a internet
- Sin redundancia de conectividad

#### ✅ Solución Aplicada
Reconexión y ajuste del cable ethernet, verificación de todas las conexiones

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Juan Pérez (Personal CFT)
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Juan Pérez (Personal CFT)
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello

#### 💡 Lecciones Aprendidas
Necesidad de implementar redundancia en ubicaciones con múltiples cámaras. Revisar todas las instalaciones de subcontratistas.

---

### Caso 4: Falla Fibra Óptica Bicicletero Principal

**📅 Fecha:** 2025-10-16
**⏱️ Tiempo de resolución:** 8.95 horas

#### 📝 Descripción
Todas las cámaras del Bicicletero Principal perdieron conexión por falla en cable de fibra óptica proveniente del Edificio L (Odontología)

#### 📦 Componentes Involucrados
- Gabinete Bicicletero Principal
- Switch Bicicletero
- Fuente de poder Bicicletero
- Cable fibra óptica Edificio L → Bicicletero
- Todas las cámaras Bicicletero Principal

#### 📹 Cámaras Afectadas
- **Todas las cámaras Bicicletero Principal**
- **Todas las cámaras Bicicletero Principal**
- **Todas las cámaras Bicicletero Principal**
- **Todas las cámaras Bicicletero Principal**

#### 🔗 Dependencias en Cascada
- Dinfo (Sistema Central) → Fibra → Edificio Matemáticas
- Edificio Matemáticas → Fibra → Edificio L (Odontología)
- Edificio L (Odontología) → Fibra → Bicicletero Principal
- Bicicletero Principal: Switch + Fuente → Cámaras

#### ✅ Solución Aplicada
Apertura de gabinete, identificación de cable fibra suelto, reconexión del cable de fibra óptica

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Personal técnico
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello
- **Observaciones:** El Bicicletero Principal depende de enlace de fibra desde Edificio L. Topología: Dinfo → Matemáticas → Odontología → Bicicletero. Gabinete contiene 1 switch + 1 fuente de poder.

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Personal técnico
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello
- **Observaciones:** El Bicicletero Principal depende de enlace de fibra desde Edificio L. Topología: Dinfo → Matemáticas → Odontología → Bicicletero. Gabinete contiene 1 switch + 1 fuente de poder.

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Personal técnico
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello
- **Observaciones:** El Bicicletero Principal depende de enlace de fibra desde Edificio L. Topología: Dinfo → Matemáticas → Odontología → Bicicletero. Gabinete contiene 1 switch + 1 fuente de poder.

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Personal técnico
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello
- **Observaciones:** El Bicicletero Principal depende de enlace de fibra desde Edificio L. Topología: Dinfo → Matemáticas → Odontología → Bicicletero. Gabinete contiene 1 switch + 1 fuente de poder.

#### 💡 Lecciones Aprendidas
Puntos críticos de falla en enlaces de fibra óptica de larga distancia. Necesidad de monitoreo de conectividad de enlaces críticos. Documentar topología completa de red de fibra. El Bicicletero depende de una cadena de 3 enlaces de fibra (Dinfo→Matemáticas→Odontología→Bicicletero).

---

### Caso 5: Caída cámaras ZM - Falla Eléctrica

**📅 Fecha:** 2025-10-17
**⏱️ Tiempo de resolución:** 2.67 horas

#### 📝 Descripción
Caída de 3 cámaras del ZM por falla eléctrica. Automático desconectado en caseta guardia frente a taller

#### 📦 Componentes Involucrados
- ZM-container_Ciclovia
- ZM-Ciclovia a AM
- ZM-Bodega_Ciclovia
- Automático eléctrico caseta guardia

#### 📹 Cámaras Afectadas
- **Total:** 3 cámaras
  - ZM-container_Ciclovia
  - ZM-Ciclovia a AM
  - ZM-Bodega_Ciclovia
- **Total:** 3 cámaras
  - ZM-container_Ciclovia
  - ZM-Ciclovia a AM
  - ZM-Bodega_Ciclovia

#### 🔗 Dependencias en Cascada
- Caseta guardia frente a taller
- Automático ubicado fuera de gabinetes principales
- Zona ZM - Ciclovia

#### ✅ Solución Aplicada
Subir automático en caseta guardia

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Marco Contreras (Encargado Seguridad)
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello
- **Observaciones:** Automático ubicado fuera de los gabinetes principales, en caseta guardia frente a taller. Requiere señalización.

#### 👨‍🔧 Detalles Técnicos
- **Técnico:** Marco Contreras (Encargado Seguridad)
- **Costo de reparación:** $0
- **Prioridad:** Alta
- **Campus:** Andrés Bello
- **Observaciones:** Automático ubicado fuera de los gabinetes principales, en caseta guardia frente a taller. Requiere señalización.

#### 💡 Lecciones Aprendidas
Automáticos eléctricos ubicados en lugares no convencionales requieren señalización y documentación clara. Considerar centralización de protecciones eléctricas.

---

## 📊 Análisis de Tipos de Fallas

| Tipo de Falla | Cantidad | Promedio Horas | Costo Total |
|---------------|----------|----------------|-------------|
| Falla de conectividad | 4 | 8.95h | $0 |
| Falla de alimentación | 2 | 2.67h | $0 |
| Cable suelto | 2 | 26.50h | $0 |

---

## 🚨 Recomendaciones Preventivas

### Basadas en los casos documentados:

1. **Redundancia en enlaces críticos de fibra óptica**
   - El Bicicletero y CFT Prat han presentado fallas por cables sueltos
   - Implementar enlaces redundantes en ubicaciones con múltiples cámaras

2. **Revisión de instalaciones de subcontratistas**
   - Caso CFT Prat evidenció problemas de instalación
   - Auditoría completa de todas las instalaciones externas

3. **Mantenimiento preventivo de UPS**
   - Caso Edificio O: cambio exitoso de baterías
   - Programar cambios preventivos cada 18 meses

4. **Documentación de puntos eléctricos no convencionales**
   - Caso ZM: automático en caseta guardia
   - Señalizar y documentar todas las protecciones eléctricas

5. **Limpieza preventiva de cámaras exteriores**
   - Caso Bunker: telarañas en lente
   - Programa trimestral de limpieza

6. **Monitoreo de conectividad en tiempo real**
   - Múltiples casos de fallas detectadas tardíamente
   - Sistema de alertas automáticas

7. **Topología de red documentada**
   - Caso Bicicletero evidenció cadena de 3 enlaces
   - Mapeo completo de dependencias de fibra óptica


---

## 📝 Información del Documento

- **Base de datos:** sistema_camaras.db
- **Generado:** 2025-10-20 21:46:51
- **Sistema:** Sistema de Gestión de Cámaras UFRO
- **Total casos:** 5
- **Total fallas:** 8
