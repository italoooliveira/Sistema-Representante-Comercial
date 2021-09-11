from rest_framework import viewsets
from representacao.models import *
from api.serializers import *


class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer


class UnidadesVendaViewSet(viewsets.ModelViewSet):
    queryset = UnidadesVenda.objects.all()
    serializer_class = UnidadesVendaSerializer


class TiposEmbalagemViewSet(viewsets.ModelViewSet):
    queryset = TiposEmbalagem.objects.all()
    serializer_class = TiposEmpresaSerializer


class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializer
