import xml.etree.ElementTree as ET
from fastapi import FastAPI
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/demande-pret")
async def demande_pret(data: bytes):
    # Convertissez les données du fichier en un objet Python
    tree = ET.parse(data)
    root = tree.getroot()

    # Récupérez les informations de la demande de prêt
    montant = root.attrib["montant"]
    durée = root.attrib["durée"]
    taux = root.attrib["taux"]

    # Créez la réponse du service
    response = {
        "montant": montant,
        "durée": durée,
        "taux": taux,
    }

    return response

if __name__ == '__main__':
    # Le chemin du dossier que vous souhaitez surveiller
    dossier = 'demande_pret/'

    # Créez un gestionnaire d'événements personnalisé pour surveiller les ajouts de fichiers
    class fileEvenements(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return  print(f"Le dossier {event.src_path} n'est pas un dossier valide.")
            print(f"Le fichier {event.src_path} a été créé.")

            # Récupérez le chemin du fichier créé
            data = event.src_path

            # Envoyez la demande de prêt au service FastAPI
            response = app.post("/demande-pret", data=data)

            # Imprimez la réponse du service
            print(response)

    observateur = Observer()
    observateur.schedule(fileEvenements(), path=dossier, recursive=False)

    observateur.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observateur.stop()

    observateur.join()
