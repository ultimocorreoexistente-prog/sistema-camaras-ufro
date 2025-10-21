import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Server, MapPin, HardDrive, Battery, Network, Plus } from 'lucide-react'

export default function GabinetesModule() {
  const gabinetes = [
    {
      id: 'GAB-001',
      nombre: 'Rack Edificio O - 3P',
      tipo: 'Interior dependencia',
      ubicacion: 'Edificio O - 3er Piso - Sala técnica',
      estado: 'Funcionando',
      ultimaRevision: '13/10/2025',
      equipos: {
        ups: 'UPS-001 (APC Smart-UPS 1500)',
        switch: 'SW-001 (24 puertos)',
        nvr: 'No'
      },
      fibraOptica: true,
      camarasConectadas: 11,
      observaciones: 'Cambio de batería UPS realizado el 13/10/2025'
    },
    {
      id: 'GAB-002',
      nombre: 'Gabinete Subterráneo Francisco Salazar',
      tipo: 'Subterráneo',
      ubicacion: 'Francisco Salazar - Subterráneo - Acceso norte',
      estado: 'Funcionando',
      ultimaRevision: '',
      equipos: {
        ups: 'No',
        switch: 'SW-002 (8 puertos)',
        nvr: 'No'
      },
      fibraOptica: true,
      camarasConectadas: 1,
      observaciones: 'Requiere revisión de humedad'
    },
  ]

  const getTipoBadge = (tipo) => {
    const colors = {
      'Subterráneo': 'bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300',
      'Interior dependencia': 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300',
      'Exterior dependencia': 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300',
      'Poste': 'bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300'
    }
    return (
      <Badge variant="outline" className={colors[tipo] || ''}>
        {tipo}
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
                <Server className="h-6 w-6" />
                Gestión de Gabinetes y Racks
              </CardTitle>
              <CardDescription>
                Administra los gabinetes que contienen los equipos de red y alimentación
              </CardDescription>
            </div>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Nuevo Gabinete
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {gabinetes.map((gabinete) => (
              <Card key={gabinete.id} className="border-2 hover:border-blue-300 dark:hover:border-blue-700 transition-colors">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <code className="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded text-sm font-mono">
                          {gabinete.id}
                        </code>
                        {getTipoBadge(gabinete.tipo)}
                      </div>
                      <CardTitle className="text-lg">{gabinete.nombre}</CardTitle>
                    </div>
                    <Badge variant={gabinete.estado === 'Funcionando' ? 'default' : 'destructive'}>
                      {gabinete.estado}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Ubicación */}
                  <div className="flex items-start gap-3 p-3 bg-slate-50 dark:bg-slate-900 rounded-lg">
                    <MapPin className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-sm font-medium text-slate-900 dark:text-white">Ubicación</p>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{gabinete.ubicacion}</p>
                    </div>
                  </div>

                  {/* Equipamiento */}
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-slate-900 dark:text-white">Equipamiento</p>
                    
                    <div className="flex items-center gap-2 text-sm">
                      <Battery className="h-4 w-4 text-green-600" />
                      <span className="text-slate-600 dark:text-slate-400">UPS:</span>
                      <span className="font-medium text-slate-900 dark:text-white">
                        {gabinete.equipos.ups || 'No instalado'}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 text-sm">
                      <HardDrive className="h-4 w-4 text-blue-600" />
                      <span className="text-slate-600 dark:text-slate-400">Switch:</span>
                      <span className="font-medium text-slate-900 dark:text-white">
                        {gabinete.equipos.switch || 'No instalado'}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 text-sm">
                      <Server className="h-4 w-4 text-purple-600" />
                      <span className="text-slate-600 dark:text-slate-400">NVR/DVR:</span>
                      <span className="font-medium text-slate-900 dark:text-white">
                        {gabinete.equipos.nvr || 'No instalado'}
                      </span>
                    </div>

                    {gabinete.fibraOptica && (
                      <div className="flex items-center gap-2 text-sm">
                        <Network className="h-4 w-4 text-orange-600" />
                        <Badge variant="secondary" className="text-xs">
                          Conexión Fibra Óptica
                        </Badge>
                      </div>
                    )}
                  </div>

                  {/* Estadísticas */}
                  <div className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                    <div>
                      <p className="text-sm text-slate-600 dark:text-slate-400">Cámaras conectadas</p>
                      <p className="text-2xl font-bold text-blue-600">{gabinete.camarasConectadas}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-slate-600 dark:text-slate-400">Última revisión</p>
                      <p className="text-sm font-medium text-slate-900 dark:text-white">
                        {gabinete.ultimaRevision || 'Sin registro'}
                      </p>
                    </div>
                  </div>

                  {/* Observaciones */}
                  {gabinete.observaciones && (
                    <div className="p-3 bg-yellow-50 dark:bg-yellow-950/20 rounded-lg">
                      <p className="text-sm font-medium text-yellow-900 dark:text-yellow-100 mb-1">
                        Observaciones
                      </p>
                      <p className="text-sm text-yellow-800 dark:text-yellow-200">
                        {gabinete.observaciones}
                      </p>
                    </div>
                  )}

                  {/* Acciones */}
                  <div className="flex gap-2 pt-2">
                    <Button variant="outline" size="sm" className="flex-1">
                      Ver Detalles
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1">
                      Historial
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Leyenda de tipos */}
          <div className="mt-6 p-4 bg-slate-50 dark:bg-slate-900 rounded-lg">
            <p className="text-sm font-medium text-slate-900 dark:text-white mb-3">
              Tipos de Ubicación de Gabinetes
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { tipo: 'Subterráneo', desc: 'Cámaras en ubicaciones bajo tierra' },
                { tipo: 'Interior dependencia', desc: 'Dentro de edificios' },
                { tipo: 'Exterior dependencia', desc: 'Fuera pero cerca de edificios' },
                { tipo: 'Poste', desc: 'Instalaciones en postes' }
              ].map((item, idx) => (
                <div key={idx} className="text-sm">
                  {getTipoBadge(item.tipo)}
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

