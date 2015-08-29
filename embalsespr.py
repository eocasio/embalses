#  encoding: utf-8
#  embalsespr.py
#  Muestra cambio en nivel en ultimas 24 horas (aproximadamente)
#
#  Inspirado por http://mate.uprh.edu/embalsespr/
#  8/27/2015
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Copyright 2015 Edwood Ocasio <edwood.ocasio@gmail.com>
#

import csv, sys
from datetime import datetime, timedelta
from StringIO import StringIO

try:
    import requests
except ImportError:
    print u"Este programa requiere el módulo 'requests'"
    sys.exit()


header= """
#  embalsespr.py
#  Muestra cambio en nivel en ultimas 24 horas (aproximadamente)
#  Inspirado por http://mate.uprh.edu/embalsespr/
#  8/27/2015
#  Copyright 2015 Edwood Ocasio <edwood.ocasio@gmail.com>
########################################################################
# Datos provistos por el grupo CienciaDatosPR del Departamento de 
# Matematicas de la Universidad de Puerto Rico en Humacao
# Inspirado por http://mate.uprh.edu/embalsespr/
########################################################################

Estos datos están sujetos a revisión por el USGS y no deben ser tomados 
como oficiales o libres de errores de medición.

"""

########################################################################
# Datos provistos por el grupo CienciaDatosPR del Departamento de 
# Matemáticas de la Universidad de Puerto Rico en Humacao
# https://raw.githubusercontent.com/mecobi/EmbalsesPR/master/embalses.csv

sites_raw_data = """nombre,siteID,latitude,longitude,desborde,seguridad,observacion,ajuste,control,capacidad
Carite,50039995,18.07524,-66.10683,544,542,539,537,536,8320
Carraizo,50059000,18.32791,-66.01628,41.14,39.5,38.5,36.5,30,12000
La Plata,50045000,18.343,-66.23607,51,43,39,38,31,26516
Cidra,50047550,18.1969,-66.14072,403.05,401.05,400.05,399.05,398.05,4480
Patillas,50093045,18.01774,-66.0185,67.07,66.16,64.33,60.52,59.45,9890
Toa Vaca,50111210,18.10166,-66.48902,161,152,145,139,133,50650
Rio Blanco,50076800,18.22389,-65.78142,28.75,26.5,24.25,22.5,18,3795
Caonillas,50026140,18.27654,-66.65642,252,248,244,242,235,31730
Fajardo,50071225,18.2969,-65.65858,52.5,48.3,43.4,37.5,26,4430
Guajataca,50010800,18.39836,-66.9227,196,194,190,186,184,33340
Cerrillos,50113950,18.07703,-66.57547,173.4,160,155.5,149.4,137.2,42600
"""

# Guardar datos anteriores como "file object" para
# tratarlos como un archivo csv
sites_data = csv.DictReader(StringIO(sites_raw_data))

# Lista de embalses específicos por nombre
# e.g. ['Carite','Patillas']
# Deje lista vacía para incluir todos los embalses.
only_this_sites = []

# Fechas de interés
today = datetime.now().date()
yesterday = today - timedelta(days=1)

# Plantilla URL para obtener datos del USGS
# ver http://waterdata.usgs.gov/nwis?automated_retrieval_info

USGS_URL = 'http://nwis.waterdata.usgs.gov/pr/nwis/uv/?cb_62616=on&format=rdb&site_no=%s&begin_date=%s&end_date=%s'

print header
print u"Actualizado: ", datetime.now()
print

print u"Datos embalses en USGS ..."
print

# Nombre columnas
print u"%-15s %-8s %-8s %-16s %-12s  %-8s %-8s %-8s %-8s %-8s" % ("Embalse", "Nivel",  "Cambio", "Fecha medida", "Estatus", 'Desborde', 'Seguridad', 'Observ', 'Ajuste', 'Contr')

for site in sites_data:
    # ¿Existe una lista específica de embalses?
    if only_this_sites:
        if site["nombre"] in only_sites:
            site_ID = site["siteID"]
        else:
            continue
    else:
        site_ID =site["siteID"]
    
    url_final = USGS_URL % (site_ID, yesterday , today)

    try:
        # Buscar datos
        r = requests.get(url_final, timeout=60)
        
        # Convertirlos en archivo CSV
        levels_data = csv.reader(StringIO(r.content), delimiter='\t')
        
        # Extraer todas las filas de datos ignorando comentarios
        rows = [row for row in levels_data if row[0][0] != '#']
        
        # Obtener nivel del embalse hace 24 horas (aproximadamente)
        # Cada fila representa un intervalo de 15 minutos.
        # La fila 96 intervalos atrás contiene ese valor (aproximadamente).
        first_row = rows[-97]
        
        first_level = float(first_row[4])
        
        # Última lectura del archivo
        last_row = rows[-1]
        measurement_date = last_row[2]
        last_level = float(last_row[4])
        
        diff_levels = last_level - first_level
        
        # Determinar estatus del embalse
        status = ''
        if last_level >= float(site["desborde"]):
            status = "DESBORDE"
        elif float(site["seguridad"]) <= last_level < float(site["desborde"]):
            status = "SEGURIDAD"
        elif float(site["observacion"]) <= last_level < float(site["seguridad"]):
            status = "OBSERVACION"
        elif float(site["ajuste"]) <= last_level < float(site["observacion"]):
            status = "AJUSTE"
        elif float(site["control"]) <= last_level < float(site["ajuste"]):
            status = "CONTROL"
        elif last_level < float(site["control"]):
            status = "FUERA SERVICIO"
       
        # Mostrar información resumida del embalse:
        #   nombre, última lectura en metros, cambio en últimas 24 horas, fecha última lectura, estatus, estatus y sus niveles de referencia
         
        print u"%-15s %-8s [%+.2fm] %-16s %-12s  %-8s %-8s %-8s %-8s %-8s" % (site["nombre"], last_level,  diff_levels, measurement_date, status, float(site['desborde']), float(site['seguridad']), float(site['observacion']), float(site['ajuste']), float(site['control']))


    except Exception, e:
        print u"%s = N/A" % site["nombre"]
        
        # Para ver errores específicos:           
        # print "Error: %s" % str(e)

