#!/usr/bin/env python3
"""
Script de demostración de las nuevas funcionalidades de mapas de red y campus
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:5000"  # Cambiar según el entorno
USERNAME = "admin"  # Usuario demo
PASSWORD = "admin123"  # Contraseña demo

class DemoMapasCampus:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.logged_in = False
    
    def login(self, username, password):
        """Iniciar sesión en el sistema"""
        print(f"🔐 Iniciando sesión como {username}...")
        
        login_data = {
            'username': username,
            'password': password
        }
        
        response = self.session.post(f"{self.base_url}/login", data=login_data)
        
        if response.status_code == 200 and 'dashboard' in response.url:
            self.logged_in = True
            print("✅ Sesión iniciada exitosamente")
            return True
        else:
            print("❌ Error al iniciar sesión")
            return False
    
    def obtener_campus_disponibles(self):
        """Obtener lista de campus configurados"""
        print("\n📍 Obteniendo campus disponibles...")
        
        response = self.session.get(f"{self.base_url}/api/campus-disponibles")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                campus = data['data']
                print(f"✅ Campus encontrados: {', '.join(campus)}")
                return campus
            else:
                print(f"❌ Error: {data['error']}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
        
        return []
    
    def generar_mapa_red_completo(self):
        """Generar mapa completo de red"""
        print("\n🌐 Generando mapa de red completo...")
        
        response = self.session.get(f"{self.base_url}/api/informes/mapa-red-completo")
        
        if response.status_code == 200:
            filename = f"mapa_red_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Mapa de datos generado: {filename}")
            return filename
        else:
            print(f"❌ Error generando mapa: {response.status_code}")
        
        return None
    
    def generar_mapa_visual(self, tipo_mapa, campus=None):
        """Generar visualización de mapa"""
        print(f"\n🎨 Generando visualización: {tipo_mapa}")
        
        params = {}
        if campus:
            params['campus'] = campus
        
        response = self.session.get(f"{self.base_url}/api/mapa-visual/{tipo_mapa}", params=params)
        
        if response.status_code == 200:
            filename = f"mapa_visual_{tipo_mapa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Visualización generada: {filename}")
            return filename
        else:
            print(f"❌ Error generando visualización: {response.status_code}")
        
        return None
    
    def generar_inventario_campus(self, tipo_inventario):
        """Generar inventarios por campus"""
        print(f"\n📋 Generando inventario: {tipo_inventario}")
        
        response = self.session.get(f"{self.base_url}/api/informes/{tipo_inventario}")
        
        if response.status_code == 200:
            filename = f"inventario_{tipo_inventario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Inventario generado: {filename}")
            return filename
        else:
            print(f"❌ Error generando inventario: {response.status_code}")
        
        return None
    
    def generar_informe_filtrado(self, tipo_informe, campus_lista, fecha_inicio=None, fecha_fin=None):
        """Generar informe filtrado por campus y fechas"""
        print(f"\n🔍 Generando informe filtrado: {tipo_informe}")
        print(f"   Campus: {', '.join(campus_lista)}")
        if fecha_inicio and fecha_fin:
            print(f"   Fechas: {fecha_inicio} a {fecha_fin}")
        
        params = {}
        for campus in campus_lista:
            params.setdefault('campus', []).append(campus)
        
        if fecha_inicio:
            params['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            params['fecha_fin'] = fecha_fin
        
        # Convertir lista de campus a múltiples parámetros
        url_params = []
        if 'campus' in params:
            for campus in params['campus']:
                url_params.append(f"campus={campus}")
        if 'fecha_inicio' in params:
            url_params.append(f"fecha_inicio={params['fecha_inicio']}")
        if 'fecha_fin' in params:
            url_params.append(f"fecha_fin={params['fecha_fin']}")
        
        query_string = "&".join(url_params)
        url = f"{self.base_url}/api/informes/{tipo_informe}/filtro?{query_string}"
        
        response = self.session.get(url)
        
        if response.status_code == 200:
            campus_str = "_".join(campus_lista[:2])  # Primeros 2 campus en nombre
            filename = f"informe_{tipo_informe}_{campus_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Informe filtrado generado: {filename}")
            return filename
        else:
            print(f"❌ Error generando informe filtrado: {response.status_code}")
            print(f"   URL: {url}")
        
        return None
    
    def demostrar_todas_funcionalidades(self):
        """Ejecutar demostración completa"""
        print("🚀 DEMOSTRACIÓN DE FUNCIONALIDADES AVANZADAS")
        print("=" * 50)
        
        if not self.logged_in:
            print("❌ Debe iniciar sesión primero")
            return
        
        # 1. Obtener campus disponibles
        campus_lista = self.obtener_campus_disponibles()
        
        # 2. Generar mapas de red (datos)
        print("\n" + "="*30 + " MAPAS DE RED " + "="*30)
        self.generar_mapa_red_completo()
        
        for tipo_mapa in ['mapa-red-cascada', 'mapa-red-campus', 'mapa-jerarquico']:
            self.generar_mapa_red_completo()  # Usar mismo endpoint por simplicidad
        
        # 3. Generar visualizaciones
        print("\n" + "="*30 + " VISUALIZACIONES " + "="*30)
        for tipo_visual in ['completo', 'campus', 'cascada']:
            campus_param = campus_lista[0] if campus_lista and tipo_visual == 'campus' else None
            self.generar_mapa_visual(tipo_visual, campus_param)
        
        # 4. Generar inventarios por campus
        print("\n" + "="*30 + " INVENTARIOS " + "="*30)
        for tipo_inventario in ['camaras-campus', 'gabinetes-campus', 'switches-campus']:
            self.generar_inventario_campus(tipo_inventario)
        
        # 5. Generar informes filtrados por campus
        if campus_lista:
            print("\n" + "="*30 + " INFORMES FILTRADOS " + "="*30)
            
            # Usar fechas de ejemplo (último mes)
            fecha_fin = datetime.now().strftime('%Y-%m-%d')
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Usar primeros 2 campus para demo
            campus_demo = campus_lista[:2] if len(campus_lista) >= 2 else campus_lista
            
            for tipo_informe in ['fallas-pendientes-campus', 'fallas-reparadas-campus', 'camaras-campus']:
                self.generar_informe_filtrado(tipo_informe, campus_demo, fecha_inicio, fecha_fin)
        
        print("\n" + "="*50)
        print("✅ DEMOSTRACIÓN COMPLETADA")
        print("\nArchivos generados en el directorio actual:")
        
        # Listar archivos generados
        import glob
        archivos = glob.glob("*.xlsx") + glob.glob("*.png")
        archivos_hoy = [f for f in archivos if datetime.now().strftime('%Y%m%d') in f]
        
        for archivo in sorted(archivos_hoy):
            size = os.path.getsize(archivo) / 1024  # KB
            print(f"  📄 {archivo} ({size:.1f} KB)")
    
    def menu_interactivo(self):
        """Menú interactivo para probar funcionalidades"""
        while True:
            print("\n" + "="*50)
            print("🎛️  MENÚ INTERACTIVO - MAPAS Y CAMPUS")
            print("="*50)
            print("1. Obtener campus disponibles")
            print("2. Generar mapa de red completo")
            print("3. Generar visualización de mapa")
            print("4. Generar inventario por campus")
            print("5. Generar informe filtrado")
            print("6. 🚀 Demostrar todas las funcionalidades")
            print("7. Salir")
            
            opcion = input("\nSeleccione una opción (1-7): ").strip()
            
            if opcion == "1":
                self.obtener_campus_disponibles()
            
            elif opcion == "2":
                self.generar_mapa_red_completo()
            
            elif opcion == "3":
                print("\nTipos de mapa disponibles:")
                print("1. completo")
                print("2. campus")
                print("3. cascada")
                tipo = input("Seleccione tipo (1-3): ").strip()
                tipo_map = {"1": "completo", "2": "campus", "3": "cascada"}
                if tipo in tipo_map:
                    campus = input("Campus (opcional): ").strip() or None
                    self.generar_mapa_visual(tipo_map[tipo], campus)
            
            elif opcion == "4":
                print("\nTipos de inventario:")
                print("1. camaras-campus")
                print("2. gabinetes-campus") 
                print("3. switches-campus")
                tipo = input("Seleccione tipo (1-3): ").strip()
                tipo_map = {"1": "camaras-campus", "2": "gabinetes-campus", "3": "switches-campus"}
                if tipo in tipo_map:
                    self.generar_inventario_campus(tipo_map[tipo])
            
            elif opcion == "5":
                campus_input = input("Campus (separados por coma): ").strip()
                campus_lista = [c.strip() for c in campus_input.split(",")] if campus_input else []
                fecha_inicio = input("Fecha inicio (YYYY-MM-DD, opcional): ").strip() or None
                fecha_fin = input("Fecha fin (YYYY-MM-DD, opcional): ").strip() or None
                tipo_informe = input("Tipo de informe (ej: fallas-pendientes-campus): ").strip()
                
                if tipo_informe:
                    self.generar_informe_filtrado(tipo_informe, campus_lista, fecha_inicio, fecha_fin)
            
            elif opcion == "6":
                self.demostrar_todas_funcionalidades()
            
            elif opcion == "7":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción no válida")

def main():
    print("🎯 SISTEMA DE DEMO - MAPAS DE RED Y CAMPUS")
    print("="*50)
    
    # Configurar demo
    demo = DemoMapasCampus(BASE_URL)
    
    # Intentar login
    if demo.login(USERNAME, PASSWORD):
        print("\n¿Qué desea hacer?")
        print("1. Demostración automática completa")
        print("2. Menú interactivo")
        
        modo = input("\nSeleccione modo (1-2): ").strip()
        
        if modo == "1":
            demo.demostrar_todas_funcionalidades()
        elif modo == "2":
            demo.menu_interactivo()
        else:
            print("❌ Opción no válida")
    else:
        print(f"\n⚠️  Instrucciones para usar este script:")
        print(f"1. Asegúrese de que el servidor esté ejecutándose en {BASE_URL}")
        print(f"2. Verifique las credenciales: {USERNAME}/{PASSWORD}")
        print(f"3. Ejecute: python actualizar_db_campus.py")
        print(f"4. Ejecute: python app.py")
        print(f"5. Vuelva a ejecutar este script")

if __name__ == "__main__":
    main()