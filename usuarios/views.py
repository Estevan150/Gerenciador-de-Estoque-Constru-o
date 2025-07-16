# usuarios/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import User, UserStatus

def aprovar_usuario(request, token):
    """
    Esta view procura por um usuário com o token fornecido e, se encontrar,
    muda seu status para ATIVO.
    """
    # Procura por um usuário com o token correspondente ou retorna um erro 404 (Não Encontrado)
    usuario = get_object_or_404(User, approval_token=token)

    # Se encontrou, atualiza o status e limpa o token (para não ser usado de novo)
    usuario.status = UserStatus.ATIVO
    usuario.approval_token = None  # Invalida o token após o uso
    usuario.save()

    # Retorna uma mensagem simples de sucesso na página
    return HttpResponse("<h1>Usuário aprovado com sucesso!</h1><p>Esta conta agora pode acessar o sistema.</p>")


from django.shortcuts import redirect
# ... outros imports e views ...

# Esta view apenas redireciona para nossa página de login nomeada 'login'
def custom_admin_login(request):
    return redirect('login')