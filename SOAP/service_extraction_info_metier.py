import logging
import sys
from spyne import ServiceBase, Unicode, Application, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
import xml.etree.ElementTree as ET
from suds.client import Client
from suds import WebFault


class ServiceExtractionInformation(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def ExtraireInformations(ctx, demande_xml):
        informations_structurees = ExtractionInfo(demande_xml)
        nom_client=stockage_information(informations_structurees)
        xml_db = find_db_client(nom_client)
        #tree = lecture_bdd(xml_db)
        print('Demande de prêt enregistrée avec succès')
        #tree = to_service_verification_solvabilite()
        return xml_db #tree


def ExtractionInfo(demande_xml):
    root = ET.parse(demande_xml).getroot()
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
            'Tranquilite': description_propriete_tranquilite
        },
        'RevenuMensuel': revenu_mensuel,
        'DepensesMensuelles': depenses_mensuelles
    }
    return informations_structurees


def stockage_information(informations_structurees):
    root = ET.Element('DemandePret')
    prenom_client = ET.SubElement(root, 'PrenomClient')
    prenom_client.text = informations_structurees['PrenomClient']
    nom_client = ET.SubElement(root, 'NomClient')
    nom_client.text = informations_structurees['NomClient']
    adresse = ET.SubElement(root, 'Adresse')
    adresse_rue = ET.SubElement(adresse, 'Rue')
    adresse_rue.text = informations_structurees['Adresse']['Rue']
    adresse_ville = ET.SubElement(adresse, 'Ville')
    adresse_ville.text = informations_structurees['Adresse']['Ville']
    adresse_code_postal = ET.SubElement(adresse, 'CodePostal')
    adresse_code_postal.text = informations_structurees['Adresse']['CodePostal']
    adresse_pays = ET.SubElement(adresse, 'Pays')
    adresse_pays.text = informations_structurees['Adresse']['Pays']
    email = ET.SubElement(root, 'Email')
    email.text = informations_structurees['Email']
    numero_telephone = ET.SubElement(root, 'NumeroTelephone')
    numero_telephone.text = informations_structurees['NumeroTelephone']
    montant_pret_demande = ET.SubElement(root, 'MontantPretDemande')
    montant_pret_demande.text = str(informations_structurees['MontantPretDemande'])
    duree_pret = ET.SubElement(root, 'DureePret')
    duree_pret.text = str(informations_structurees['DureePret'])
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
    revenu_mensuel = ET.SubElement(root, 'RevenuMensuel')
    revenu_mensuel.text = str(informations_structurees['RevenuMensuel'])
    depenses_mensuelles = ET.SubElement(root, 'DepensesMensuelles')
    depenses_mensuelles.text = str(informations_structurees['DepensesMensuelles'])
    tree = ET.ElementTree(root)
    tree.write(f'demande_pret_{nom_client.text}.xml')
    return nom_client.text

def find_db_client(nom_client):
    return f'demande_pret_{nom_client}.xml'


def lecture_bdd(xml_db):

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
            'Tranquilite': description_propriete_tranquilite
        },
        'RevenuMensuel': revenu_mensuel,
        'DepensesMensuelles': depenses_mensuelles
    }
    return informations_structurees

if __name__ == '__main__':
    application = Application([ServiceExtractionInformation],
                              tns='ServiceExtractionInformation',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'ServiceExtractionInformation')
    ]

    sys.exit(run_twisted(twisted_apps, 8000))
