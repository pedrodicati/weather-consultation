from django.db import models
from django.contrib.auth.models import User

class FavoriteCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        # Garante que um usuário não possa adicionar a mesma cidade duas vezes
        unique_together = ('user', 'name')
