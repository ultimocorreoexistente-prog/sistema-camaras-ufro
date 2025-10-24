export default function SwitchesModule({ switches }: any) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Gestión de Switches</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {switches.map((sw: any) => (
          <div key={sw.id} className="border border-slate-200 rounded-lg p-4">
            <h3 className="font-semibold text-lg mb-2">{sw.nombre}</h3>
            <div className="space-y-1 text-sm">
              <p><span className="text-slate-600">Código:</span> {sw.codigo}</p>
              <p><span className="text-slate-600">Marca:</span> {sw.marca}</p>
              <p><span className="text-slate-600">Modelo:</span> {sw.modelo}</p>
              <p><span className="text-slate-600">Puertos Totales:</span> {sw.puertos_totales}</p>
              <p><span className="text-slate-600">Puertos Usados:</span> {sw.puertos_usados}</p>
              <p><span className="text-slate-600">Puertos Disponibles:</span> {sw.puertos_disponibles}</p>
              <div className="mt-2">
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${(sw.puertos_usados / sw.puertos_totales) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
