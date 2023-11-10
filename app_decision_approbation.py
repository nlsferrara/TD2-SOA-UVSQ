from fastapi import FastAPI, Body
import uvicorn
import xml.etree.ElementTree as ET
from typing import Dict

app = FastAPI()

# miltiple input with Body 
@app.post("/decision-approbation")
def approbationPret(data: dict):
    evalProp = data.get('evalProp', '')
    infoClient = data.get('infoClient', '')
    scoreSolvabilite = data.get('scoreSolvabilite', '')
    tree = ET.fromstring(evalProp)
    valeurEstime = tree.find('.//ValeurEstimee').text
    litigesFonciers = tree.find('.//LitigesFonciersEnCours').text
    conformeReglementsBatiment = tree.find('.//ConformeReglementsBatiment').text
    admissiblePretImmobilier = tree.find('.//AdmissiblePretImmobilier').text

    tree2 = ET.fromstring(infoClient)
    montantPret = tree2.find('.//MontantPretDemande').text
    revenuMensuel = tree2.find('.//RevenuMensuel').text
    depenseMensuel = tree2.find('.//DepensesMensuelles').text
    dureePret = tree2.find('.//DureePret').text

    if int(scoreSolvabilite) >= 0:
        if (int(montantPret) / (int(dureePret))) / 12 <= (int(revenuMensuel) - int(depenseMensuel)) * 0.5:
            if int(montantPret) < float(valeurEstime) * 1.3:
                if litigesFonciers == 'false':
                    if conformeReglementsBatiment == 'true':
                        if admissiblePretImmobilier == 'true':
                            return "Pret approuvé"
                        return "Pret refusé (Non admissible au prêt)"
                    return "Pret refusé (Non conforme aux règlements du bâtiment)"
                return "Pret refusé (Litiges fonciers en cours)"
            return "Pret refusé (Valeur du bien trop élevé comparé à l'estimation"
        return "Pret refusé (Montant du prêt trop élevé comparé au revenu)"
    return "Pret refusé (Score de solvabilité trop bas)"


if __name__ == '__main__':
    uvicorn.run(app, port=8004)
