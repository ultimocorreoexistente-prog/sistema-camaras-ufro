import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { HardDrive, Battery, Server, Zap, Plus } from 'lucide-react'

export default function EquiposModule() {
  const equipos = [
    {
      id: 'UPS-001',
      tipo: 'UPS',
      marca: 'APC',
      modelo: 'Smart-UPS 1500',
      capacidad: '1500 VA',
      baterias: 1,
      gabinete: 'GAB-001',
      alimenta: 'Switch SW-001',
      estado: 'Funcionando',
      ultimoMantenimiento: '13/10/2025',
      tipoMantenimiento: 'Cambio de batería'
    },
    {
      id: 'SW-001',
      tipo: 'Switch',
      marca: 'Cisco',
      modelo: 'PoE 24 puertos',
      capacidad: '24 puertos',
      baterias: 0,
      gabinete: 'GAB-001',
      alimenta: '11 cámaras + enlace fibra',
      estado: 'Funcionando',
      ultimoMantenimiento: '',
      tipoMantenimiento: ''
    },
    {
      id: 'SW-002',
      tipo: 'Switch',
      marca: 'TP-Link',
      modelo: 'PoE 8 puertos',
      capacidad: '8 puertos',
      baterias: 0,
      gabinete: 'GAB-002',
      alimenta: '1 cámara PTZ',
      estado: 'Funcionando',
      ultimoMantenimiento: '',
      tipoMantenimiento: ''
    },
    {
      id: 'POE-001',
      tipo: 'POE Externo',
      marca: 'Genérico',
      modelo: 'POE Injector 48V',
      capacidad: '48V 1A',
      baterias: 0,
      gabinete: 'GAB-002',
      alimenta: 'Cámara PTZ Francisco Salazar',
      estado: 'Funcionando',
      ultimoMantenimiento: '',
      tipoMantenimiento: ''
    },
  ]

  const getIcon = (tipo) => {
    switch (tipo) {
      case 'UPS':
        return <Battery className="h-5 w-5 text-green-600" />
      case 'Switch':
        return <HardDrive className="h-5 w-5 text-blue-600" />
      case 'NVR/DVR':
        return <Server className="h-5 w-5 text-purple-600" />
      case 'POE Externo':
        return <Zap className="h-5 w-5 text-orange-600" />
      default:
        return <HardDrive className="h-5 w-5 text-slate-600" />
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <HardDrive className="h-6 w-6" />
                Gestión de Equipos Técnicos
              </CardTitle>
              <CardDescription>
                UPS, Switches, NVR/DVR, Fuentes de Poder y POE
              </CardDescription>
            </div>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Nuevo Equipo
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="border rounded-lg overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-slate-50 dark:bg-slate-900">
                  <TableHead className="font-semibold">ID / Tipo</TableHead>
                  <TableHead className="font-semibold">Marca / Modelo</TableHead>
                  <TableHead className="font-semibold">Capacidad</TableHead>
                  <TableHead className="font-semibold">Ubicación</TableHead>
                  <TableHead className="font-semibold">Alimenta</TableHead>
                  <TableHead className="font-semibold">Estado</TableHead>
                  <TableHead className="font-semibold">Último Mant.</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {equipos.map((equipo) => (
                  <TableRow key={equipo.id} className="hover:bg-slate-50 dark:hover:bg-slate-900/50">
                    <TableCell>
                      <div className="flex items-center gap-2">
                        {getIcon(equipo.tipo)}
                        <div>
                          <div className="font-medium">{equipo.id}</div>
                          <div className="text-sm text-slate-500">{equipo.tipo}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{equipo.marca}</div>
                        <div className="text-sm text-slate-500">{equipo.modelo}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{equipo.capacidad}</div>
                        {equipo.baterias > 0 && (
                          <div className="text-sm text-slate-500">
                            {equipo.baterias} batería(s)
                          </div>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <code className="px-2 py-1 bg-purple-50 dark:bg-purple-950 text-purple-700 dark:text-purple-300 rounded text-sm">
                        {equipo.gabinete}
                      </code>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm">{equipo.alimenta}</span>
                    </TableCell>
                    <TableCell>
                      <Badge variant={equipo.estado === 'Funcionando' ? 'default' : 'destructive'}>
                        {equipo.estado}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {equipo.ultimoMantenimiento ? (
                        <div>
                          <div className="text-sm font-medium">{equipo.ultimoMantenimiento}</div>
                          <div className="text-xs text-slate-500">{equipo.tipoMantenimiento}</div>
                        </div>
                      ) : (
                        <span className="text-sm text-slate-400">Sin registro</span>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Información de UPS */}
          <div className="mt-6 p-4 bg-green-50 dark:bg-green-950/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Battery className="h-5 w-5 text-green-600 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-green-900 dark:text-green-100 mb-1">
                  Control de UPS y Baterías
                </p>
                <p className="text-sm text-green-800 dark:text-green-200">
                  Es importante registrar la marca, modelo, capacidad (VA/W) y número de baterías de cada UPS. 
                  El historial de cambio de baterías permite programar mantenimientos preventivos.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

