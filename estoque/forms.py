# estoque/forms.py

from django import forms
# Novo import para o inlineformset_factory
from django.forms import inlineformset_factory
from .models import SaidaMaterial, Material, Requisicao, ItemRequisicao

class UploadXMLForm(forms.Form):
    xml_file = forms.FileField(label='Selecione o arquivo XML da NF-e')

class SaidaMaterialForm(forms.ModelForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(estoque_atual__gt=0),
        label="Material"
    )

    class Meta:
        model = SaidaMaterial
        fields = ['material', 'quantidade', 'data_saida', 'observacao']
        widgets = {
            'data_saida': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

# --- FORMULÁRIOS PARA O NOVO MÓDULO DE REQUISIÇÃO ---

class RequisicaoForm(forms.ModelForm):
    """ Este é o formulário "pai", para a Requisição em si. """
    class Meta:
        model = Requisicao
        # A requisição não precisa de campos visíveis no formulário,
        # pois o solicitante e o status serão definidos automaticamente na view.
        fields = []

# Usamos inlineformset_factory para criar um conjunto de formulários para os Itens.
# Ele vai criar múltiplos formulários de ItemRequisicao ligados a uma única Requisição.
ItemRequisicaoFormSet = inlineformset_factory(
    Requisicao,             # O modelo "pai"
    ItemRequisicao,         # O modelo "filho"
    fields=('material', 'quantidade_solicitada'), # Os campos que queremos no formulário do item
    extra=3,                # Quantos formulários em branco devem aparecer por padrão
    can_delete=False,       # Não vamos permitir que o usuário delete itens nesta tela
    widgets={
        'material': forms.Select(attrs={'class': 'form-select'}),
        'quantidade_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
    }
)
