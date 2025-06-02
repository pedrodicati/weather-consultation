from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Poderíamos customizar o UserCreationForm aqui se necessário,
# mas por enquanto vamos usar o padrão nas views.
# Exemplo:
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         fields = UserCreationForm.Meta.fields + ('email',)


# O AuthenticationForm já é bem completo.
