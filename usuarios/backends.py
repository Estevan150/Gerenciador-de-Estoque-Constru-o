# usuarios/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User, UserStatus

class StatusCheckBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Tenta autenticar o usuário com as credenciais
        user = super().authenticate(request, username=username, password=password, **kwargs)

        # Se a autenticação falhou (usuário/senha errados) ou o status é ATIVO,
        # não precisamos fazer mais nada aqui.
        if user is None or user.status == UserStatus.ATIVO:
            return user

        # Se chegou aqui, o usuário existe, a senha está certa, mas o status
        # é PENDENTE ou INATIVO. Nesse caso, bloqueamos o login.
        return None
