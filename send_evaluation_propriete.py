import requests
import xml.etree.ElementTree as ET

def lecture_bdd(xml_db='demande_pret_Doe.xml'):
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
    description_propriete_annnee_construction = int(description_propriete_annnee_construction.text) if description_propriete_annnee_construction is not None else 0
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

def to_service_evaluation_propiete(xml_db='demande_pret_Doe.xml'):
    informations_structurees = lecture_bdd(xml_db)
    
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
    description_propriete_annnee_construction.text = str(informations_structurees['DescriptionPropriete']['AnneeConstruction'])
    tree = ET.tostring(root)
    tree = tree.decode('utf-8')

    return tree


if __name__ == '__main__':
    headers = {'Content-Type': 'application/xml'}
    url = 'http://127.0.0.1:8003/evaluation-propriete'
    
    xml_db = 'demande_pret_Doe.xml'
    data = to_service_evaluation_propiete(xml_db)
    
    try:
        # Appelez la méthode du service en lui passant le XML comme argument
        response = requests.post(url, data=data.encode('utf-8'), headers=headers)
        # Vérifiez la réponse du service
        print("Réponse du service evealuation propriete:")
        print(response)
    except requests.exceptions.RequestException as e:
        print(e)