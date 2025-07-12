# usuarios/models.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    ENGENHEIRO = 'ENGENHEIRO', 'Engenheiro'
    ALMOXARIFE = 'ALMOXARIFE', 'Almoxarife'
    MESTRE_DE_OBRAS = 'MESTRE_DE_OBRAS', 'Mestre de Obras'

class UserStatus(models.TextChoices):
    ATIVO = 'ATIVO', 'Ativo'
    PENDENTE = 'PENDENTE', 'Pendente'
    INATIVO = 'INATIVO', 'Inativo'

class User(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        verbose_name='Perfil de Usuário'
    )
    status = models.CharField(
        max_length=50,
        choices=UserStatus.choices,
        default=UserStatus.PENDENTE,
        verbose_name='Status da Conta'
    )
    approval_token = models.UUIDField(
        null=True,
        blank=True,
        editable=False
    )

    def __str__(self):
        return self.username

    @property
    def pode_importar_xml(self):
        """Retorna True se o usuário for Admin ou Almoxarife."""
        return self.role in [UserRole.ADMIN, UserRole.ALMOXARIFE]

    @property
    def is_admin_role(self):
        """Retorna True se o perfil do usuário for ADMIN."""
        return self.role == UserRole.ADMIN
    