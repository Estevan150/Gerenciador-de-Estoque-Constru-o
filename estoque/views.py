# estoque/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.core.exceptions import PermissionDenied
import os

# Adicionamos os novos formulários e modelos aos imports
from .forms import UploadXMLForm, SaidaMaterialForm, RequisicaoForm, ItemRequisicaoFormSet
from .xml_parser import processar_nfe_xml
from .models import Material, SaidaMaterial, UnidadeMedida, Requisicao
from usuarios.models import UserRole

# ... (as views upload_nfe_view e saida_material_view continuam aqui, sem alterações) ...
@login_required
def upload_nfe_view(request):
    if request.method == 'POST':
        form = UploadXMLForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['xml_file']
            fs = FileSystemStorage()
            filename = fs.save(xml_file.name, xml_file)
            caminho_do_arquivo = fs.path(filename)
            nota_fiscal_processada = processar_nfe_xml(caminho_do_arquivo)
            os.remove(caminho_do_arquivo)
            if nota_fiscal_processada:
                messages.success(request, f'Nota Fiscal nº {nota_fiscal_processada.numero} processada com sucesso!')
            else:
                messages.error(request, 'Ocorreu um erro ao processar o arquivo XML.')
            return redirect('upload_nfe')
    else:
        form = UploadXMLForm()
    return render(request, 'estoque/upload_nfe.html', {'form': form})

@login_required 
@transaction.atomic 
def saida_material_view(request):
    if request.method == 'POST':
        form = SaidaMaterialForm(request.POST)
        if form.is_valid():
            material_selecionado = form.cleaned_data['material']
            quantidade_retirada = form.cleaned_data['quantidade']
            if material_selecionado.estoque_atual >= quantidade_retirada:
                nova_saida = form.save(commit=False)
                nova_saida.usuario = request.user
                nova_saida.save()
                material_selecionado.estoque_atual -= quantidade_retirada
                material_selecionado.save()
                messages.success(request, 'Saída de material registrada com sucesso!')
                return redirect('saida_material')
            else:
                messages.error(request, f'Estoque insuficiente para {material_selecionado.descricao}. '
                                        f'Disponível: {material_selecionado.estoque_atual}')
    else:
        form = SaidaMaterialForm()
    materiais = Material.objects.all()
    return render(request, 'estoque/saida_material.html', {
        'form': form,
        'materiais': materiais
    })

# estoque/views.py

@login_required # Este decorator já garante que só usuários logados acessam
def dashboard_view(request):
    # A verificação de perfil foi removida daqui, permitindo que todos os
    # usuários logados (Mestre de Obras, Almoxarife, etc.) vejam o dashboard.
    # A lógica de mostrar/esconder links no menu já controla o que cada um pode fazer.

    # O resto da lógica para buscar os dados continua exatamente igual
    materiais_agrupados = {}
    unidades = UnidadeMedida.choices
    for sigla, nome_extenso in unidades:
        materiais_da_unidade = Material.objects.filter(unidade_medida=sigla).order_by('descricao')
        if materiais_da_unidade.exists():
            materiais_agrupados[nome_extenso] = materiais_da_unidade

    total_tipos_materiais = Material.objects.count()

    context = {
        'materiais_agrupados': materiais_agrupados,
        'total_tipos_materiais': total_tipos_materiais
    }

    return render(request, 'estoque/dashboard.html', context)


# --- NOSSA NOVA VIEW PARA CRIAR REQUISIÇÕES ---
@login_required
@transaction.atomic
def criar_requisicao_view(request):
    # Apenas Admins e Mestres de Obra podem criar requisições
    if request.user.role not in [UserRole.ADMIN, UserRole.MESTRE_DE_OBRAS]:
        raise PermissionDenied

    # Se o formulário está sendo enviado
    if request.method == 'POST':
        form = RequisicaoForm(request.POST)
        formset = ItemRequisicaoFormSet(request.POST)

        # Valida ambos, o formulário principal e o conjunto de itens
        if form.is_valid() and formset.is_valid():
            # Salva a requisição "pai" para obter um ID
            requisicao = form.save(commit=False)
            requisicao.solicitante = request.user # Define o usuário logado como solicitante
            requisicao.save()

            # Associa os itens à requisição recém-criada e os salva
            formset.instance = requisicao
            formset.save()

            messages.success(request, 'Requisição de material enviada com sucesso!')
            return redirect('criar_requisicao') # Redireciona para a mesma página

    # Se a página está sendo apenas carregada
    else:
        form = RequisicaoForm()
        formset = ItemRequisicaoFormSet()

    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'estoque/criar_requisicao.html', context)
