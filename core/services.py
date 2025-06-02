import requests
from django.conf import settings # Para ler a chave da API de settings.py

def get_weather_data(city_name):
    if not settings.OPENWEATHERMAP_API_KEY:
        # Idealmente, logar um erro aqui ou levantar uma exceção mais específica
        print("Chave da API OpenWeatherMap não configurada em settings.py")
        return None

    params = {
        "q": city_name,
        "appid": settings.OPENWEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
    url = "http://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Levanta um HTTPError para respostas ruins (4xx ou 5xx)

        weather_data = response.json()

        # Extrair apenas os dados que realmente vamos usar
        # (ou podemos retornar weather_data completo se preferirmos processar na view)
        main_weather = weather_data.get('weather', [{}])[0]

        return {
            'name': weather_data.get('name'),
            'temperature': weather_data.get('main', {}).get('temp'),
            'description': main_weather.get('description'),
            'icon': main_weather.get('icon') # Adicionando o ícone
        }

    except requests.exceptions.RequestException as e:
        # Logar o erro e/ou notificar
        print(f"Erro na requisição à API OpenWeatherMap: {e}")
        # Poderia retornar uma estrutura de erro padronizada
        # ex: {'error': True, 'message': str(e)}
        return None
    except Exception as e:
        print(f"Erro ao processar dados do tempo: {e}")
        return None
