# usuarios/admin.py
import uuid
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .models import User, UserRole

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'status')
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Customizados', {'fields': ('role', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Customizados', {'fields': ('role', 'status')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Sobrescrevemos o método de salvar para adicionar nossa lógica customizada.
        'change' é False quando o objeto está sendo criado e True quando está sendo editado.
        """
        # Se o usuário está sendo CRIADO (não é uma edição)
        if not change:
            # 1. Gera um token de aprovação único
            obj.approval_token = uuid.uuid4()

            # 2. Chama a função para enviar o e-mail de aprovação
            # (Passamos 'request' para que possamos construir a URL completa depois)
            self._enviar_email_aprovacao_com_link(request, obj)

        # Continua com o processo de salvar padrão do Django
        super().save_model(request, obj, form, change)

    def _enviar_email_aprovacao_com_link(self, request, usuario_pendente):
        """
        Função auxiliar para montar e enviar o e-mail com o link de aprovação.
        """
        # Busca todos os admins ativos para notificar
        admins = User.objects.filter(role=UserRole.ADMIN, status='ATIVO')
        lista_emails_admin = [admin.email for admin in admins if admin.email]

        if not lista_emails_admin:
            return

        # Monta a URL de aprovação
        # (Ainda não criamos essa URL, mas já vamos deixar preparado)
        token = usuario_pendente.approval_token
        # A função 'reverse' cria a URL a partir do nome que daremos a ela em urls.py
        # A função 'request.build_absolute_uri' transforma a URL relativa em uma completa (com http://...)
        caminho_aprovacao = reverse('aprovar_usuario', kwargs={'token': token})
        link_aprovacao = request.build_absolute_uri(caminho_aprovacao)

        # Prepara e envia o e-mail
        assunto = f"Aprovação Necessária: Novo Usuário {usuario_pendente.username}"
        mensagem = (
            f"Olá, Administrador.\n\n"
            f"O usuário '{usuario_pendente.username}' está aguardando aprovação.\n\n"
            f"Para aprovar o acesso, por favor clique no link abaixo:\n"
            f"{link_aprovacao}\n\n"
            f"Se o link não funcionar, por favor acesse o painel de administração e ative o usuário manualmente."
        )
        remetente = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@sgac.com')

        send_mail(assunto, mensagem, remetente, lista_emails_admin)
        print(f"E-mail de APROVAÇÃO sobre '{usuario_pendente.username}' enviado para {len(lista_emails_admin)} admin(s).")

# A linha de registro continua a mesma
admin.site.register(User, CustomUserAdmin)
