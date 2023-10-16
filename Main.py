inicio = 2002 
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO

#print(datetime.today().strftime('%Y-%m-%d'))
#print(inicio)

anio_actual = int( datetime.today().strftime('%Y') )
for anio in  range( inicio , anio_actual +2 ) :
    for torneo in ["apertura","clausura"] :
        jornada =1
        while True :
            try:

                URL_PRIMERA = f"https://www.resultados-futbol.com/{torneo}_mexico{str(anio)}/grupo1/jornada{str(jornada)}"
                #print(URL_PRIMERA_2018)
                req_primera = requests.get(URL_PRIMERA)
                
                

                soup_primera = BeautifulSoup(req_primera.content.decode('utf-8'), features="lxml")

                #with open('Scraping.txt', 'w', encoding= "utf-8") as f:
                #    f.write(str(soup_primera.find('table',{'id': 'tabla1'})))

                tabla_Resultados = str(soup_primera.find('table',{'id': 'tabla1'}))

                # juegos=str(soup_primera.find_all('tr',{'class:','vevent'}))
                # with open('juegos.txt','w',encoding= "utf-8") as j :
                #     j.write(juegos)

                # htmlpage= str(soup_primera.find('body'))
                # print(htmlpage)
                # with open('todo.html','w',encoding="utf-8") as elhtml:
                #     elhtml.write(htmlpage)

                # equipos_local=  str(soup_primera.find_all('td',{'class:','equipo1'}))
                # equipo_local = "".join(str(x) for x in equipos_local).replace("[<td","<td").replace("</td>,","</td>").replace("</td>]","</td>")

                # equipo_visita=str(soup_primera.find_all('td',{'class:','equipo2'}))
                # resultados=str(soup_primera.find_all('td',{'class:','rstd'}))
                # with open('locales.txt','w',encoding="utf-8") as local :
                #     local.write(equipo_local)
                # with open('visitas.txt','w',encoding="utf-8") as visita :
                #     visita.write(equipo_visita)
                # with open('marcadores.txt','w',encoding="utf-8") as res :
                #     res.write(resultados)


                # import lxml.html
                # locales = lxml.html.fromstring(equipo_local)
                # # locales

                
                # html = etree.HTML(equipo_local)
                # result = etree.tostring(html,pretty_print =True, method = "html")
                # # print (result)

            
                # stringHtml = StringIO(equipo_local)
                # print(type(stringHtml))
                # tree = etree.parse(stringHtml)

                # el = tree.xpath("/td/a")
                # print(len(el))

                # ioPage= StringIO(htmlpage)
                # treePage= etree.parse(ioPage)

                # f = StringIO('<foo><bar></bar></foo>')
                # tree = etree.parse(f)

                # r = tree.xpath('/foo/bar')
                # print(len(r))

                iotabla= StringIO(tabla_Resultados)
                treetabla = etree.parse(iotabla)
                locales = treetabla.xpath("//td[@class='equipo1']/a[string-length(text())>0]")
                visitas = treetabla.xpath("//td[@class='equipo2']/a[string-length(text())>0]")
                marcadores = treetabla.xpath("//td[@class='rstd']/a/span[@class='clase']")
                
                print(f"{torneo} {anio} jornada{jornada}")

                for pos,a in enumerate(locales) :
                    marcador = marcadores[pos].text if pos < len(marcadores) else " - "
                    print(f"{a.text} {marcador} {visitas[pos].text}")

                jornada+=1
                if len(locales) * 2 == jornada :
                    break
            except Exception as e:
                # print(str(e))
                break