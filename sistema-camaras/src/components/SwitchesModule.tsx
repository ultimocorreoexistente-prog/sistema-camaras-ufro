interface Switch {
  id: number
  codigo: string
  nombre: string
  marca: string
  puertos_totales: number
  puertos_usados: number
  puertos_disponibles: number
  estado: string
}

interface SwitchesModuleProps {
  switches: Switch[]
}

export default function SwitchesModule({ switches }: SwitchesModuleProps) {
  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-xl font-bold text-slate-900 mb-4">Switches de Red</h2>
        <p className="text-slate-600">Total de switches: {switches.length}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {switches.map(sw => (
          <div key={sw.id} className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-slate-900 mb-3">{sw.codigo}</h3>
            <div className="space-y-2 text-sm mb-4">
              <p className="text-slate-600"><strong>Modelo:</strong> {sw.nombre}</p>
              <p className="text-slate-600"><strong>Marca:</strong> {sw.marca}</p>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-600">Puertos Usados</span>
                <span className="font-medium">{sw.puertos_usados} / {sw.puertos_totales}</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${(sw.puertos_usados / sw.puertos_totales) * 100}%` }}
                ></div>
              </div>
              <p className="text-xs text-slate-600">{sw.puertos_disponibles} puertos disponibles</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
