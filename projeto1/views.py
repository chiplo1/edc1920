from itertools import count

from lxml import etree
from django.shortcuts import render
from BaseXClient import BaseXClient
from io import StringIO
from io import BytesIO
import sys
import xmltodict
import feedparser

# Create your views here.

def main(request):
    doc = etree.parse("portugal.xml")
    search = doc.xpath("//distrito")
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    send = {}
    infoportugal = {}
    for s in search:
        send[s.find("nomedistrito").text] = s.find("iddistrito").text

    try:
        input = '''
        for $i in doc("portugal")
        let $dados := $i//municipio
        let $totalpop := sum($dados/populacao)
        let $totalarea := sum($dados/area)
        let $densidadeportugal := $totalpop div $totalarea
        return <portugal>{<totalpop>{xs:integer($totalpop)}</totalpop>, <totalarea>{$totalarea}</totalarea>, <densidadeportugal>{$densidadeportugal}</densidadeportugal>}</portugal>'''
        query = session.query(input)
        search = xmltodict.parse(query.execute())['portugal']
        query.close()
    finally:
        if session:
            infoportugal['totalpop'] = search['totalpop']
            infoportugal['totalarea'] = search['totalarea']
            infoportugal['densidadeportugal'] = search['densidadeportugal']
            session.close()
    return render(request, 'newmain.html', {"send": send, "infoportugal": infoportugal})

def distritos(request):
    doc = etree.parse("portugal.xml")
    search = doc.xpath("//distrito")
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    send = {}
    infoportugal = {}
    for s in search:
        send[s.find("nomedistrito").text] = s.find("iddistrito").text

    try:
        input = '''
            for $i in doc("portugal")
            let $dados := $i//municipio
            let $totalpop := sum($dados/populacao)
            let $totalarea := sum($dados/area)
            let $densidadeportugal := $totalpop div $totalarea
            return <portugal>{<totalpop>{xs:integer($totalpop)}</totalpop>, <totalarea>{$totalarea}</totalarea>, <densidadeportugal>{$densidadeportugal}</densidadeportugal>}</portugal>'''
        query = session.query(input)
        search = xmltodict.parse(query.execute())['portugal']
        query.close()
    finally:
        if session:
            infoportugal['totalpop'] = search['totalpop']
            infoportugal['totalarea'] = search['totalarea']
            infoportugal['densidadeportugal'] = search['densidadeportugal']
            session.close()
    return render(request, 'distritos.html', {"send": send, "infoportugal": infoportugal})

def rssFeed(request):
    NewsFeed = feedparser.parse("https://www.ine.pt/ine/rssfeed_pub.jsp?lang=EN")
    list = []
    for news_entry in NewsFeed.entries:
        dict = {
        'news_title': news_entry.title,
        'news_link': news_entry.link,
        'news_description': news_entry.description,
        }
        list.append(dict)

    return render(request, 'rssFeed.html', {"list": list})

#def distritoDetail(request):
#    data = request.GET
#    id = data['id']
#    doc = etree.parse("portugal.xml")
#    string = '//distrito[iddistrito="{}"]'.format(id)
#
#    search = doc.xpath(string)
#
#    send = {}
#
#    for s in search:
#        send["nomedistrito"] = s.find("nomedistrito").text
#        municipios = s.findall("municipios/municipio")
#        interesses = s.findall("interesses/interesse")
#
#    listanomes = {}
#    for x in municipios:
#        listanomes[x.find("idmunicipio").text] = x.find("nomeconcelho").text
#
#    listainteresses = {}
#    for x in interesses:
#        listainteresses[x.find("iddistrito").text] = x.find("nome").text
#
#    send["municipios"] = listanomes
#    send["interesses"] = listainteresses
#    return render(request, 'distritoDetail.html', {"send": send})

###########################conecçao com basex  xquery-infoDistrito################################

def distritoDetail(request):
    #create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    data = request.GET
    id = data['id']
    try:
        #create query instance
        input = "import module namespace funcs = 'com.funcs.my.index';funcs:distrito({})".format(id)
        query = session.query(input)

        response = query.execute()

        query.close()

        input = "import module namespace funcs = 'com.funcs.my.index';funcs:interesseDist({})".format(id)
        query = session.query(input)
        response2 = query.execute()
        query.close()
    finally:
        if session:
            municipios = {}
            interesses = {}
            search = xmltodict.parse(response)['distrito']
            if not response2 == "<interesse/>":
                search1 = xmltodict.parse(response2)['interesse']['interesse']
            else:
                search1 = ''
            municipios['imagemdistrito'] = search['imagemdistrito']
            municipios['nomedistrito'] = search['nomedistrito']
            municipios['numpopulacao'] = search['numpopulacao']
            municipios['areatotal'] = round(float(search['areatotal']), 2)
            municipios['densidadedistrito'] = round(float(search['densidadedistrito']), 2)

            for s in search['municipios']['municipio']:
                municipios[s['idmunicipio']] = s['nomeconcelho']
            for m in search1:
                interesses[m['idinteresse']] = m['nome']
            session.close()

    return render(request, 'distritoDetail.html', {"municipios":municipios,"interesses":interesses})


