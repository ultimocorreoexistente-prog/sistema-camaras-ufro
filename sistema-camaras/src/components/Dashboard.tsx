import { Camera, AlertCircle, Wrench, Server } from 'lucide-react'

interface DashboardProps {
  data: any
}

export default function Dashboard({ data }: DashboardProps) {
  const stats = data.estadisticas

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-600">Total Cámaras</p>
              <p className="text-3xl font-bold text-slate-900">{stats?.total_camaras || 0}</p>
            </div>
            <Camera className="h-12 w-12 text-blue-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-600">Cámaras Activas</p>
              <p className="text-3xl font-bold text-green-600">{stats?.camaras_activas || 0}</p>
            </div>
            <Camera className="h-12 w-12 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-600">Fallas Pendientes</p>
              <p className="text-3xl font-bold text-red-600">{stats?.fallas_pendientes || 0}</p>
            </div>
            <AlertCircle className="h-12 w-12 text-red-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-600">Mantenimientos</p>
              <p className="text-3xl font-bold text-orange-600">{stats?.mantenimientos_programados || 0}</p>
            </div>
            <Wrench className="h-12 w-12 text-orange-600" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Resumen del Sistema</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded">
              <span className="text-slate-700">Total Gabinetes</span>
              <span className="font-bold text-blue-600">{stats?.total_gabinetes || 0}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded">
              <span className="text-slate-700">Total Switches</span>
              <span className="font-bold text-blue-600">{stats?.total_switches || 0}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded">
              <span className="text-slate-700">Cámaras Inactivas</span>
              <span className="font-bold text-red-600">{stats?.camaras_inactivas || 0}</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Estado del Sistema</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm text-slate-600">Operatividad</span>
                <span className="text-sm font-medium">
                  {stats?.total_camaras > 0 
                    ? Math.round((stats.camaras_activas / stats.total_camaras) * 100) 
                    : 0}%
                </span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ 
                    width: `${stats?.total_camaras > 0 
                      ? (stats.camaras_activas / stats.total_camaras) * 100 
                      : 0}%` 
                  }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
