from django.shortcuts import render

from .models import Maison

from os import listdir
from os.path import isfile, join

initPetrol = 20
initEau = 20
initBois = 20
initMine = 20

listeRessourcesSession = [
    ("toit", lambda request: request.session['toit']),
    ("mur", lambda request: request.session['mur']),
    ("porte", lambda request: request.session['porte']),
]

indexListeRessourcesSession = {
    "toit": 0, "mur": 1, "porte": 2#, "fenetre": 3
}

def concatDict(dic1, dic2):
    res = dict(dic1)
    res.update(dic2)
    return res

def returnRequest(request):
    return {
        'petrol': request.session['petrol'],
        'eau': request.session['eau'],
        'bois': request.session['bois'],
        'mine': request.session['mine'],
    }

def getListeRessourcesSession(request):
    res = []
    for i in listeRessourcesSession:
        if 1 == request.session[i[0]]:
            res.append(i[0])
    return res

def getListeElement(nomElment):
    imgs = [f for f in listdir(nomElment) if isfile(join(nomElment, f))]
    res = []
    for i in imgs:
        if ".txt" in i:
            nom = i[0:-4]
            for j in imgs:
                if nom in j and not ".txt" in j:
                    res.append([j, getCaracteristiques(nomElment + "/" + i)])
    return res

def getCaracteristiques(nomFichier):
    res = {}
    with open(nomFichier, "r") as fd:
        data = fd.read()
        lines = data.split("\n")
        for l in lines:
            if 0 != len(l):
                tmp = l.split(":")
                res[tmp[0]] = tmp[1]
    return res

def index(request):
    # Ressources
    request.session['petrol'] = initPetrol
    request.session['eau'] = initEau
    request.session['bois'] = initBois
    request.session['mine'] = initMine
    request.session['maison'] = "base.png"

    # Element de la construction restante
    request.session['toit'] = 1
    request.session['mur'] = 1
    request.session['porte'] = 1
    request.session['fenetre'] = 1

    return render(request, 'houseBuilder/index.html', {})

def construction(request):
    if request.method == 'GET':
        resDic = returnRequest(request)
        resDic["element"] = listeRessourcesSession[0][0]
        element_maison = []
        for i in listeRessourcesSession:
            if i[1](request) == 1:
                element_maison.append([i[0].capitalize(), "elements/" + i[0] + ".png"])

        resDic = concatDict(resDic, {'maison': request.session['maison'], 'element_maison': element_maison})
        if len(element_maison) == 0:
            return render(request, 'houseBuilder/win.html', resDic)
        return render(request, 'houseBuilder/construction.html', resDic)

def listeElements(request):
    element = ""
    if request.method == 'GET':
        element = getListeRessourcesSession(request)[0]
    else:
        element = getListeRessourcesSession(request)[int(request.POST["nbSend"])]
    res = {'elements': getListeElement(element), 'typeElement': element}
    res = concatDict(res, returnRequest(request))
    return render(request, 'houseBuilder/listeElements.html', res)

def ressources(request):
    if request.method == 'GET':
        return render(request, 'houseBuilder/ressources.html', {})
    # Assignation des matières restantes
    res = {}
    if request.session['maison'] == "base.png":
        request.session['maison'] = "elements/" + request.POST["fichier"]
    else:
        request.session['maison'] += request.POST["fichier"]
    request.session['maison'] = request.session['maison'].replace("jpg", "png")
    tabRessources = ['petrol', 'eau', 'bois', 'mine']
    for i in tabRessources:
        res[i + "_delete"] = int(request.POST[i])
        res[i + "_solde"] = request.session[i]
    for i in tabRessources:
        if i in request.POST:
            request.session[i] -= int(request.POST[i])
        else:
            print("----> Erreur " + i + " n'est pas dans la page ressources")

    for i in listeRessourcesSession:
        if i[0] == request.POST["typeElement"]:
            request.session[i[0]] = 0

    resDic = returnRequest(request)
    resDic = concatDict(resDic, res)
    return render(request, 'houseBuilder/ressources.html', resDic)

def lose(request):
    return render(request, 'houseBuilder/lose.html', {})

def win(request):
    return render(request, 'houseBuilder/win.html', {})
