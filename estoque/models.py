# estoque/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class UnidadeMedida(models.TextChoices):
    UNIDADE = 'UN', 'Unidade'
    QUILOGRAMA = 'KG', 'Quilograma'
    LITRO = 'L', 'Litro'
    METRO = 'M', 'Metro'
    METRO_CUBICO = 'M3', 'Metro Cúbico'


class Fornecedor(models.Model):
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    nome_razao_social = models.CharField(max_length=255, verbose_name="Nome / Razão Social")

    def __str__(self):
        return self.nome_razao_social

    class Meta:
        verbose_name_plural = "Fornecedores"


class Material(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código do Material")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    unidade_medida = models.CharField(
        max_length=2,
        choices=UnidadeMedida.choices,
        default=UnidadeMedida.UNIDADE,
        verbose_name="Unidade de Medida"
    )
    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Estoque Atual")

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

    class Meta:
        verbose_name_plural = "Materiais"


class NotaFiscalEntrada(models.Model):
    numero = models.CharField(max_length=44, unique=True, verbose_name="Número da NF-e")
    data_emissao = models.DateField(verbose_name="Data de Emissão")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='notas_fiscais')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total da Nota")
    data_entrada = models.DateTimeField(auto_now_add=True, verbose_name="Data da Entrada")

    def __str__(self):
        return f"NF-e nº {self.numero} - {self.fornecedor.nome_razao_social}"

    class Meta:
        verbose_name_plural = "Notas Fiscais de Entrada"


class ItemNotaFiscal(models.Model):
    nota_fiscal = models.ForeignKey(NotaFiscalEntrada, on_delete=models.CASCADE, related_name='itens')
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='entradas')
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário")

    def __str__(self):
        return f"Item {self.material.descricao} da NF-e {self.nota_fiscal.numero}"

    @property
    def valor_total_item(self):
        return self.quantidade * self.valor_unitario

    class Meta:
        unique_together = ('nota_fiscal', 'material')
        verbose_name_plural = "Itens de Notas Fiscais"


class SaidaMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name="Material")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade Retirada")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Usuário Responsável")
    data_saida = models.DateTimeField(default=timezone.now, verbose_name="Data da Saída")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação/Destino")

    def __str__(self):
        return f"{self.quantidade} x {self.material.codigo} em {self.data_saida.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Saída de Material"
        verbose_name_plural = "Saídas de Materiais"
        ordering = ['-data_saida']

# --- NOVOS MODELOS PARA A FASE 2 ---

class Requisicao(models.Model):
    class StatusRequisicao(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        APROVADO = 'APROVADO', 'Aprovado'
        REPROVADO = 'REPROVADO', 'Reprovado'

    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requisicoes_feitas', verbose_name="Solicitante")
    aprovador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requisicoes_aprovadas', null=True, blank=True, verbose_name="Aprovador")
    status = models.CharField(max_length=10, choices=StatusRequisicao.choices, default=StatusRequisicao.PENDENTE)
    data_requisicao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Requisição")
    data_aprovacao = models.DateTimeField(null=True, blank=True, verbose_name="Data da Aprovação")

    def __str__(self):
        return f"Requisição nº {self.id} por {self.solicitante.username}"

    class Meta:
        verbose_name = "Requisição"
        verbose_name_plural = "Requisições"
        ordering = ['-data_requisicao']


class ItemRequisicao(models.Model):
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE, related_name='itens')
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantidade_solicitada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade Solicitada")

    def __str__(self):
        return f"{self.quantidade_solicitada} x {self.material.codigo} na Requisição nº {self.requisicao.id}"

    class Meta:
        verbose_name = "Item de Requisição"
        verbose_name_plural = "Itens de Requisição"
        unique_together = ('requisicao', 'material')