def municipioDetail(request):
    nomeinteresse = None
    tipo = None
    lastid = None
    data = request.GET
    id = data['id']
    doc = etree.parse("portugal.xml")
    string = '//municipio[idmunicipio="{}"]'.format(id)

    search = doc.xpath(string)

    send = {}

    for s in search:
        send["nomeconcelho"] = s.find("nomeconcelho").text
        send["idmunicipio"] = s.find("idmunicipio").text
        send["regiao"] = s.find("regiao").text
        send["area"] = s.find("area").text
        send["populacao"] = s.find("populacao").text
        send["densidadepopulacional"] = s.find("densidadepopulacional").text
        #interesses = s.findall("interesses/interesse")

        #if isinstance(interesses,list):
         #   for i in interesses:
          #      listanomes[i.find("idinteresse").text] = (i.find("nome").text,i.find("tipo").text)
        #else:
        #    listanomes[interesses.find("idinteresse").text] = (interesses.find("nome").text,interesses.find("tipo").text)

        #send['interesses'] = listanomes

    #####IMPRIMIR INTERESSES
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    listanomes = {}
    try:
        input = "import module namespace funcs = 'com.funcs.my.index';funcs:interesseMunicipio({})".format(id)
        query = session.query(input)
        response = query.execute()
        search = xmltodict.parse(response)['interesse']
        #print(search)
        #print(search['num'])
        if search['num'] == "0":
            listanomes = {}
        elif search['num'] == "1":
            #print(search['interesse']['nome'])
            listanomes[search['interesse']['idinteresse']] = {"nome": search['interesse']['nome'], "tipo": search['interesse']['tipo']}
        else:
            for s in search['interesse']:
                print(s)
                listanomes[s['idinteresse']] = {"nome": s['nome'], "tipo": s['tipo']}
        #print(listanomes)
        query.close()
    finally:
        if session:
            session.close()

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        input = '''for $i in doc('portugal')
                        let $int := $i//idinteresse
                        return max($int)'''
        query = session.query(input)
        lastid = query.execute()
        query.close()
    finally:
        if session:
            session.close()

     # receber informaçao do html para adicinar o interesse
    if 'nomeinteresse' in request.POST and 'tipo' in request.POST:
        nomeinteresse = request.POST.get('nomeinteresse')
        tipo = request.POST.get('tipo')

    response = None
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        # create query instance
        if (nomeinteresse != None and tipo != None):
            # input = "import module namespace funcs = 'com.funcs.my.index';funcs:add({}, {}, {}, {})".format(id, str(nomeinteresse), tipo, maximo+1)
            lastid = int(lastid, 10) + 1
            input = '''for $i in doc('portugal')//municipio
                       where $i/idmunicipio = {}
                       return
                         insert node
                       <interesse>
                         <idinteresse>{}</idinteresse>
                         <nome>{}</nome>
                         <tipo>{}</tipo>
                       </interesse>
                       as last into $i/interesses'''.format(id, lastid, nomeinteresse, tipo)
            query = session.query(input)
            response = query.execute()
            query.close()
    finally:
        #lastid += 1
        if session:
            session.close()
    send['valid'] = 'Não selecionou nenhum XML'

    if 'xmldocument' in request.POST :
        doc = request.POST.get('xmldocument')
        if doc != '':
            xmldocument = request.POST.get('xmldocument')
            isvalid = validateXML(xmldocument)
            send['valid'] = isvalid
            ## XML VALID, NOW INSERT INTO DATABASE

            if isvalid == 'XML válido':
                values = etree.parse(xmldocument)

                search = values.xpath("//interesse")
                # create session
                session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
                '''
                for s in search:
                    
                    nomei = s.find("nome").text
                    tipoi = s.find("tipo").text
                    nomedistritoi = s.find("nomedistrito").text
                    nomeconcelhoi = s.find("nomeconcelho").text
                    try:
                        # create query instance
                        if (nomei != None and tipoi != None and nomedistritoi != None and nomeconcelhoi != None):
                            # input = "import module namespace funcs = 'com.funcs.my.index';funcs:add({}, {}, {}, {})".format(nomeconcelhoi, str(nomei), tipoi, maximo)
                            #input = ''''''for $i in doc('portugal')//municipio
                                       where $i/nomeconcelho = {}
                                       return
                                         insert node
                                       <interesse>
                                         <idinteresse>{}</idinteresse>
                                         <nome>{}</nome>
                                         <tipo>{}</tipo>
                                       </interesse>
                              #         as last into $i/interesses''''''.format(nomeconcelhoi, maximo, nomei, tipoi)
                            query = session.query(input)
                            response = query.execute()
                            query.close()
                    finally:
                        maximo += 1
                        if session:
                            session.close()'''

    return render(request, 'municipioDetail.html', {"send": send, "interesses": listanomes})

