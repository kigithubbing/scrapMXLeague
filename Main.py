inicio = 2002 
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO

#print(datetime.today().strftime('%Y-%m-%d'))

with open('Scraping.csv','w', encoding="utf-8") as header :
    header.write("torneo,año,jornada,local,visita,marcador,estadio,fecha,resultado")

anio_actual = int( datetime.today().strftime('%Y') )
for anio in  range( inicio , anio_actual +2 ) :
    res_torneo=""
    for torneo in ["apertura","clausura"] :
        jornada =1
        
        while True :
            try:

                URL_PRIMERA = f"https://www.resultados-futbol.com/{torneo}_mexico{str(anio)}/grupo1/jornada{str(jornada)}"
                req_primera = requests.get(URL_PRIMERA)
                soup_primera = BeautifulSoup(req_primera.content.decode('utf-8'), features="lxml")

                tabla_Resultados = str(soup_primera.find('table',{'id': 'tabla1'}))

                iotabla= StringIO(tabla_Resultados)
                treetabla = etree.parse(iotabla)
                locales = treetabla.xpath("//td[@class='equipo1']/a[string-length(text())>0]")
                visitas = treetabla.xpath("//td[@class='equipo2']/a[string-length(text())>0]")
                marcadores = treetabla.xpath("//td[@class='rstd']/a/span[@class='clase']")
                estadios= treetabla.xpath("//td[@class='rstd']/span[@class='location hidden']")
                fechas= treetabla.xpath("//td[@class='rstd']/span[@class='dtstart hidden']")
                
                for pos,a in enumerate(locales) :
                    marcador = marcadores[pos].text if pos < len(marcadores) else " - "
                    fecha = fechas[pos].text.split('T')[0]
                    resultado= "?" if ' ' in marcador else "L" if int(marcador[0]) > int(marcador[2]) else "V" if int(marcador[0]) < int(marcador[2]) else "X"
                    res_torneo+= f"\n{torneo},{anio},{jornada},{a.text},{visitas[pos].text},{marcador},{estadios[pos].text},{fecha},{resultado}"

                jornada+=1
                if len(locales) * 2 == jornada :
                    break
            
            except Exception as e:
                print(str(e))
                break
    with open('Scraping.csv','a',encoding="utf-8") as file:
        print(f"Writing {anio}")
        file.write(res_torneo)