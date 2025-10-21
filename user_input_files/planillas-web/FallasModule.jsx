import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { AlertTriangle, Plus, Cable, Camera, Flame, Hammer, Zap } from 'lucide-react'

export default function FallasModule() {
  const fallas = [
    {
      id: 'F-001',
      fecha: '12/10/2025',
      tipo: 'Cámara que deja de funcionar',
      equipo: 'Cámara Domo 2P-03',
      gabinete: 'GAB-001',
      switch: 'SW-001',
      puerto: '5',
      descripcion: 'Cámara sin imagen, no responde a ping',
      impacto: '1 cámara sin servicio',
      estado: 'En proceso',
      tecnico: 'Técnico Propio',
      prioridad: 'Media'
    },
    {
      id: 'F-002',
      fecha: '10/10/2025',
      tipo: 'Switch que se quema',
      equipo: 'Switch SW-003',
      gabinete: 'GAB-005',
      switch: 'SW-003',
      puerto: 'Todos',
      descripcion: 'Switch completamente inoperativo, posible sobrecarga',
      impacto: '8 cámaras sin servicio',
      estado: 'Reportada',
      tecnico: 'Oliver Carrasco',
      prioridad: 'Alta'
    },
    {
      id: 'F-003',
      fecha: '12/10/2025',
      tipo: 'Telas de araña',
      equipo: 'Bunker_EX_costado',
      gabinete: 'GAB-003',
      switch: 'SW-004',
      puerto: '1',
      descripcion: 'Telas de araña en lente, se visualiza con visión nocturna',
      impacto: 'Visibilidad reducida en visión nocturna',
      estado: 'Reportada',
      tecnico: 'Marco Altamirano',
      prioridad: 'Baja'
    },
    {
      id: 'F-004',
      fecha: '12/10/2025',
      tipo: 'Mica rallada/dañada',
      equipo: 'ED-O_3P_Salida_Emergencia',
      gabinete: 'GAB-001',
      switch: 'SW-001',
      puerto: '11',
      descripcion: 'Mica rallada, no se visualiza imagen con visión nocturna',
      impacto: 'No se visualiza con visión nocturna',
      estado: 'Reportada',
      tecnico: 'ConectaSur',
      prioridad: 'Media'
    },
  ]

  const tiposFallas = [
    { nombre: 'Cables rotos', icon: Cable, color: 'text-orange-600' },
    { nombre: 'Cámaras que se queman', icon: Flame, color: 'text-red-600' },
    { nombre: 'Cámaras vandalizadas', icon: Hammer, color: 'text-purple-600' },
    { nombre: 'Cámaras que dejan de funcionar', icon: Camera, color: 'text-blue-600' },
    { nombre: 'Fuentes que se queman', icon: Zap, color: 'text-yellow-600' },
    { nombre: 'Switches que se queman', icon: Flame, color: 'text-red-600' },
    { nombre: 'Postes que se dañan', icon: AlertTriangle, color: 'text-orange-600' },
    { nombre: 'UPS averiados', icon: AlertTriangle, color: 'text-red-600' },
    { nombre: 'NVR averiados', icon: AlertTriangle, color: 'text-purple-600' },
    { nombre: 'Telas de araña', icon: Camera, color: 'text-green-600' },
    { nombre: 'Mica rallada/dañada', icon: Camera, color: 'text-red-600' },
    { nombre: 'Mancha en lente', icon: Camera, color: 'text-yellow-600' },
    { nombre: 'Intermitencia', icon: AlertTriangle, color: 'text-orange-600' },
    { nombre: 'Empañada/Humedad', icon: Camera, color: 'text-blue-600' },
    { nombre: 'Franjas negras visión nocturna', icon: Camera, color: 'text-purple-600' },
  ]

  const getPrioridadBadge = (prioridad) => {
    const variants = {
      'Alta': 'destructive',
      'Media': 'secondary',
      'Baja': 'outline'
    }
    return <Badge variant={variants[prioridad]}>{prioridad}</Badge>
  }

  const getEstadoBadge = (estado) => {
    const colors = {
      'Reportada': 'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300',
      'En proceso': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-950 dark:text-yellow-300',
      'Resuelta': 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300',
      'Cerrada': 'bg-slate-100 text-slate-800 dark:bg-slate-950 dark:text-slate-300'
    }
    return <Badge className={colors[estado]}>{estado}</Badge>
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-6 w-6" />
                Gestión de Fallas
              </CardTitle>
              <CardDescription>
                Registro y seguimiento de incidencias del sistema
              </CardDescription>
            </div>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Reportar Falla
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {/* Fallas activas */}
          <div className="space-y-4 mb-6">
            {fallas.map((falla) => (
              <Card key={falla.id} className="border-l-4 border-l-red-500">
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3 flex-wrap">
                      <code className="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded text-sm font-mono">
                        {falla.id}
                      </code>
                      {getPrioridadBadge(falla.prioridad)}
                      {getEstadoBadge(falla.estado)}
                    </div>
                    <span className="text-sm text-slate-500">{falla.fecha}</span>
                  </div>

                  <h3 className="font-semibold text-lg text-slate-900 dark:text-white mb-2">
                    {falla.tipo}
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Equipo afectado</p>
                      <p className="font-medium text-slate-900 dark:text-white">{falla.equipo}</p>
                    </div>
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Conexión</p>
                      <p className="font-medium text-slate-900 dark:text-white">
                        {falla.gabinete} → {falla.switch} → Puerto {falla.puerto}
                      </p>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 dark:bg-slate-900 rounded-lg mb-4">
                    <p className="text-sm font-medium text-slate-900 dark:text-white mb-1">Descripción</p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">{falla.descripcion}</p>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Impacto</p>
                      <p className="text-sm font-medium text-red-600">{falla.impacto}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-slate-600 dark:text-slate-400">Técnico asignado</p>
                      <p className="text-sm font-medium text-slate-900 dark:text-white">
                        {falla.tecnico || 'Sin asignar'}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-2 mt-4 pt-4 border-t">
                    <Button variant="outline" size="sm">Ver Detalles</Button>
                    <Button variant="outline" size="sm">Actualizar Estado</Button>
                    <Button variant="outline" size="sm">Resolver</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Tipos de fallas */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Tipos de Fallas del Sistema</CardTitle>
              <CardDescription>
                Categorías de incidencias que se pueden presentar
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {tiposFallas.map((tipo, idx) => {
                  const Icon = tipo.icon
                  return (
                    <div
                      key={idx}
                      className="flex items-center gap-3 p-3 bg-slate-50 dark:bg-slate-900 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                    >
                      <Icon className={`h-5 w-5 ${tipo.color}`} />
                      <span className="text-sm font-medium text-slate-900 dark:text-white">
                        {tipo.nombre}
                      </span>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* Información importante */}
          <div className="mt-6 p-4 bg-orange-50 dark:bg-orange-950/20 rounded-lg">
            <div className="flex items-start gap-3">
              <AlertTriangle className="h-5 w-5 text-orange-600 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-orange-900 dark:text-orange-100 mb-1">
                  Importancia del Registro de Fallas
                </p>
                <p className="text-sm text-orange-800 dark:text-orange-200">
                  Registrar cada falla con su relación a gabinete, switch y puerto permite identificar 
                  patrones de problemas y realizar troubleshooting más eficiente. Por ejemplo, si un 
                  switch se quema, todas las cámaras conectadas a ese switch quedan sin servicio.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

