interface Gabinete {
  id: number
  codigo: string
  nombre: string
  campus: string
  edificio: string
  ubicacion: string
  estado: string
}

interface GabinetesModuleProps {
  gabinetes: Gabinete[]
}

export default function GabinetesModule({ gabinetes }: GabinetesModuleProps) {
  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-xl font-bold text-slate-900 mb-4">Gestión de Gabinetes</h2>
        <p className="text-slate-600">Total de gabinetes: {gabinetes.length}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {gabinetes.map(gabinete => (
          <div key={gabinete.id} className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-slate-900 mb-2">{gabinete.codigo}</h3>
            <div className="space-y-2 text-sm">
              <p className="text-slate-600"><strong>Nombre:</strong> {gabinete.nombre}</p>
              <p className="text-slate-600"><strong>Campus:</strong> {gabinete.campus}</p>
              <p className="text-slate-600"><strong>Edificio:</strong> {gabinete.edificio}</p>
              <p className="text-slate-600"><strong>Ubicación:</strong> {gabinete.ubicacion}</p>
              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                gabinete.estado === 'Operativo' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {gabinete.estado}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
