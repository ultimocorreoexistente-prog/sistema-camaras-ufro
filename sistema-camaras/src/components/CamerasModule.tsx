import { useState } from 'react'
import { Search, Filter } from 'lucide-react'

interface Camera {
  id: number
  codigo: string
  nombre: string
  campus: string
  edificio: string
  estado: string
  ip: string
  marca: string
  ubicacion: string
}

interface CamerasModuleProps {
  camaras: Camera[]
}

export default function CamerasModule({ camaras }: CamerasModuleProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterCampus, setFilterCampus] = useState('')
  const [filterEstado, setFilterEstado] = useState('')

  const filteredCamaras = camaras.filter(cam => {
    const matchesSearch = cam.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         cam.codigo?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCampus = !filterCampus || cam.campus === filterCampus
    const matchesEstado = !filterEstado || cam.estado === filterEstado
    return matchesSearch && matchesCampus && matchesEstado
  })

  const campusList = [...new Set(camaras.map(c => c.campus).filter(Boolean))]
  const estadosList = [...new Set(camaras.map(c => c.estado).filter(Boolean))]

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Gestión de Cámaras</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
            <input
              type="text"
              placeholder="Buscar por nombre o código..."
              className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select
            className="px-4 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={filterCampus}
            onChange={(e) => setFilterCampus(e.target.value)}
          >
            <option value="">Todos los Campus</option>
            {campusList.map(campus => (
              <option key={campus} value={campus}>{campus}</option>
            ))}
          </select>

          <select
            className="px-4 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={filterEstado}
            onChange={(e) => setFilterEstado(e.target.value)}
          >
            <option value="">Todos los Estados</option>
            {estadosList.map(estado => (
              <option key={estado} value={estado}>{estado}</option>
            ))}
          </select>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Código</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Nombre</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Campus</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Edificio</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">IP</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Estado</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {filteredCamaras.map((camara) => (
                <tr key={camara.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{camara.codigo}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{camara.nombre}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{camara.campus}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{camara.edificio}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{camara.ip}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      camara.estado === 'Operativa' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {camara.estado}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="mt-4 text-sm text-slate-600">
          Mostrando {filteredCamaras.length} de {camaras.length} cámaras
        </div>
      </div>
    </div>
  )
}
