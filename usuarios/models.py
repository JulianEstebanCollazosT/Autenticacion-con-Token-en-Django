from django.db import models
from django.contrib.auth.models import User
import secrets

class UserToken(models.Model):
    # Creo una tabla para el manejo de tokens
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_token(cls, user):
        token = secrets.token_hex(32)  # Genera un token de 64 caracteres
        user_token = cls.objects.create(user=user, token=token) # Genera un registro en la tabla UserToken
        return user_token.token
