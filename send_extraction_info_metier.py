import requests

# data prend la valeur du XML à envoyer 'johndoe.xml'
# Lisez le contenu du fichier XML de la demande
data='johndoe.xml'

body = open(data, 'r').read()
print(body)
headers = {'Content-Type': 'application/xml'}
url = 'http://127.0.0.1:8001/extract-information'

try:
    # Appelez la méthode du service en lui passant le XML comme argument
    response = requests.post(url, data=body.encode('utf-8'), headers=headers)

    # Vérifiez la réponse du service
    print("Réponse du service:")
    print(response)
except requests.exceptions.RequestException as e:
    print(e)
