import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { Search, Plus, Download, Camera, MapPin, Network } from 'lucide-react'

export default function CamerasModule() {
  const [searchTerm, setSearchTerm] = useState('')

  // Datos de ejemplo basados en el caso real
  const camaras = [
    {
      id: 1,
      nombre: '2030_Acceso_1P',
      ip: '172.22.3.9',
      ubicacion: 'Edificio 2030 - 1er Piso - Acceso',
      gabinete: 'GAB-001',
      switch: 'SW-001',
      puerto: '1',
      tipo: 'Domo',
      poe: 'No',
      estado: 'Funcionando',
      instalador: 'Técnico Propio'
    },
    {
      id: 2,
      nombre: 'EdificioO_Domo_1P_01',
      ip: '172.22.4.10',
      ubicacion: 'Edificio O - 1er Piso - Pasillo',
      gabinete: 'GAB-001',
      switch: 'SW-001',
      puerto: '2',
      tipo: 'Domo',
      poe: 'No',
      estado: 'Funcionando',
      instalador: 'Técnico Propio'
    },
    {
      id: 3,
      nombre: 'EdificioO_PTZ_3P_Exterior',
      ip: '172.22.4.25',
      ubicacion: 'Edificio O - 3er Piso - Exterior',
      gabinete: 'GAB-001',
      switch: 'SW-001',
      puerto: '11',
      tipo: 'PTZ',
      poe: 'Sí',
      estado: 'Funcionando',
      instalador: 'Técnico Propio'
    },
    {
      id: 4,
      nombre: 'PTZ_FranciscoSalazar',
      ip: '172.22.5.30',
      ubicacion: 'Francisco Salazar - Subterráneo',
      gabinete: 'GAB-002',
      switch: 'SW-002',
      puerto: '1',
      tipo: 'PTZ',
      poe: 'Sí',
      estado: 'Funcionando',
      instalador: 'Empresa Subcontratista'
    },
  ]

  const filteredCamaras = camaras.filter(cam =>
    cam.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cam.ip.includes(searchTerm) ||
    cam.ubicacion.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getEstadoBadge = (estado) => {
    const variants = {
      'Funcionando': 'default',
      'Averiada': 'destructive',
      'En mantenimiento': 'secondary',
      'Fuera de servicio': 'outline'
    }
    return <Badge variant={variants[estado] || 'default'}>{estado}</Badge>
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Camera className="h-6 w-6" />
                Gestión de Cámaras
              </CardTitle>
              <CardDescription>
                Administra todas las cámaras del sistema con sus conexiones y ubicaciones
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Exportar
              </Button>
              <Button size="sm">
                <Plus className="h-4 w-4 mr-2" />
                Nueva Cámara
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Búsqueda */}
          <div className="mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
              <Input
                type="text"
                placeholder="Buscar por nombre, IP o ubicación..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>

          {/* Tabla de cámaras */}
          <div className="border rounded-lg overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-slate-50 dark:bg-slate-900">
                  <TableHead className="font-semibold">Nombre</TableHead>
                  <TableHead className="font-semibold">IP</TableHead>
                  <TableHead className="font-semibold">Ubicación</TableHead>
                  <TableHead className="font-semibold">Conexión</TableHead>
                  <TableHead className="font-semibold">Tipo</TableHead>
                  <TableHead className="font-semibold">POE Extra</TableHead>
                  <TableHead className="font-semibold">Estado</TableHead>
                  <TableHead className="font-semibold">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredCamaras.map((camara) => (
                  <TableRow key={camara.id} className="hover:bg-slate-50 dark:hover:bg-slate-900/50">
                    <TableCell className="font-medium">{camara.nombre}</TableCell>
                    <TableCell>
                      <code className="px-2 py-1 bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300 rounded text-sm">
                        {camara.ip}
                      </code>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-start gap-2">
                        <MapPin className="h-4 w-4 text-slate-400 mt-0.5 flex-shrink-0" />
                        <span className="text-sm">{camara.ubicacion}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-start gap-2">
                        <Network className="h-4 w-4 text-slate-400 mt-0.5 flex-shrink-0" />
                        <div className="text-sm">
                          <div className="font-medium">{camara.gabinete}</div>
                          <div className="text-slate-500">
                            {camara.switch} • Puerto {camara.puerto}
                          </div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{camara.tipo}</Badge>
                    </TableCell>
                    <TableCell>
                      {camara.poe === 'Sí' ? (
                        <Badge variant="secondary">Sí</Badge>
                      ) : (
                        <span className="text-slate-400">No</span>
                      )}
                    </TableCell>
                    <TableCell>{getEstadoBadge(camara.estado)}</TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm">
                        Ver Detalles
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Información adicional */}
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
            <p className="text-sm text-blue-900 dark:text-blue-100">
              <strong>Nota:</strong> La dirección IP es un dato crítico para la identificación y acceso a cada cámara. 
              El puerto del switch permite un troubleshooting rápido de problemas de conectividad.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

