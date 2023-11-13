from fastapi import FastAPI, Body
import uvicorn
import xml.etree.ElementTree as ET

app = FastAPI()

def getInfoClientBureauCredit(idClient):
    dictInfoClient = {}
    client = root.find('.//Client[ID="%s"]' % idClient)
    if client is not None:
        dette = client.find('Dette').text
        dictInfoClient["dette"] = dette

        paiementRetard = client.find('PaiementRetard').text
        dictInfoClient["paiementRetard"] = paiementRetard

        faillite = client.find('Faillite').text
        dictInfoClient["faillite"] = faillite

        return dictInfoClient
    return "Client non trouvé"

def getClientId(nomClient, prenomClient):
    for client in root.findall('Client'):
        prenom = client.find('.//PrenomClient').text
        nom = client.find('.//NomClient').text
        if prenom == prenomClient and nom == nomClient:
            return client.find('ID').text
    return "Client non trouvé"

@app.post("/verification-solvabilite", response_model=str)
def calculateScore(tree2: str = Body()):
    tree2 = ET.fromstring(tree2)
    nom = tree2.find('.//NomClient').text
    prenom = tree2.find('.//PrenomClient').text
    infoClient = getInfoClientBureauCredit(getClientId(nom, prenom))
    print('infoClient ', infoClient)
    revenu = tree2.find('.//RevenuMensuel').text
    depense = tree2.find('.//DepensesMensuelles').text
    score = 0
    # Votre logique de calcul de score ici
    dette = int(infoClient['dette'])
    if dette > 15000:
        score -= 3
    elif dette >= 10000:
        score -= 2
    elif dette >= 5000:
        score -= 1
    elif dette == 0:
        score += 1

    paiementeRetard = int(infoClient['paiementRetard'])
    if paiementeRetard > 3:
        score -= 3
    elif paiementeRetard > 0:
        score -= 1
    elif paiementeRetard == 0:
        score += 1

    faillite = infoClient['faillite']
    if faillite == 'True':
        score -= 5

    if int(revenu) < int(depense) + int(dette):
        score -= 2
    if int(revenu) >= int(depense) + int(dette):
        score += 1

    return str(score)


if __name__ == '__main__':
    tree = ET.parse('bureauCredit.xml')
    root = tree.getroot()
    uvicorn.run(app, port=8002)
