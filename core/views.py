from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout # Renomeado para evitar conflito
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import FavoriteCity
from .services import get_weather_data
# Removido forms daqui, pois não são usados diretamente nestas views por enquanto,
# exceto os de autenticação que já estão sendo importados diretamente.

@login_required
def home_view(request):
    weather_context = None
    favorite_cities = FavoriteCity.objects.filter(user=request.user).order_by('name')
    last_searched_city = request.session.get('last_searched_city', None)

    if request.method == 'POST':
        if 'search_city' in request.POST:
            city_name = request.POST.get('city_name')
            if city_name:
                weather_data = get_weather_data(city_name)
                if weather_data and weather_data.get('name'): # Verifica se a API retornou dados válidos
                    weather_context = weather_data
                    request.session['last_searched_city'] = weather_data['name'] # Salva a cidade pesquisada
                elif weather_data and weather_data.get('error'):
                    messages.error(request, weather_data.get('message', 'Erro ao buscar dados da cidade.'))
                else:
                    messages.error(request, f'Não foi possível encontrar dados para "{city_name}". Verifique o nome e tente novamente.')
            else:
                messages.error(request, 'Por favor, digite o nome de uma cidade.')

        elif 'add_favorite' in request.POST:
            city_name_to_add = request.POST.get('city_name_to_add')
            if city_name_to_add:
                if not FavoriteCity.objects.filter(user=request.user, name__iexact=city_name_to_add).exists():
                    FavoriteCity.objects.create(user=request.user, name=city_name_to_add)
                    messages.success(request, f'"{city_name_to_add}" adicionada aos favoritos.')
                else:
                    messages.info(request, f'"{city_name_to_add}" já está nos seus favoritos.')
                return redirect('home') # Redireciona para limpar o POST e recarregar os favoritos
            else:
                messages.error(request, 'Nome da cidade inválido para adicionar aos favoritos.')


        elif 'remove_favorite' in request.POST:
            city_id_to_remove = request.POST.get('city_id_to_remove')
            favorite_city = get_object_or_404(FavoriteCity, id=city_id_to_remove, user=request.user)
            city_name_removed = favorite_city.name
            favorite_city.delete()
            messages.success(request, f'"{city_name_removed}" removida dos favoritos.')
            return redirect('home')

    # Se houver uma cidade pesquisada na sessão (após adicionar aos favoritos, por exemplo), busca o clima dela
    # Ou se uma cidade favorita foi clicada (tratado por GET no template)
    city_to_display = request.GET.get('city', last_searched_city if not weather_context else None)
    if not weather_context and city_to_display:
        weather_data = get_weather_data(city_to_display)
        if weather_data and weather_data.get('name'):
            weather_context = weather_data
            request.session['last_searched_city'] = weather_data['name']


    context = {
        'weather': weather_context,
        'favorite_cities': favorite_cities,
        'current_city_is_favorite': False
    }

    if weather_context and weather_context.get('name'):
        context['current_city_is_favorite'] = favorite_cities.filter(name__iexact=weather_context['name']).exists()

    return render(request, 'core/home.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # Usando o alias
            messages.success(request, 'Registro bem-sucedido! Você está logado.')
            return redirect('home')
        else:
            # Simplificando a mensagem de erro
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user) # Usando o alias
                messages.info(request, f'Bem-vindo de volta, {username}!')
                # Redirecionar para o 'next' ou 'home'
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            # Não precisa de outra mensagem de erro, o form já terá os erros.
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form, 'title': 'Login'})

@login_required
def logout_view(request): # Adicionado @login_required para logout view também
    auth_logout(request) # Usando o alias
    messages.info(request, 'Você foi desconectado.')
    return redirect('login')
