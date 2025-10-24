import { useState, useEffect } from 'react'
import { Camera, Server, HardDrive, AlertTriangle, Wrench, BarChart3 } from 'lucide-react'
import Dashboard from './components/Dashboard'
import CamerasModule from './components/CamerasModule'
import GabinetesModule from './components/GabinetesModule'
import SwitchesModule from './components/SwitchesModule'
import FallasModule from './components/FallasModule'
import MantenimientosModule from './components/MantenimientosModule'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [data, setData] = useState({
    camaras: [],
    gabinetes: [],
    switches: [],
    fallas: [],
    mantenimientos: [],
    estadisticas: null
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [camarasRes, gabinetesRes, switchesRes, fallasRes, mantenimientosRes, estadisticasRes] = await Promise.all([
        fetch('/api/camaras'),
        fetch('/api/gabinetes'),
        fetch('/api/switches'),
        fetch('/api/fallas'),
        fetch('/api/mantenimientos'),
        fetch('/api/estadisticas')
      ])

      setData({
        camaras: await camarasRes.json(),
        gabinetes: await gabinetesRes.json(),
        switches: await switchesRes.json(),
        fallas: await fallasRes.json(),
        mantenimientos: await mantenimientosRes.json(),
        estadisticas: await estadisticasRes.json()
      })
    } catch (error) {
      console.error('Error cargando datos:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <header className="bg-white shadow-md border-b border-slate-200">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Camera className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">
                Sistema de Gestión de Cámaras UFRO
              </h1>
              <p className="text-sm text-slate-600">Universidad de la Frontera</p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md mb-8">
          <div className="grid grid-cols-2 md:grid-cols-6 gap-2 p-2">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-4 py-3 rounded-md transition-colors ${
                activeTab === 'dashboard' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Dashboard</span>
            </button>
            <button
              onClick={() => setActiveTab('camaras')}
              className={`flex items-center gap-2 px-4 py-3 rounded-md transition-colors ${
                activeTab === 'camaras' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <Camera className="h-4 w-4" />
              <span className="hidden sm:inline">Cámaras</span>
            </button>
            <button
              onClick={() => setActiveTab('gabinetes')}
              className={`flex items-center gap-2 px-4 py-3 rounded-md transition-colors ${
                activeTab === 'gabinetes' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <Server className="h-4 w-4" />
              <span className="hidden sm:inline">Gabinetes</span>
            </button>
            <button
              onClick={() => setActiveTab('switches')}
              className={`flex items-center gap-2 px-4 py-3 rounded-md transition-colors ${
                activeTab === 'switches' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <HardDrive className="h-4 w-4" />
              <span className="hidden sm:inline">Switches</span>
            </button>
            <button
              onClick={() => setActiveTab('fallas')}
              className={`flex items-center gap-2 px-4 py-3 rounded-md transition-colors ${
                activeTab === 'fallas' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <AlertTriangle className="h-4 w-4" />
              <span className="hidden sm:inline">Fallas</span>
            </button>
            <button
              onClick={() => setActiveTab('mantenimientos')}
              className={`flex items-center gap-2 px-4 py-3 rounded-md transition-colors ${
                activeTab === 'mantenimientos' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <Wrench className="h-4 w-4" />
              <span className="hidden sm:inline">Mantenimiento</span>
            </button>
          </div>
        </div>

        <div className="mt-6">
          {activeTab === 'dashboard' && <Dashboard data={data} />}
          {activeTab === 'camaras' && <CamerasModule camaras={data.camaras} />}
          {activeTab === 'gabinetes' && <GabinetesModule gabinetes={data.gabinetes} />}
          {activeTab === 'switches' && <SwitchesModule switches={data.switches} />}
          {activeTab === 'fallas' && <FallasModule fallas={data.fallas} />}
          {activeTab === 'mantenimientos' && <MantenimientosModule mantenimientos={data.mantenimientos} />}
        </div>
      </main>

      <footer className="bg-white border-t border-slate-200 mt-16">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-sm text-slate-600">
            2025 Universidad de la Frontera - Sistema de Gestión de Cámaras de Seguridad
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
