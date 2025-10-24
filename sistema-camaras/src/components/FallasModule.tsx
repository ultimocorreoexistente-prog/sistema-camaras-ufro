export default function FallasModule({ fallas }: any) {
  const fallasPorEstado = {
    abiertas: fallas.filter((f: any) => f.estado === 'Abierta').length,
    enProceso: fallas.filter((f: any) => f.estado === 'En Proceso').length,
    resueltas: fallas.filter((f: any) => f.estado === 'Resuelta').length
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <p className="text-sm text-red-600">Fallas Abiertas</p>
          <p className="text-3xl font-bold text-red-700">{fallasPorEstado.abiertas}</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <p className="text-sm text-yellow-600">En Proceso</p>
          <p className="text-3xl font-bold text-yellow-700">{fallasPorEstado.enProceso}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <p className="text-sm text-green-600">Resueltas</p>
          <p className="text-3xl font-bold text-green-700">{fallasPorEstado.resueltas}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Registro de Fallas</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Fecha</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Tipo</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Cámara</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Ubicación</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Estado</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Prioridad</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {fallas.map((falla: any) => (
                <tr key={falla.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{falla.fecha_reporte}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{falla.tipo}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{falla.camara_afectada}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{falla.ubicacion}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      falla.estado === 'Abierta' ? 'bg-red-100 text-red-800' :
                      falla.estado === 'En Proceso' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {falla.estado}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{falla.prioridad}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
