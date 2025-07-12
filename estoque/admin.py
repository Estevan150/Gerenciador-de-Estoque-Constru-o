# estoque/admin.py
from django.contrib import admin
from .models import Fornecedor, Material, NotaFiscalEntrada, ItemNotaFiscal, SaidaMaterial

# Apenas registros simples para visualização no admin
admin.site.register(Fornecedor)
admin.site.register(Material)
admin.site.register(NotaFiscalEntrada)
admin.site.register(ItemNotaFiscal)
admin.site.register(SaidaMaterial)