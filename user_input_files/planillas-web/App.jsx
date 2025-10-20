import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Camera, HardDrive, AlertTriangle, Wrench, BarChart3, Server, Battery, Cable } from 'lucide-react'
import './App.css'
import CamerasModule from './components/CamerasModule'
import GabinetesModule from './components/GabinetesModule'
import EquiposModule from './components/EquiposModule'
import FallasModule from './components/FallasModule'
import MantenimientosModule from './components/MantenimientosModule'
import Dashboard from './components/Dashboard'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [cameras, setCameras] = useState([])
  const [gabinetes, setGabinetes] = useState([])
  const [switches, setSwitches] = useState([])
  const [switchPorts, setSwitchPorts] = useState([])
  const [technicalEquipment, setTechnicalEquipment] = useState([])
  const [failures, setFailures] = useState([])
  const [maintenance, setMaintenance] = useState([])
  const [locations, setLocations] = useState([])
  const [failureTypes, setFailureTypes] = useState([])
  const [realFailureExamples, setRealFailureExamples] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const [
          camerasRes,
          gabinetesRes,
          switchesRes,
          switchPortsRes,
          technicalEquipmentRes,
          failuresRes,
          maintenanceRes,
          locationsRes,
          failureTypesRes,
          realFailureExamplesRes
        ] = await Promise.all([
          fetch('/data/cameras.json'),
          fetch('/data/gabinetes.json'),
          fetch('/data/switches.json'),
          fetch('/data/switch_ports.json'),
          fetch('/data/technical_equipment.json'),
          fetch('/data/failures.json'),
          fetch('/data/maintenance.json'),
          fetch('/data/locations.json'),
          fetch('/data/failure_types.json'),
          fetch('/data/real_failure_examples.json')
        ])

        const camerasData = await camerasRes.json()
        const gabinetesData = await gabinetesRes.json()
        const switchesData = await switchesRes.json()
        const switchPortsData = await switchPortsRes.json()
        const technicalEquipmentData = await technicalEquipmentRes.json()
        const failuresData = await failuresRes.json()
        const maintenanceData = await maintenanceRes.json()
        const locationsData = await locationsRes.json()
        const failureTypesData = await failureTypesRes.json()
        const realFailureExamplesData = await realFailureExamplesRes.json()

        setCameras(camerasData)
        setGabinetes(gabinetesData)
        setSwitches(switchesData)
        setSwitchPorts(switchPortsData)
        setTechnicalEquipment(technicalEquipmentData)
        setFailures(failuresData)
        setMaintenance(maintenanceData)
        setLocations(locationsData)
        setFailureTypes(failureTypesData)
        setRealFailureExamples(realFailureExamplesData)
        setLoading(false)
      } catch (error) {
        console.error('Error al cargar los datos:', error)
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-4 border-blue-600 mx-auto"></div>
          <p className="mt-6 text-xl font-semibold text-gray-700">Cargando datos del sistema...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Header */}
      <header className="bg-white dark:bg-slate-900 shadow-md border-b border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Camera className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                  Sistema de Gestión de Cámaras
                </h1>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Universidad de la Frontera (UFRO)
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="text-sm px-3 py-1">
                {cameras.length} Cámaras
              </Badge>
              <Badge variant="outline" className="text-sm px-3 py-1">
                v1.0.0
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-6 mb-8 bg-white dark:bg-slate-900 p-1 rounded-lg shadow-md">
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Dashboard</span>
            </TabsTrigger>
            <TabsTrigger value="camaras" className="flex items-center gap-2">
              <Camera className="h-4 w-4" />
              <span className="hidden sm:inline">Cámaras</span>
            </TabsTrigger>
            <TabsTrigger value="gabinetes" className="flex items-center gap-2">
              <Server className="h-4 w-4" />
              <span className="hidden sm:inline">Gabinetes</span>
            </TabsTrigger>
            <TabsTrigger value="equipos" className="flex items-center gap-2">
              <HardDrive className="h-4 w-4" />
              <span className="hidden sm:inline">Equipos</span>
            </TabsTrigger>
            <TabsTrigger value="fallas" className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              <span className="hidden sm:inline">Fallas</span>
            </TabsTrigger>
            <TabsTrigger value="mantenimientos" className="flex items-center gap-2">
              <Wrench className="h-4 w-4" />
              <span className="hidden sm:inline">Mantenimiento</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="mt-0">
            <Dashboard 
              cameras={cameras}
              gabinetes={gabinetes}
              switches={switches}
              technicalEquipment={technicalEquipment}
              failures={failures}
              maintenance={maintenance}
            />
          </TabsContent>

          <TabsContent value="camaras" className="mt-0">
            <CamerasModule 
              cameras={cameras}
              gabinetes={gabinetes}
              switches={switches}
              switchPorts={switchPorts}
              technicalEquipment={technicalEquipment}
            />
          </TabsContent>

          <TabsContent value="gabinetes" className="mt-0">
            <GabinetesModule 
              gabinetes={gabinetes}
              switches={switches}
              technicalEquipment={technicalEquipment}
            />
          </TabsContent>

          <TabsContent value="equipos" className="mt-0">
            <EquiposModule 
              technicalEquipment={technicalEquipment}
              gabinetes={gabinetes}
            />
          </TabsContent>

          <TabsContent value="fallas" className="mt-0">
            <FallasModule 
              failures={failures}
              realFailureExamples={realFailureExamples}
              failureTypes={failureTypes}
              cameras={cameras}
              gabinetes={gabinetes}
              switches={switches}
            />
          </TabsContent>

          <TabsContent value="mantenimientos" className="mt-0">
            <MantenimientosModule 
              maintenance={maintenance}
              technicalEquipment={technicalEquipment}
              gabinetes={gabinetes}
            />
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 mt-16">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-sm text-slate-600 dark:text-slate-400">
            © 2025 Universidad de la Frontera - Sistema de Gestión de Cámaras de Seguridad
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App

