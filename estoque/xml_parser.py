# estoque/xml_parser.py

import xml.etree.ElementTree as ET
from decimal import Decimal
from django.db import transaction
from .models import Fornecedor, Material, NotaFiscalEntrada, ItemNotaFiscal, UnidadeMedida

@transaction.atomic
def processar_nfe_xml(caminho_do_arquivo):
    print(f"--- Iniciando processamento do arquivo: {caminho_do_arquivo} ---")
    
    try:
        tree = ET.parse(caminho_do_arquivo)
        root = tree.getroot()

        prestador_node = root.find('.//prestador')
        if prestador_node is None:
            raise ValueError("Nó do prestador não encontrado no XML.")
        
        cnpj_prestador = prestador_node.find('documento').text
        nome_prestador = prestador_node.find('razao_social').text

        fornecedor, criado = Fornecedor.objects.get_or_create(
            cnpj=cnpj_prestador,
            defaults={'nome_razao_social': nome_prestador}
        )
        if criado:
            print(f"Novo fornecedor criado: {fornecedor.nome_razao_social}")
        else:
            print(f"Fornecedor existente encontrado: {fornecedor.nome_razao_social}")

        nf_node = root.find('.//nfse')
        numero_nf = nf_node.find('numero').text
        data_emissao_nf = nf_node.find('data_emissao').text
        valor_total_str = nf_node.find('valor_total').text
        valor_total_nf = Decimal(valor_total_str.replace('.', '').replace(',', '.'))
        data_formatada = f"{data_emissao_nf[4:]}-{data_emissao_nf[2:4]}-{data_emissao_nf[:2]}"

        nota_fiscal, nf_criada = NotaFiscalEntrada.objects.get_or_create(
            numero=numero_nf,
            defaults={
                'data_emissao': data_formatada,
                'fornecedor': fornecedor,
                'valor_total': valor_total_nf
            }
        )
        
        if not nf_criada:
            print(f"Nota Fiscal nº {nota_fiscal.numero} já existe. O processamento será interrompido.")
            return None

        print(f"Nota Fiscal de Entrada nº {nota_fiscal.numero} salva.")

        print("\n--- Processando Itens ---")
        itens = root.findall('.//item')
        for item_node in itens:
            descricao_item = item_node.find('descricao').text.strip()
            codigo_item = descricao_item[:50] 
            unidade_item_xml = item_node.find('unidade').text.upper()
            quantidade_str = item_node.find('quantidade').text
            valor_unitario_str = item_node.find('valor_unitario').text
            quantidade_item = Decimal(quantidade_str.replace('.', '').replace(',', '.'))
            valor_unitario_item = Decimal(valor_unitario_str.replace('.', '').replace(',', '.'))

            unidade_db = UnidadeMedida.UNIDADE 
            if 'KG' in unidade_item_xml or 'QUILO' in unidade_item_xml:
                unidade_db = UnidadeMedida.QUILOGRAMA
            elif 'LITRO' in unidade_item_xml:
                unidade_db = UnidadeMedida.LITRO
            elif 'M3' in unidade_item_xml or 'METRO CUBICO' in unidade_item_xml:
                unidade_db = UnidadeMedida.METRO_CUBICO
            elif 'METRO' in unidade_item_xml:
                unidade_db = UnidadeMedida.METRO

            material, criado = Material.objects.get_or_create(
                codigo=codigo_item,
                defaults={
                    'descricao': descricao_item,
                    'unidade_medida': unidade_db
                }
            )
            if criado:
                print(f"  - Novo material criado: {material.descricao[:30]}...")
            else:
                print(f"  - Material existente encontrado: {material.descricao[:30]}...")

            ItemNotaFiscal.objects.create(
                nota_fiscal=nota_fiscal, material=material,
                quantidade=quantidade_item, valor_unitario=valor_unitario_item
            )
            print(f"    - Item salvo na nota fiscal.")

            material.estoque_atual += quantidade_item
            material.save()
            print(f"    - Estoque de '{material.codigo}' atualizado para {material.estoque_atual}")

        print("\n--- Processamento concluído com sucesso! ---")
        return nota_fiscal

    except Exception as e:
        print(f"ERRO! Ocorreu um erro inesperado: {e}")
        return None
    