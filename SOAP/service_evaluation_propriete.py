import logging
import sys
from spyne import ServiceBase, Unicode, Application, rpc, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
import xml.etree.ElementTree as ET


class ServiceEvaluationPropriete(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def EvaluerPropriete(ctx, demande_pret):
        
        xml_demande_pret = ET.fromstring(demande_pret)

        adresse = xml_demande_pret.find('.//Adresse')
        description_propriete = xml_demande_pret.find('.//DescriptionPropriete')
        montant_pret_demande = xml_demande_pret.find('.//MontantPretDemande').text
        annee_construction = xml_demande_pret.find('.//AnneeConstruction').text

        # 1. Analyse des Données du Marché Immobilier
        valeur_estimee = analyse_donnees_marche_immobilier(adresse, description_propriete, montant_pret_demande)
        
        # 2. Inspection Virtuelle
        valeur_estimee = inspection_virtuelle(valeur_estimee, annee_construction)

        # 3. Conformité Légale et Réglementaire
        litiges_fonciers_en_cours, conforme_reglements_batiment, admissible_pret_immobilier = verifier_conformite_legale(adresse)

        tree = envoie_reponse(litiges_fonciers_en_cours, conforme_reglements_batiment, admissible_pret_immobilier, valeur_estimee)

        return tree


def analyse_donnees_marche_immobilier(adresse, description_propriete, montant_pret_demande):
    """
    <VentesRecentes>
        <Vente>
            <Adresse>
                <Rue>123, rue de la Rue</Rue>
                <Ville>Villeville</Ville>
                <CodePostal>75000</CodePostal>
                <Pays>France</Pays>
            </Adresse>
            <PrixVente>250000</PrixVente>
            <DescriptionPropriete>
                <Etage>2</Etage>
                <Taille>56</Taille>
                <Jardin>True</Jardin>
                <Quartier>Résidentiel</Quartier>
                <Tranquilite>Calme</Tranquilite>    
            </DescriptionPropriete>
        </Vente>
        <Vente>
            <Adresse>
                <Rue>456, avenue de l'Avenue</Rue>
                <Ville>Villeville</Ville>
                <CodePostal>75000</CodePostal>
                <Pays>France</Pays>
            </Adresse>
            <PrixVente>220000</PrixVente>
            <DescriptionPropriete>
                <Etage>1</Etage>
                <Taille>60</Taille>
                <Jardin>False</Jardin>
                <Quartier>Central</Quartier>
                <Tranquilite>Animé</Tranquilite>    
            </DescriptionPropriete>
        </Vente>
    </VentesRecentes>
    """
    xml= 'historique_vente.xml'
    root = ET.parse(xml).getroot()
    for vente in root.findall('Vente'):
        rue = vente.find('./Adresse/Rue')
        rue = rue.text if rue is not None else ''
        ville = vente.find('./Adresse/Ville')
        ville = ville.text if ville is not None else ''
        code_postal = vente.find('./Adresse/CodePostal')
        code_postal = code_postal.text if code_postal is not None else ''
        pays = vente.find('./Adresse/Pays')
        pays = pays.text if pays is not None else ''
        description_propriete_etage = vente.find('./DescriptionPropriete/Etage')
        description_propriete_etage = description_propriete_etage.text if description_propriete_etage is not None else ''
        description_propriete_taille = vente.find('./DescriptionPropriete/Taille')
        description_propriete_taille = description_propriete_taille.text if description_propriete_taille is not None else ''
        description_propriete_jardin = vente.find('./DescriptionPropriete/Jardin')
        description_propriete_jardin = description_propriete_jardin.text if description_propriete_jardin is not None else ''
        description_propriete_quartier = vente.find('./DescriptionPropriete/Quartier')
        description_propriete_quartier = description_propriete_quartier.text if description_propriete_quartier is not None else ''
        description_propriete_tranquilite = vente.find('./DescriptionPropriete/Tranquilite')
        description_propriete_tranquilite = description_propriete_tranquilite.text if description_propriete_tranquilite is not None else ''
        
        prix_vente = vente.find('./PrixVente')
        prix_vente = int(prix_vente.text) if prix_vente is not None else -1
        
        if ville == adresse.find('./Ville').text:
            if description_propriete_etage == description_propriete.find('./Etage').text:
                if description_propriete_taille == description_propriete.find('./Taille').text:
                    if description_propriete_jardin == description_propriete.find('./Jardin').text:
                        if description_propriete_quartier == description_propriete.find('./Quartier').text:
                            if description_propriete_tranquilite == description_propriete.find('./Tranquilite').text:
                                if int(prix_vente) >= int(montant_pret_demande):
                                    return prix_vente

    return 0


def inspection_virtuelle(valeur_estimee, annee_construction):
    # Vous pouvez effectuer une inspection virtuelle de la propriété ici en fonction de l'adresse et de l'année de
    # construction. Vous pouvez utiliser des images satellite ou d'autres sources d'information.

    # Exemple simplifié : si la propriété a plus de 10 ans, réduisez la valeur estimée de 10 %.
    if int(annee_construction) <= 2012:
        valeur_estimee *= 0.9

    return valeur_estimee


def verifier_conformite_legale(adresse):
    # voilà le format du fichier de legislation
    """
    <EvaluationProprieteRequest>
        <Propriete>
            <Adresse>
            <Rue>123, rue de la Rue</Rue>
            <Ville>Villeville</Ville>
            <CodePostal>75000</CodePostal>
            <Pays>France</Pays>
            </Adresse>
            <AnneeConstruction>2010</AnneeConstruction>
            <LitigesFonciersEnCours>false</LitigesFonciersEnCours>
            <ConformeReglementsBatiment>true</ConformeReglementsBatiment>
            <AdmissiblePretImmobilier>true</AdmissiblePretImmobilier>
        </Propriete>
    </EvaluationProprieteRequest>
    """
    litiges_fonciers_en_cours = 'false'
    conforme_reglements_batiment = 'true'
    admissible_pret_immobilier = 'true'
    xml_legislation = 'legislation.xml'
    root = ET.parse(xml_legislation).getroot()
    for propriete in root.findall('Propriete'):
        rue = propriete.find('.//Rue')
        rue = rue.text if rue is not None else ''
        ville = propriete.find('.//Ville')
        ville = ville.text if ville is not None else ''
        code_postal = propriete.find('.//CodePostal')
        code_postal = code_postal.text if code_postal is not None else ''
        pays = propriete.find('.//Pays')
        pays = pays.text if pays is not None else ''
        if rue == adresse.find('.//Rue').text and ville == adresse.find('.//Ville').text and code_postal == adresse.find('.//CodePostal').text and pays == adresse.find('.//Pays').text:
            litiges_fonciers_en_cours = propriete.find('.//LitigesFonciersEnCours')
            litiges_fonciers_en_cours = litiges_fonciers_en_cours.text if litiges_fonciers_en_cours is not None else ''
            conforme_reglements_batiment = propriete.find('.//ConformeReglementsBatiment')
            conforme_reglements_batiment = conforme_reglements_batiment.text if conforme_reglements_batiment is not None else ''
            admissible_pret_immobilier = propriete.find('.//AdmissiblePretImmobilier')
            admissible_pret_immobilier = admissible_pret_immobilier.text if admissible_pret_immobilier is not None else ''
            return litiges_fonciers_en_cours, conforme_reglements_batiment, admissible_pret_immobilier


def envoie_reponse(litiges_fonciers_en_cours, conforme_reglements_batiment, admissible_pret_immobilier,valeur_estimee):
    root = ET.Element('EvaluationProprieteResponse')
    ET.SubElement(root, 'LitigesFonciersEnCours').text = str(litiges_fonciers_en_cours)
    ET.SubElement(root, 'ConformeReglementsBatiment').text = str(conforme_reglements_batiment)
    ET.SubElement(root, 'AdmissiblePretImmobilier').text = str(admissible_pret_immobilier)
    ET.SubElement(root, 'ValeurEstimee').text = str(valeur_estimee)
    tree = ET.tostring(root)
    return tree.decode('utf-8')


if __name__ == '__main__':
    application = Application([ServiceEvaluationPropriete],
                              tns='ServiceEvaluationPropriete',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'ServiceEvaluationPropriete')
    ]

    sys.exit(run_twisted(twisted_apps, 8003))
