from lxml import etree
from django.shortcuts import render
from BaseXClient import BaseXClient
import xmltodict

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
        for $i in doc("portugal.xml")
        let $dados := $i//municipio
        let $totalpop := sum($dados/populacao)
        let $totalarea := sum($dados/area)
        let $densidadeportugal := $totalpop div $totalarea
        return <portugal>{<totalpop>{xs:integer($totalpop)}</totalpop>, <totalarea>{$totalarea}</totalarea>, <densidadeportugal>{$densidadeportugal}</densidadeportugal>}</portugal>'''
        query = session.query(input)
        response = query.execute()
        query.close()
    finally:
        if session:
            search = xmltodict.parse(response)['portugal']
            infoportugal['totalpop'] = search['totalpop']
            infoportugal['totalarea'] = search['totalarea']
            infoportugal['densidadeportugal'] = search['densidadeportugal']
            session.close()
    return render(request, 'newmain.html', {"send": send, "infoportugal": infoportugal})

def distritos(request):
    doc = etree.parse("portugal.xml")
    search = doc.xpath("//distrito")

    send = {}

    for s in search:
        send[s.find("nomedistrito").text] = s.find("iddistrito").text

    return render(request, 'main.html', {"send": send})

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


    return render(request, 'municipioDetail.html', {"send": send})

def interesseDetail(request):
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    data = request.GET
    id = data['id']
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
    return render(request, 'interesses.html', {"send": ''})

def sobre(request):
    return render(request, 'sobre.html', {"send": ''})

def labelList(request):
    data = request.GET
    id = data['id']
    doc = etree.parse("portugal.xml")
    string = "//" + str(id)
    print(string)
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