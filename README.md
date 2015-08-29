# embalses
Python script to fetch and display USGS Water Data for Puerto Rico's damsites

Inspired by http://mate.uprh.edu/embalsespr/  (https://github.com/mecobi/EmbalsesPR)

Wrote this script during storm Erika (8/27/2015) when the embalsepr application (http://mate.uprh.edu/embalsespr/) was not loading data. Installed the script in a cloud server and scheduled it (crontab) to run every 30 minutes to generate a text file in an accesible web server folder.

GPL licensed.

Sample output:

Embalse         Nivel    Cambio   Fecha medida     Estatus       Desborde Seguridad Observ   Ajuste   Contr   
Carite          539.39   [+0.27m] 2015-08-28 20:25 OBSERVACION   544.0    542.0    539.0    537.0    536.0   
Carraizo        36.38    [+1.85m] 2015-08-28 20:45 CONTROL       41.14    39.5     38.5     36.5     30.0    
La Plata        35.229   [+0.38m] 2015-08-28 20:45 CONTROL       51.0     43.0     39.0     38.0     31.0    
Cidra           399.51   [+0.08m] 2015-08-28 20:45 AJUSTE        403.05   401.05   400.05   399.05   398.05  
Patillas        62.706   [+0.65m] 2015-08-28 20:45 AJUSTE        67.07    66.16    64.33    60.52    59.45   
Toa Vaca        144.91   [+0.04m] 2015-08-28 20:45 AJUSTE        161.0    152.0    145.0    139.0    133.0   
Rio Blanco      23.576   [+0.35m] 2015-08-28 20:40 AJUSTE        28.75    26.5     24.25    22.5     18.0    
Caonillas       250.25   [+0.00m] 2015-08-28 20:45 SEGURIDAD     252.0    248.0    244.0    242.0    235.0   
Fajardo         45.2     [+0.35m] 2015-08-28 20:30 OBSERVACION   52.5     48.3     43.4     37.5     26.0    
Guajataca       195.71   [-0.06m] 2015-08-28 20:45 SEGURIDAD     196.0    194.0    190.0    186.0    184.0   
Cerrillos       164.38   [+0.32m] 2015-08-28 20:45 SEGURIDAD     173.4    160.0    155.5    149.4    137.2


