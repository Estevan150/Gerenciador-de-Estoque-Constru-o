# usuarios/models.py - Versão Final com Correção do SystemCheckError

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as _

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

    # --- CORREÇÃO PARA O SystemCheckError ---
    # Adicionamos os campos ManyToMany com um 'related_name' único para evitar conflitos.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="user",
    )
    # ----------------------------------------

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_staff = True

        super().save(*args, **kwargs)

        if not self.is_superuser:
            self.user_permissions.clear()
            codinomes_permissoes = []

            if self.role == UserRole.MESTRE_DE_OBRAS:
                codinomes_permissoes = [
                    'view_material', 'add_requisicao', 'view_requisicao', 
                    'change_requisicao', 'delete_requisicao'
                ]
            elif self.role == UserRole.ALMOXARIFE:
                codinomes_permissoes = [
                    'add_material', 'change_material', 'delete_material', 'view_material',
                    'view_requisicao', 'change_requisicao',
                    'add_saidamaterial', 'view_saidamaterial',
                    'view_notafiscalentrada',
                ]
            elif self.role == UserRole.ENGENHEIRO:
                codinomes_permissoes = [
                    'view_material', 'add_requisicao', 'view_requisicao', 
                    'change_requisicao', 'delete_requisicao',
                    'view_saidamaterial', 'view_notafiscalentrada',
                ]

            for codename in set(codinomes_permissoes):
                try:
                    permissao = Permission.objects.get(codename=codename)
                    self.user_permissions.add(permissao)
                except Permission.DoesNotExist:
                    print(f"AVISO: Permissão com codinome '{codename}' não foi encontrada.")

    @property
    def pode_importar_xml(self):
        return self.role in [UserRole.ADMIN, UserRole.ALMOXARIFE]

    @property
    def is_admin_role(self):
        return self.role == UserRole.ADMIN