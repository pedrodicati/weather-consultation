import requests

# entre no site e pegue sua chave própria
# https://openweathermap.org

KEY = open("key.txt", "r").read()
URL = "http://api.openweathermap.org/data/2.5/weather"

CITY = str(input("Digite a cidade: "))

request = requests.get(URL, params={"q": CITY,          # cidade em que quer consultar a previsão
                                    "appid": KEY,       # chave de acesso à API
                                    "units": "metric",  # pega os dados em celsius
                                    "lang": "pt_br"})   # traz em pt-br os dados

if (request.status_code == 200): # codigo 200 significa que a solicitação deu certo 
    
    weather = request.json() # transforma a requisição em um dicionário
    
    name        = weather['name']
    temperature = weather['main']['temp']
    description = weather['weather'][0]['description']
    
    print(f"\nCidade: {name}\nTemperatura: {temperature}\nDescrição: {description}")
else:
    print(f"\nErro: {request.status_code}")