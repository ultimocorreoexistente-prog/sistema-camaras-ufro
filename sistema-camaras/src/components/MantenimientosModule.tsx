import { Calendar } from 'lucide-react'

interface Mantenimiento {
  id: number
  fecha_programada: string
  tipo: string
  descripcion: string
  estado: string
  equipo_gabinete: string
}

interface MantenimientosModuleProps {
  mantenimientos: Mantenimiento[]
}

export default function MantenimientosModule({ mantenimientos }: MantenimientosModuleProps) {
  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-xl font-bold text-slate-900 mb-4">Mantenimientos Programados</h2>
        <p className="text-slate-600">Total: {mantenimientos.length}</p>
      </div>

      <div className="space-y-3">
        {mantenimientos.map(mant => (
          <div key={mant.id} className="bg-white p-4 rounded-lg shadow-md">
            <div className="flex items-start gap-3">
              <Calendar className="h-6 w-6 text-blue-600 mt-1" />
              <div className="flex-1">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-slate-900">{mant.tipo}</h3>
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    mant.estado === 'Programado' ? 'bg-blue-100 text-blue-800' : 
                    mant.estado === 'Completado' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {mant.estado}
                  </span>
                </div>
                <p className="text-sm text-slate-600 mb-2">{mant.descripcion}</p>
                <div className="flex gap-4 text-xs text-slate-500">
                  <span>Equipo: {mant.equipo_gabinete}</span>
                  <span>Fecha: {new Date(mant.fecha_programada).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
