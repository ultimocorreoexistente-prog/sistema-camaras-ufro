import { useState } from 'react'
import { Search, MapPin } from 'lucide-react'

interface Camera {
  id: number
  codigo: string
  nombre: string
  campus: string
  edificio: string
  ubicacion: string
  ip: string
  marca: string
  modelo: string
  estado: string
}

interface CamerasModuleProps {
  camaras: Camera[]
}

export default function CamerasModule({ camaras }: CamerasModuleProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCampus, setSelectedCampus] = useState('all')

  const campus = [...new Set(camaras.map(c => c.campus).filter(Boolean))]

  const filteredCamaras = camaras.filter(camara => {
    const matchesSearch = camara.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         camara.codigo?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCampus = selectedCampus === 'all' || camara.campus === selectedCampus
    return matchesSearch && matchesCampus
  })

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Buscar cámaras..."
              className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-md"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            className="px-4 py-2 border border-slate-300 rounded-md"
            value={selectedCampus}
            onChange={(e) => setSelectedCampus(e.target.value)}
          >
            <option value="all">Todos los Campus</option>
            {campus.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-100">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Código</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Nombre</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Campus</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Edificio</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">IP</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredCamaras.map(camara => (
                <tr key={camara.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 text-sm text-slate-900">{camara.codigo}</td>
                  <td className="px-4 py-3 text-sm text-slate-900">{camara.nombre}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{camara.campus}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{camara.edificio}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{camara.ip}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      camara.estado === 'Operativa' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {camara.estado}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-md">
        <p className="text-sm text-slate-600">
          Mostrando {filteredCamaras.length} de {camaras.length} cámaras
        </p>
      </div>
    </div>
  )
}
