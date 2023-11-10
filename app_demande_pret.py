from fastapi import FastAPI, Body, UploadFile, File, Request, Response, HTTPException
import xml.etree.ElementTree as ET
import uvicorn
import requests
import json

app = FastAPI()
  
def getExtractInfo(demande_xml):
    headers = {'Content-Type': 'application/xml'}
    url = 'http://127.0.0.1:8001/extract-information'

    try:
        # Appelez la méthode du service en lui passant le XML comme argument
        response = requests.post(url, data=demande_xml.encode('utf-8'), headers=headers)

        # Vérifiez la réponse du service
        print("Réponse de getExtractInfo:")
        print(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        print(e)


def getScoringPret(tree):
    headers = {'Content-Type': 'application/xml'}
    url = 'http://127.0.0.1:8002/verification-solvabilite'

    try:
        # Appelez la méthode du service en lui passant le XML comme argument
        response = requests.post(url, data=tree.encode('utf-8'), headers=headers)

        # Vérifiez la réponse du service
        print("Réponse du service solvabilité:")
        print(f"Response : {response.text}")

        return response.text
    except Exception as e:
        # Gérez d'autres exceptions possibles ici
        print(f"Une erreur s'est produite : {e}")


def getApprobationPret(evalProp, infoClient, scoreSolvabilite):
    headers = {'Content-Type': 'application/xml'}
    url = 'http://127.0.0.1:8004/decision-approbation'
    xml_data = {
        'evalProp': str(evalProp.replace('"', '')),
        'infoClient': str(infoClient),
        'scoreSolvabilite': str(scoreSolvabilite.replace('"', ''))
    }
    print(f"xml_data : {xml_data}")
    try:

        # Appelez la méthode du service en lui passant le XML comme argument
        response = requests.post(url, data=json.dumps(xml_data), headers={'Content-Type': 'application/json'})
        # Vérifiez la réponse du service
        print("Réponse du service approbation:")
        print(f"Response : {response.text}")

        return response.text
    except Exception as e:
        # Gérez d'autres exceptions possibles ici
        print(f"Une erreur s'est produite : {e}")


def getEvalProp(infoProp):
    headers = {'Content-Type': 'application/xml'}
    url = "http://localhost:8003/evaluation-propriete"

    try:

        # Appelez la méthode du service en lui passant le XML comme argument
        response = requests.post(url, data=infoProp.encode('utf-8'), headers=headers)

        # Vérifiez la réponse du service
        print("Réponse du service eval prop:")
        # print l'abre xml de la réponse
        print(f"Response : {response.text}")

        return response.text
    except Exception as e:
        # Gérez d'autres exceptions possibles ici
        print(f"Une erreur s'est produite : {e}")


def lecture_bdd(xml_db):
    xml_db = xml_db.replace('"', '')
    root = ET.parse(xml_db).getroot()
    prenom_client = root.find('.//PrenomClient')
    prenom_client = prenom_client.text if prenom_client is not None else ''
    nom_client = root.find('.//NomClient')
    nom_client = nom_client.text if nom_client is not None else ''
    adresse_rue = root.find('.//Adresse/Rue')
    adresse_rue = adresse_rue.text if adresse_rue is not None else ''
    adresse_ville = root.find('.//Adresse/Ville')
    adresse_ville = adresse_ville.text if adresse_ville is not None else ''
    adresse_code_postal = root.find('.//Adresse/CodePostal')
    adresse_code_postal = adresse_code_postal.text if adresse_code_postal is not None else ''
    adresse_pays = root.find('.//Adresse/Pays')
    adresse_pays = adresse_pays.text if adresse_pays is not None else ''
    email = root.find('.//Email')
    email = email.text if email is not None else ''
    numero_telephone = root.find('.//NumeroTelephone')
    numero_telephone = numero_telephone.text if numero_telephone is not None else ''
    montant_pret_demande = root.find('.//MontantPretDemande')
    montant_pret_demande = int(montant_pret_demande.text) if montant_pret_demande is not None else 0
    duree_pret = root.find('.//DureePret')
    duree_pret = int(duree_pret.text) if duree_pret is not None else 0
    description_propriete_etage = root.find('.//DescriptionPropriete/Etage')
    description_propriete_etage = description_propriete_etage.text if description_propriete_etage is not None else ''
    description_propriete_taille = root.find('.//DescriptionPropriete/Taille')
    description_propriete_taille = description_propriete_taille.text if description_propriete_taille is not None else ''
    description_propriete_jardin = root.find('.//DescriptionPropriete/Jardin')
    description_propriete_jardin = description_propriete_jardin.text if description_propriete_jardin is not None else ''
    description_propriete_quartier = root.find('.//DescriptionPropriete/Quartier')
    description_propriete_quartier = description_propriete_quartier.text if description_propriete_quartier is not None else ''
    description_propriete_tranquilite = root.find('.//DescriptionPropriete/Tranquilite')
    description_propriete_tranquilite = description_propriete_tranquilite.text if description_propriete_tranquilite is not None else ''
    description_propriete_annnee_construction = root.find('.//DescriptionPropriete/AnneeConstruction')
    description_propriete_annnee_construction = int(
        description_propriete_annnee_construction.text) if description_propriete_annnee_construction is not None else 0
    revenu_mensuel = root.find('.//RevenuMensuel')
    revenu_mensuel = int(revenu_mensuel.text) if revenu_mensuel is not None else 0
    depenses_mensuelles = root.find('.//DepensesMensuelles')
    depenses_mensuelles = int(depenses_mensuelles.text) if depenses_mensuelles is not None else 0
    informations_structurees = {
        'PrenomClient': prenom_client,
        'NomClient': nom_client,
        'Adresse': {
            'Rue': adresse_rue,
            'Ville': adresse_ville,
            'CodePostal': adresse_code_postal,
            'Pays': adresse_pays
        },
        'Email': email,
        'NumeroTelephone': numero_telephone,
        'MontantPretDemande': montant_pret_demande,
        'DureePret': duree_pret,
        'DescriptionPropriete': {
            'Etage': description_propriete_etage,
            'Taille': description_propriete_taille,
            'Jardin': description_propriete_jardin,
            'Quartier': description_propriete_quartier,
            'Tranquilite': description_propriete_tranquilite,
            'AnneeConstruction': description_propriete_annnee_construction
        },
        'RevenuMensuel': revenu_mensuel,
        'DepensesMensuelles': depenses_mensuelles
    }
    return informations_structurees


def to_service_verification_solvabilite(lecture_xml_db):
    informations_structurees = lecture_xml_db

    root = ET.Element('DemandePret')
    prenom_client = ET.SubElement(root, 'PrenomClient')
    prenom_client.text = informations_structurees['PrenomClient']
    nom_client = ET.SubElement(root, 'NomClient')
    nom_client.text = informations_structurees['NomClient']
    revenu_mensuel = ET.SubElement(root, 'RevenuMensuel')
    revenu_mensuel.text = str(informations_structurees['RevenuMensuel'])
    depenses_mensuelles = ET.SubElement(root, 'DepensesMensuelles')
    depenses_mensuelles.text = str(informations_structurees['DepensesMensuelles'])
    tree = ET.tostring(root)
    return tree.decode('utf-8')


def to_service_evaluation_propriete(lecture_xml_db):
    informations_structurees = lecture_xml_db

    root = ET.Element('DemandePret')
    adresse = ET.SubElement(root, 'Adresse')
    adresse_rue = ET.SubElement(adresse, 'Rue')
    adresse_rue.text = informations_structurees['Adresse']['Rue']
    adresse_ville = ET.SubElement(adresse, 'Ville')
    adresse_ville.text = informations_structurees['Adresse']['Ville']
    adresse_code_postal = ET.SubElement(adresse, 'CodePostal')
    adresse_code_postal.text = informations_structurees['Adresse']['CodePostal']
    adresse_pays = ET.SubElement(adresse, 'Pays')
    adresse_pays.text = informations_structurees['Adresse']['Pays']
    montant_pret_demande = ET.SubElement(root, 'MontantPretDemande')
    montant_pret_demande.text = str(informations_structurees['MontantPretDemande'])
    description_propriete = ET.SubElement(root, 'DescriptionPropriete')
    description_propriete_etage = ET.SubElement(description_propriete, 'Etage')
    description_propriete_etage.text = informations_structurees['DescriptionPropriete']['Etage']
    description_propriete_taille = ET.SubElement(description_propriete, 'Taille')
    description_propriete_taille.text = informations_structurees['DescriptionPropriete']['Taille']
    description_propriete_jardin = ET.SubElement(description_propriete, 'Jardin')
    description_propriete_jardin.text = informations_structurees['DescriptionPropriete']['Jardin']
    description_propriete_quartier = ET.SubElement(description_propriete, 'Quartier')
    description_propriete_quartier.text = informations_structurees['DescriptionPropriete']['Quartier']
    description_propriete_tranquilite = ET.SubElement(description_propriete, 'Tranquilite')
    description_propriete_tranquilite.text = informations_structurees['DescriptionPropriete']['Tranquilite']
    description_propriete_annnee_construction = ET.SubElement(description_propriete, 'AnneeConstruction')
    description_propriete_annnee_construction.text = str(
        informations_structurees['DescriptionPropriete']['AnneeConstruction'])
    tree = ET.tostring(root)
    tree = tree.decode('utf-8')

    return tree


def to_service_approbation_pret(lecture_xml_db):
    informations_structurees = lecture_xml_db

    root = ET.Element('DemandePret')
    revenu_mensuel = ET.SubElement(root, 'RevenuMensuel')
    revenu_mensuel.text = str(informations_structurees['RevenuMensuel'])
    depenses_mensuelles = ET.SubElement(root, 'DepensesMensuelles')
    depenses_mensuelles.text = str(informations_structurees['DepensesMensuelles'])
    montant_pret_demande = ET.SubElement(root, 'MontantPretDemande')
    montant_pret_demande.text = str(informations_structurees['MontantPretDemande'])
    duree_pret_demande = ET.SubElement(root, 'DureePret')
    duree_pret_demande.text = str(informations_structurees['DureePret'])
    tree = ET.tostring(root)
    tree = tree.decode('utf-8')

    return tree

@app.post("/submit")
def submit(demande_xml: str = Body()):
    print(f"Requête reçue : {demande_xml}")
    try:
        xml_db = getExtractInfo(demande_xml)
        infoClient = lecture_bdd(xml_db)
        infoClientSolv = to_service_verification_solvabilite(infoClient)
        scoreSolvabilite = getScoringPret(infoClientSolv)

        tree_eval_prop = to_service_evaluation_propriete(infoClient)
        eval_prop = getEvalProp(tree_eval_prop)

        infoClientAprob = to_service_approbation_pret(infoClient)
        print(f"infoClientAprob : {infoClientAprob}")
        approbationPret = getApprobationPret(eval_prop, infoClientAprob, scoreSolvabilite)

        return approbationPret
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        # Vous pouvez retourner une valeur ou un message d'erreur personnalisé ici

if __name__ == '__main__':
    uvicorn.run(app, port=8000)