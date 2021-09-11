from django.urls import path
from . import views

urlpatterns = [
    path('ofertas/', views.criar_oferta, name='ofertas'),
    path('ofertas/gerar-imagem', views.gerar_imagem, name='gerar-imagem-oferta'),
    path('ofertas/retorna_informacoes_produtos_empresa', views.retorna_informacoes_produtos_empresa, name='retorna-informacoes-produtos-empresa')
]