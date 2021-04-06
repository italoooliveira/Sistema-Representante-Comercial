from api.views.configuracoes import *
from api.views.empresas import *
from api.views.pessoas import *
from api.views.pedidos import *
from api.views.usuarios import *
from api.views.relatorios import *
from api.views.produtos import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('configuracoes', ConfiguracoesViewSet, 'Configuracoes')
router.register('empresas', EmpresasViewSet, 'Empresas')
router.register('minha_empresa', MinhaEmpresaViewSet, 'MinhaEmpresa')
router.register('tipos_empresa', TiposEmpresaViewSet, 'TiposEmpresa')
router.register('clientes', ClientesViewSet, 'Clientes')
router.register('prepostos', PrepostosViewSet, 'Prepostos')
router.register('rotas', RotasViewSet, 'Rotas')
router.register('rotas_prepostos', RotasPrepostosViewSet, 'RotasPrepostos')
router.register('preposto_clientes', PrepostoClientesViewSet, 'PrepostoClientes')
router.register('contatos', ContatosViewSet, 'Contatos')
router.register('formas_pagamento', FormasPagamentoViewSet, 'FormasPagamento')
router.register('pedidos', PedidosViewSet, 'Pedidos')
router.register('itens_pedido', ItensPedidoViewSet, 'ItensPedido')
router.register('categorias', CategoriasViewSet, 'Categorias')
router.register('unidades_venda', UnidadesVendaViewSet, 'UnidadesVenda')
router.register('tipos_embalagem', TiposEmbalagemViewSet, 'TiposEmbalagem')
router.register('produtos', ProdutosViewSet, 'Produtos')
router.register('acompanhamentos', AcompanhamentosViewSet, 'Acompanhamentos')
router.register('acompanhamento_empresa', AcompanhamentoEmpresaViewSet, 'AcompanhamentoEmpresa')
router.register('acompanhamento_preposto_empresa', AcompanhamentoPrepostoEmpresaViewSet, 'AcompanhamentoPrepostoEmpresa')
router.register('usuarios', UsuariosViewSet, 'Usuarios')
router.register('tarefas', TarefasViewSet, 'Tarefas')

urlpatterns = router.urls