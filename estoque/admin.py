# estoque/admin.py

from django.contrib import admin
from .models import (
    Fornecedor, Material, NotaFiscalEntrada, 
    ItemNotaFiscal, SaidaMaterial, Requisicao, ItemRequisicao
)
from usuarios.models import UserRole

# --- INÍCIO DA CUSTOMIZAÇÃO ---

class ItemRequisicaoInline(admin.TabularInline):
    model = ItemRequisicao
    extra = 1 

@admin.register(Requisicao)
class RequisicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitante', 'data_requisicao', 'status')
    list_filter = ('status', 'data_requisicao')
    inlines = [ItemRequisicaoInline]

    def get_queryset(self, request):
        """
        Esta é a função mágica! Ela customiza o que cada usuário vê na lista.
        """
        queryset = super().get_queryset(request)

        # Se o usuário não for superuser (admin geral), filtramos o que ele pode ver
        if not request.user.is_superuser:

            # --- MUDANÇA AQUI ---
            # Verificamos se o perfil é Mestre de Obras OU Engenheiro
            if request.user.role in [UserRole.MESTRE_DE_OBRAS, UserRole.ENGENHEIRO]:
                # Se for um desses dois perfis, ele só vê as requisições que ele mesmo criou.
                return queryset.filter(solicitante=request.user)
            # ---------------------

        # Se for Admin ou Almoxarife (ou qualquer outro caso não tratado), ele vê tudo.
        return queryset

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'unidade_medida', 'estoque_atual')
    search_fields = ('codigo', 'descricao')

admin.site.register(Fornecedor)
admin.site.register(NotaFiscalEntrada)
admin.site.register(ItemNotaFiscal)
admin.site.register(SaidaMaterial)