from lxml import etree
from django.shortcuts import render


# Create your views here.

def main(request):
    doc = etree.parse("portugal.xml")
    search = doc.xpath("//distrito")

    send = {}

    for s in search:
        send[s.find("nomedistrito").text] = s.find("iddistrito").text

    return render(request, 'newmain.html', {"send": send})

def distritos(request):
    doc = etree.parse("portugal.xml")
    search = doc.xpath("//distrito")

    send = {}

    for s in search:
        send[s.find("nomedistrito").text] = s.find("iddistrito").text

    return render(request, 'main.html', {"send": send})

def distritoDetail(request):
    data = request.GET
    id = data['id']
    doc = etree.parse("portugal.xml")
    string = '//distrito[iddistrito="{}"]'.format(id)

    search = doc.xpath(string)

    send = {}

    for s in search:
        send["nomedistrito"] = s.find("nomedistrito").text
        municipios = s.findall("municipios/municipio")
        interesses = s.findall("interesses/interesse")

    listanomes = {}
    for x in municipios:
        listanomes[x.find("idmunicipio").text] = x.find("nomeconcelho").text

    listainteresses = {}
    for x in interesses:
        listainteresses[x.find("iddistrito").text] = x.find("nome").text

    send["municipios"] = listanomes
    send["interesses"] = listainteresses
    return render(request, 'distritoDetail.html', {"send": send})

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

    print(set(send))
    return render(request, 'labelList.html', {"send": set(send)})


def interesseDetail(request):
    data = request.GET
    id = data['id']
    doc = etree.parse("portugal.xml")
    string = '//interesse[idinteresse="{}"]'.format(id)

    search = doc.xpath(string)

    send = {}

    for s in search:
        send["nome"] = s.find("nome").text
        send["tipo"] = s.find("tipo").text
    return render(request, 'municipioDetail.html', {"send": send})