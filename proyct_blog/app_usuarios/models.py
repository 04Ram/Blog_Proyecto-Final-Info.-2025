from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# accounts/models.py

class Perfil(models.Model):
    ROLES = (
        ('member', 'Miembro'),
        ('collaborator', 'Colaborador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='member')

    def __str__(self):
        return self.user.username




