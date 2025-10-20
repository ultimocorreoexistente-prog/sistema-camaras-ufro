import { AlertCircle } from 'lucide-react'

interface Falla {
  id: number
  fecha_reporte: string
  tipo: string
  descripcion: string
  estado: string
  prioridad: string
  camara_afectada: string
}

interface FallasModuleProps {
  fallas: Falla[]
}

export default function FallasModule({ fallas }: FallasModuleProps) {
  const fallasAbiertas = fallas.filter(f => f.estado === 'Abierta')

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-xl font-bold text-slate-900 mb-4">Gestión de Fallas</h2>
        <div className="flex gap-4">
          <div className="text-sm">
            <span className="text-slate-600">Total: </span>
            <span className="font-bold">{fallas.length}</span>
          </div>
          <div className="text-sm">
            <span className="text-slate-600">Abiertas: </span>
            <span className="font-bold text-red-600">{fallasAbiertas.length}</span>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {fallas.map(falla => (
          <div key={falla.id} className="bg-white p-4 rounded-lg shadow-md">
            <div className="flex items-start gap-3">
              <AlertCircle className={`h-6 w-6 mt-1 ${
                falla.prioridad === 'Alta' ? 'text-red-600' : 
                falla.prioridad === 'Media' ? 'text-orange-600' : 'text-yellow-600'
              }`} />
              <div className="flex-1">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-slate-900">{falla.tipo}</h3>
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    falla.estado === 'Abierta' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                  }`}>
                    {falla.estado}
                  </span>
                </div>
                <p className="text-sm text-slate-600 mb-2">{falla.descripcion}</p>
                <div className="flex gap-4 text-xs text-slate-500">
                  <span>Cámara: {falla.camara_afectada}</span>
                  <span>Prioridad: {falla.prioridad}</span>
                  <span>Fecha: {new Date(falla.fecha_reporte).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
