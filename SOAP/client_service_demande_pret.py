import xml.etree.ElementTree as ET
from suds.client import Client
from suds import WebFault
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

if __name__ == '__main__':
    # Le chemin du dossier que vous souhaitez surveiller
    dossier = 'demande_pret/'

    # Créez un gestionnaire d'événements personnalisé pour surveiller les ajouts de fichiers
    class fileEvenements(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return  print(f"Le dossier {event.src_path} n'est pas un dossier valide.")
            print(f"Le fichier {event.src_path} a été créé.")

            url = "http://localhost:8002/DemandePret?wsdl"
            client = Client(url, cache=None)

            # Récupérez le chemin du fichier créé
            data = event.src_path

            try:
                response = client.service.demandePret(data)

                print("Bonjour, voici ma demande de prêt :")

                tree = ET.parse(data)

                # Convertir l'arbre XML en une chaîne de caractères
                print(ET.tostring(tree.getroot(), encoding='utf-8').decode('utf-8'))

                # Vérifiez la réponse du service
                if response:
                    print("\nRéponse du service DemandePret:")
                    print(response)
                else:
                    print("La réponse du service est vide.")
            except WebFault as e:
                # En cas d'erreur, imprimez le message d'erreur
                print(f"Erreur lors de l'appel au service : {e}")
            except Exception as e:
                print(f"Une erreur s'est produite : {e}")

    observateur = Observer()
    observateur.schedule(fileEvenements(), path=dossier, recursive=False)

    observateur.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observateur.stop()

    observateur.join()
