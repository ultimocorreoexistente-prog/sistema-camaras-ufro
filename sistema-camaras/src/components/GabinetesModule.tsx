export default function GabinetesModule({ gabinetes }: any) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Gestión de Gabinetes</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Código</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Nombre</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Campus</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Edificio</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Estado</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {gabinetes.map((gab: any) => (
              <tr key={gab.id} className="hover:bg-slate-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{gab.codigo}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{gab.nombre}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{gab.campus}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{gab.edificio}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{gab.estado}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
