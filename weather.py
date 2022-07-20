import requests

CHAVE = "c44c583615bd2805ebd575b615fd2e86"
URL = "http://api.openweathermap.org/data/2.5/weather"

CIDADE = str(input("Digite a cidade do Brasil: "))
PAIS = "br"

requisicao = requests.get(URL, params={"q": f"{CIDADE},{PAIS}",
                                      "appid": CHAVE,
                                      "units": "metric",
                                      "lang": "pt_br"})

if(requisicao.status_code == 200):
    clima = requisicao.json() # transforma a requisição em um dicionário
    name = clima['name']
    temperatura = clima['main']['temp']
    descricao = clima['weather'][0]['description']
    print(name, temperatura, descricao)