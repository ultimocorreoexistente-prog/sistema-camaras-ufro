import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Wrench, Plus, Calendar, CheckCircle, Clock } from 'lucide-react'

export default function MantenimientosModule() {
  const mantenimientos = [
    {
      id: 'MNT-001',
      fechaProgramada: '13/10/2025',
      fechaRealizacion: '13/10/2025',
      tipo: 'Correctivo',
      categoria: 'Cambio de batería',
      equipo: 'UPS-001 / GAB-001',
      ubicacion: 'Edificio O - 3er Piso',
      descripcion: 'Cambio de 1 batería de UPS',
      estado: 'Completado',
      tecnico: 'Técnico Propio',
      materiales: '1 Batería 12V 9Ah',
      equiposAfectados: '10 cámaras domo + 1 PTZ temporalmente sin respaldo',
      tiempo: '30 minutos',
      observaciones: 'Mantenimiento exitoso, sistema operando normalmente'
    },
    {
      id: 'MNT-002',
      fechaProgramada: '15/10/2025',
      fechaRealizacion: '',
      tipo: 'Preventivo',
      categoria: 'Revisión de equipos',
      equipo: 'Todos los UPS',
      ubicacion: 'Campus Principal',
      descripcion: 'Revisión general de estado de UPS y medición de voltaje de baterías',
      estado: 'Programado',
      tecnico: 'Oliver Carrasco',
      materiales: 'Multímetro, registro de mediciones',
      equiposAfectados: 'Ninguno (revisión sin interrupción)',
      tiempo: '2 horas',
      observaciones: ''
    },
    {
      id: 'MNT-003',
      fechaProgramada: '20/10/2025',
      fechaRealizacion: '',
      tipo: 'Preventivo',
      categoria: 'Limpieza de cámaras',
      equipo: 'Cámaras exteriores',
      ubicacion: 'Todos los edificios',
      descripcion: 'Limpieza de lentes y carcasas de cámaras exteriores',
      estado: 'Programado',
      tecnico: 'Marco Altamirano',
      materiales: 'Paños de microfibra, limpiador de lentes',
      equiposAfectados: 'Ninguno',
      tiempo: '3 horas',
      observaciones: ''
    },
    {
      id: 'MNT-004',
      fechaProgramada: '25/10/2025',
      fechaRealizacion: '',
      tipo: 'Correctivo',
      categoria: 'Reemplazo de cámara',
      equipo: 'Cámara PTZ Francisco Salazar',
      ubicacion: 'Francisco Salazar - Subterráneo',
      descripcion: 'Reemplazo de cámara PTZ por vandalismo',
      estado: 'Programado',
      tecnico: 'ConectaSur',
      materiales: 'Cámara PTZ nueva, herramientas de instalación',
      equiposAfectados: 'Cámara PTZ Francisco Salazar',
      tiempo: '4 horas',
      observaciones: 'Coordinar con empresa subcontratista'
    },
  ]

  const getTipoBadge = (tipo) => {
    const colors = {
      'Preventivo': 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300',
      'Correctivo': 'bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300',
      'Predictivo': 'bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300'
    }
    return <Badge className={colors[tipo]}>{tipo}</Badge>
  }

  const getEstadoBadge = (estado) => {
    const variants = {
      'Programado': 'secondary',
      'En proceso': 'default',
      'Completado': 'outline',
      'Cancelado': 'destructive'
    }
    const icons = {
      'Programado': <Clock className="h-3 w-3 mr-1" />,
      'En proceso': <Wrench className="h-3 w-3 mr-1" />,
      'Completado': <CheckCircle className="h-3 w-3 mr-1" />,
      'Cancelado': null
    }
    return (
      <Badge variant={variants[estado]}>
        {icons[estado]}
        {estado}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Wrench className="h-6 w-6" />
                Gestión de Mantenimientos
              </CardTitle>
              <CardDescription>
                Programa y registra mantenimientos preventivos, correctivos y predictivos
              </CardDescription>
            </div>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Programar Mantenimiento
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {mantenimientos.map((mant) => (
              <Card
                key={mant.id}
                className={`border-l-4 ${
                  mant.estado === 'Completado'
                    ? 'border-l-green-500'
                    : mant.estado === 'En proceso'
                    ? 'border-l-blue-500'
                    : 'border-l-orange-500'
                }`}
              >
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3 flex-wrap">
                      <code className="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded text-sm font-mono">
                        {mant.id}
                      </code>
                      {getTipoBadge(mant.tipo)}
                      {getEstadoBadge(mant.estado)}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                      <Calendar className="h-4 w-4" />
                      {mant.fechaProgramada}
                    </div>
                  </div>

                  <h3 className="font-semibold text-lg text-slate-900 dark:text-white mb-2">
                    {mant.categoria}
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Equipo/Gabinete</p>
                      <p className="font-medium text-slate-900 dark:text-white">{mant.equipo}</p>
                    </div>
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Ubicación</p>
                      <p className="font-medium text-slate-900 dark:text-white">{mant.ubicacion}</p>
                    </div>
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Tiempo estimado</p>
                      <p className="font-medium text-slate-900 dark:text-white">{mant.tiempo}</p>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 dark:bg-slate-900 rounded-lg mb-4">
                    <p className="text-sm font-medium text-slate-900 dark:text-white mb-1">
                      Descripción del Trabajo
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">{mant.descripcion}</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                      <p className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-1">
                        Materiales Utilizados
                      </p>
                      <p className="text-sm text-blue-800 dark:text-blue-200">{mant.materiales}</p>
                    </div>
                    <div className="p-3 bg-orange-50 dark:bg-orange-950/20 rounded-lg">
                      <p className="text-sm font-medium text-orange-900 dark:text-orange-100 mb-1">
                        Equipos/Cámaras Afectadas
                      </p>
                      <p className="text-sm text-orange-800 dark:text-orange-200">
                        {mant.equiposAfectadas}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pb-4 border-b">
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Técnico responsable</p>
                      <p className="text-sm font-medium text-slate-900 dark:text-white">
                        {mant.tecnico}
                      </p>
                    </div>
                    {mant.fechaRealizacion && (
                      <div className="text-right">
                        <p className="text-sm text-slate-600 dark:text-slate-400">Fecha de realización</p>
                        <p className="text-sm font-medium text-green-600">{mant.fechaRealizacion}</p>
                      </div>
                    )}
                  </div>

                  {mant.observaciones && (
                    <div className="mt-4 p-3 bg-green-50 dark:bg-green-950/20 rounded-lg">
                      <p className="text-sm font-medium text-green-900 dark:text-green-100 mb-1">
                        Observaciones
                      </p>
                      <p className="text-sm text-green-800 dark:text-green-200">
                        {mant.observaciones}
                      </p>
                    </div>
                  )}

                  <div className="flex gap-2 mt-4">
                    <Button variant="outline" size="sm">Ver Detalles</Button>
                    {mant.estado !== 'Completado' && (
                      <>
                        <Button variant="outline" size="sm">Actualizar Estado</Button>
                        <Button variant="outline" size="sm">Marcar Completado</Button>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Caso real destacado */}
          <Card className="mt-6 bg-gradient-to-r from-blue-50 to-green-50 dark:from-blue-950/20 dark:to-green-950/20">
            <CardHeader>
              <CardTitle className="text-lg">Caso Real: Mantenimiento 13/10/2025</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-sm">
                <p className="text-slate-900 dark:text-white">
                  <strong>Ubicación:</strong> Edificio O - 3er Piso (Sala técnica)
                </p>
                <p className="text-slate-900 dark:text-white">
                  <strong>Gabinete:</strong> GAB-001 (Rack Edificio O - 3P)
                </p>
                <p className="text-slate-900 dark:text-white">
                  <strong>Equipo:</strong> UPS-001 (APC Smart-UPS 1500)
                </p>
                <p className="text-slate-900 dark:text-white">
                  <strong>Acción:</strong> Cambio de 1 batería 12V 9Ah
                </p>
                <p className="text-slate-900 dark:text-white">
                  <strong>Switch afectado:</strong> SW-001 (24 puertos)
                </p>
                <p className="text-slate-900 dark:text-white">
                  <strong>Cámaras temporalmente sin respaldo:</strong> 10 cámaras domo (3 en 1P, 2 en 2P, 3 en 3P, 2 en 4P) + 1 PTZ exterior 3P
                </p>
                <p className="text-slate-900 dark:text-white">
                  <strong>Conexión adicional:</strong> Enlace por fibra óptica a gabinete subterráneo (Cámara PTZ Francisco Salazar)
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Información importante */}
          <div className="mt-6 p-4 bg-purple-50 dark:bg-purple-950/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Wrench className="h-5 w-5 text-purple-600 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-purple-900 dark:text-purple-100 mb-1">
                  Importancia del Registro de Mantenimientos
                </p>
                <p className="text-sm text-purple-800 dark:text-purple-200">
                  Registrar cada mantenimiento con su ubicación, equipos afectados y materiales utilizados 
                  permite llevar un historial completo. Esto es especialmente importante para UPS, donde 
                  saber cuándo se cambiaron las baterías ayuda a programar futuros mantenimientos preventivos.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

