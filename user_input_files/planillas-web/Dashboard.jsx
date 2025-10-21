import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Camera, Server, HardDrive, AlertTriangle, CheckCircle, XCircle } from 'lucide-react'

export default function Dashboard() {
  // Datos de ejemplo
  const stats = {
    totalCamaras: 45,
    camarasFuncionando: 42,
    camarasAveriadas: 3,
    totalGabinetes: 12,
    totalSwitches: 15,
    fallasAbiertas: 2,
    mantenimientosPendientes: 3
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
          Dashboard General
        </h2>
        <p className="text-slate-600 dark:text-slate-400">
          Vista general del sistema de cámaras de seguridad UFRO
        </p>
      </div>

      {/* Estadísticas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-400">
              Total Cámaras
            </CardTitle>
            <Camera className="h-5 w-5 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">
              {stats.totalCamaras}
            </div>
            <div className="flex items-center gap-2 mt-2">
              <Badge variant="outline" className="text-green-600 border-green-600">
                <CheckCircle className="h-3 w-3 mr-1" />
                {stats.camarasFuncionando} funcionando
              </Badge>
              <Badge variant="outline" className="text-red-600 border-red-600">
                <XCircle className="h-3 w-3 mr-1" />
                {stats.camarasAveriadas} averiadas
              </Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-400">
              Gabinetes/Racks
            </CardTitle>
            <Server className="h-5 w-5 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">
              {stats.totalGabinetes}
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-2">
              Distribuidos en campus
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-400">
              Switches Activos
            </CardTitle>
            <HardDrive className="h-5 w-5 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">
              {stats.totalSwitches}
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-2">
              Conectividad de red
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-400">
              Fallas Abiertas
            </CardTitle>
            <AlertTriangle className="h-5 w-5 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">
              {stats.fallasAbiertas}
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-2">
              Requieren atención
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Alertas y notificaciones */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Alertas Recientes</CardTitle>
            <CardDescription>Últimas incidencias reportadas</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start gap-3 p-3 bg-red-50 dark:bg-red-950/20 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-red-600 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-slate-900 dark:text-white">
                    Cámara PTZ sin conexión
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Edificio O - 3er Piso • Hace 2 horas
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3 p-3 bg-orange-50 dark:bg-orange-950/20 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-orange-600 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-slate-900 dark:text-white">
                    Switch con alta temperatura
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Gabinete Subterráneo • Hace 5 horas
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Mantenimientos Próximos</CardTitle>
            <CardDescription>Actividades programadas</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start gap-3 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                <CheckCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-slate-900 dark:text-white">
                    Revisión de UPS
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Edificio O - Rack 3P • 15/10/2025
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                <CheckCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-slate-900 dark:text-white">
                    Limpieza de cámaras exteriores
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Campus Principal • 20/10/2025
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Estado por ubicación */}
      <Card>
        <CardHeader>
          <CardTitle>Estado por Ubicación</CardTitle>
          <CardDescription>Distribución de cámaras por edificio</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { edificio: 'Edificio O', total: 11, funcionando: 11, averiadas: 0 },
              { edificio: 'Edificio 2030', total: 8, funcionando: 7, averiadas: 1 },
              { edificio: 'Auditorium', total: 6, funcionando: 6, averiadas: 0 },
              { edificio: 'Francisco Salazar', total: 5, funcionando: 4, averiadas: 1 },
            ].map((loc, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
                <div className="flex-1">
                  <p className="font-medium text-slate-900 dark:text-white">{loc.edificio}</p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {loc.total} cámaras totales
                  </p>
                </div>
                <div className="flex gap-2">
                  <Badge variant="outline" className="text-green-600 border-green-600">
                    {loc.funcionando} OK
                  </Badge>
                  {loc.averiadas > 0 && (
                    <Badge variant="outline" className="text-red-600 border-red-600">
                      {loc.averiadas} Falla
                    </Badge>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

