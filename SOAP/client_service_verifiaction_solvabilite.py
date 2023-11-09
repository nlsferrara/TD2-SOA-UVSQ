from suds.client import Client

if __name__ == '__main__':
    client = Client('http://localhost:8001/verifSolvabilite?wsdl', cache=None)
    score = client.service.calculateScore(client.service.getClientId('Doe', 'John'), 1000, 1000)
    print(score)
