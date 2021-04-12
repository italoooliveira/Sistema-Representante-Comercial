from rest_framework import viewsets
from representacao.models import *
from api.serializers import *


class PrepostosViewSet(viewsets.ModelViewSet):
    queryset = Prepostos.objects.all()
    serializer_class = PrepostosSerializer


class RotasViewSet(viewsets.ModelViewSet):
    queryset = Rotas.objects.all()
    serializer_class = RotasSerializer


class RotasPrepostosViewSet(viewsets.ModelViewSet):
    queryset = RotaPrepostos.objects.all()
    serializer_class = RotaPrepostosSerializer


class PrepostoClientesViewSet(viewsets.ModelViewSet):
    queryset = PrepostoClientes.objects.all()
    serializer_class = PrepostosSerializer


class ContatosViewSet(viewsets.ModelViewSet):
    queryset = Contatos.objects.all()
    serializer_class = ContatosSerializer
