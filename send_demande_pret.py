import requests
import xml.etree.ElementTree as ET
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
            
            # Récupérez le chemin du fichier créé
            data = event.src_path
            body = open(data, 'r').read()
            headers = {'Content-Type': 'application/xml'}
            url = 'http://127.0.0.1:8000/submit'

            try:
                response = requests.post(url, data=body.encode('utf-8'), headers=headers)

                print("Bonjour, voici ma demande de prêt :")

                tree = ET.parse(data)

                # Convertir l'arbre XML en une chaîne de caractères
                print(ET.tostring(tree.getroot(), encoding='utf-8').decode('utf-8'))

                # Vérifiez la réponse du service
                if response:
                    print("\nRéponse du service DemandePret:")
                    print(response.text)
                else:
                    print("La réponse du service est vide.")
            except requests.exceptions.RequestException as e:
                print(e)

    observateur = Observer()
    observateur.schedule(fileEvenements(), path=dossier, recursive=False)

    observateur.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observateur.stop()

    observateur.join()