def interesseDetail(request):
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    data = request.GET
    id = data['id']
    search = {}
    try:
        #create query instance
        input = "import module namespace funcs = 'com.funcs.my.index';funcs:interesse({})".format(id)
        query = session.query(input)
        search = xmltodict.parse(query.execute())['interesse']
        query.close()
        #print(search)
    finally:
        if session:
            send = {'nome':search['nome'], 'tipo':search['tipo'], 'nomeconcelho':search['nomeconcelho'], 'nomedistrito':search['nomedistrito']}
            session.close()
    return render(request, 'interesseDetail.html', {"send": send})

def interesses(request):
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    try:
        # create query instance
        input1 = "import module namespace funcs = 'com.funcs.my.index';funcs:interesses({})".format("'Cultura'")
        query1 = session.query(input1)
        search1 = xmltodict.parse(query1.execute())['interesses']['interesse']
        send = {}
        cultura = {}
        for s in search1:
            cultura[s['idinteresse']] = [s['nome'],s['regiao']]
        query1.close()

        input2="import module namespace funcs = 'com.funcs.my.index';funcs:interesses({})".format("'Lazer'")
        query2 = session.query(input2)
        search2 = xmltodict.parse(query2.execute())['interesses']['interesse']
        lazer = {}
        for s in search2:
            lazer[s['idinteresse']] = [s['nome'],s['regiao']]
        query2.close()

        input3 = "import module namespace funcs = 'com.funcs.my.index';funcs:interesses({})".format("'Gastronomia e vinhos'")
        query3 = session.query(input3)
        search3 = xmltodict.parse(query3.execute())['interesses']['interesse']
        gastronomia = {}
        for s in search3:
            gastronomia[s['idinteresse']] = [s['nome'],s['regiao']]
        query3.close()

        input4 = "import module namespace funcs = 'com.funcs.my.index';funcs:interesses({})".format("'Património'")
        query4 = session.query(input4)
        search4 = xmltodict.parse(query4.execute())['interesses']['interesse']
        patrimonio = {}
        for s in search4:
            patrimonio[s['idinteresse']] = [s['nome'],s['regiao']]
        query4.close()

    finally:
        if session:
            session.close()

    send['cultura'] = cultura
    send['lazer'] = lazer
    send['gastronomia'] = gastronomia
    send['patrimonio'] = patrimonio

    return render(request, 'interesses.html', {"send": send})

def sobre(request):
    s = etree.parse("sobre.xml")
    xslt = etree.parse("sobre.xsl")
    transf = etree.XSLT(xslt)
    sobre = transf(s)
    print(sobre)
    return render(request, 'sobre.html', {"sobre": sobre})

def labelList(request):
    data = request.GET
    id = data['id']
    doc = etree.parse("portugal.xml")
    string = "//" + str(id)
    search = doc.xpath(string)
    send = []

    for s in search:
        send.append(s.text)

    #print(set(send))
    return render(request, 'labelList.html', {"send": set(send)})



#def interesseDetail(request):
#    data = request.GET
#    id = data['id']
#    doc = etree.parse("portugal.xml")
#    string = '//interesse[idinteresse="{}"]'.format(id)
#
#    search = doc.xpath(string)
#
#    send = {}
#
#    for s in search:
#        send["nome"] = s.find("nome").text
#        send["tipo"] = s.find("tipo").text
#    return render(request, 'municipioDetail.html', {"send": send})'''

def validateXML(name):
    filename_xml = name
    filename_xsd = "interesses.xsd"
    # open and read schema file
    with open(filename_xsd, 'r') as schema_file:
        schema_to_check = schema_file.read().encode('utf-8')
    # open and read xml file
    with open(filename_xml, 'r') as xml_file:
        xml_to_check = xml_file.read().encode('utf-8')
    xmlschema_doc = etree.parse(BytesIO(schema_to_check))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    # parse xml
    valid = 'XML inválido'
    try:
        doc = etree.parse(BytesIO(xml_to_check))
        print('XML well formed, syntax ok.')
        valid = 'XML válido'
    # check for file IO error
    finally:
        valid = 'XML inválido'
        try:
            xmlschema.assertValid(doc)
            print('XML valid, schema validation ok.')
            valid = 'XML válido'
        finally:
            return valid



