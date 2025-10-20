export default function MantenimientosModule({ mantenimientos }: any) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Gestión de Mantenimientos</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Fecha</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Tipo</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Equipo</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Técnico</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Estado</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {mantenimientos.map((mant: any) => (
              <tr key={mant.id} className="hover:bg-slate-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm">{mant.fecha_programada}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{mant.tipo}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{mant.equipo_gabinete}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{mant.tecnico_responsable}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    mant.estado === 'Programado' ? 'bg-blue-100 text-blue-800' :
                    mant.estado === 'Completado' ? 'bg-green-100 text-green-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {mant.estado}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
