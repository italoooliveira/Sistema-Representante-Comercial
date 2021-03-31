from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('autenticar', views.autenticar, name='autenticar'),
    path('logout', auth_views.LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('usuarios/cadastrar', views.cadastrar_usuario, name='cadastrar-usuario'),
    path('editar/usuario/<int:id_usuario>', views.editar_usuario, name='editar-usuario'),
    path('remover/usuario/<int:id_usuario>', views.excluir_usuario, name='excluir-usuario'),
    path('tipos-empresa/', views.listar_tipos_empresa, name='tipos-empresa'),
    path('tipos-empresa/cadastrar', views.cadastrar_tipo_empresa, name='cadastrar-tipo-empresa'),
    path('editar/tipo_empresa/<int:id_tipo_empresa>', views.editar_tipo_empresa, name='editar-tipo-empresa'),
    path('remover/tipo_empresa/<int:id_tipo_empresa>', views.excluir_tipo_empresa, name='excluir-tipo-empresa'),
    path('minha_empresa/cadastrar', views.cadastrar_minha_empresa, name='cadastrar-minha-empresa'),
    path('editar/minha_empresa/<int:id_minha_empresa>', views.editar_minha_empresa, name='editar-minha-empresa'),
    path('empresas', views.listar_empresas, name='empresas'),
    path('empresas/cadastrar', views.cadastrar_empresa, name='cadastrar-empresa'),
    path('editar/empresa/<int:id_empresa>', views.editar_empresa, name='editar-empresa'),
    path('excluir/empresa/<int:id_empresa>', views.excluir_empresa, name='excluir-empresa'),
    path('clientes/', views.listar_clientes, name='clientes'),
    path('buscar/cliente', views.buscar_dados_clientes, name='buscar-cliente'),
    path('clientes/cadastrar', views.cadastrar_cliente, name='cadastrar-cliente'),
    path('editar/cliente/<int:id_cliente>', views.editar_cliente, name='editar-cliente'),
    path('excluir/cliente/<int:id_cliente>', views.excluir_cliente, name='excluir-cliente'),
    path('prepostos/', views.listar_prepostos, name='prepostos'),
    path('prepostos/cadastrar/', views.cadastrar_preposto, name='cadastrar-preposto'),
    path('editar/preposto/<int:id_preposto>', views.editar_preposto, name='editar-preposto'),
    path('remover/preposto/<int:id_preposto>', views.excluir_preposto, name='excluir-preposto'),
    path('rotas-prepostos', views.listar_rotas_prepostos, name='rotas-prepostos'),
    path('rotas-prepostos/retorna_informacoes_preposto', views.retorna_informacoes_preposto, name='retorna-informacoes-preposto'),
    path('rotas-prepostos/cadastrar', views.cadastrar_rotas_prepostos, name='cadastrar-rotas-prepostos'),
    path('rotas-prepostos/retorna_informacoes_rota_prepostos/<int:id_rota>', views.retorna_informacoes_rota_prepostos, name='retorna-informacoes-rota-prepostos'),
    path('editar/rota/<int:id_rota>', views.editar_rotas_prepostos, name='editar-rota'),
    path('remover/rota/<int:id_rota>', views.excluir_rota, name='excluir-rota'),
    path('contatos', views.listar_contatos, name='contatos'),
    path('contatos/cadastrar', views.cadastrar_contato, name='cadastrar-contato'),
    path('editar/contato/<int:id_contato>', views.editar_contato, name='editar-contato'),
    path('remover/contato/<int:id_contato>', views.excluir_contato, name='excluir-contato'),
    path('categorias/', views.listar_categorias, name='categorias'),
    path('categorias/cadastrar', views.cadastrar_categoria, name='cadastrar-categoria'),
    path('editar/categoria/<int:id_categoria>', views.editar_categoria, name='editar-categoria'),
    path('remover/categoria/<int:id_categoria>', views.excluir_categoria, name='excluir-categoria'),
    path('unidades-venda/', views.listar_unidades_venda, name='unidades-venda'),
    path('unidades-venda/cadastrar', views.cadastrar_unidade_venda, name='cadastrar-unidade-venda'),
    path('editar/unidade_venda/<int:id_unidade_venda>', views.editar_unidade_venda, name='editar-unidade-venda'),
    path('remover/unidade_venda/<int:id_unidade_venda>', views.excluir_unidade_venda, name='excluir-unidade-venda'),
    path('tipos-embalagem/', views.listar_tipos_embalagem, name='tipos-embalagem'),
    path('tipos-embalagem/cadastrar', views.cadastrar_tipo_embalagem, name='cadastrar-tipo-embalagem'),
    path('editar/tipo_embalagem/<int:id_tipo_embalagem>', views.editar_tipo_embalagem, name='editar-tipo-embalagem'),
    path('remover/tipo_embalagem/<int:id_tipo_embalagem>', views.excluir_tipo_embalagem, name='excluir-tipo-embalagem'),
    path('produtos', views.listar_produtos, name='produtos'),
    path('produtos/cadastrar', views.cadastrar_produto, name='cadastrar-produto'),
    path('editar/produto/<int:id_produto>', views.editar_produto, name='editar-produto'),
    path('remover/produto/<int:id_produto>', views.excluir_produto, name='excluir-produto'),
    path('formas-pagamento/', views.listar_formas_pagamento, name='formas-pagamento'),
    path('formas-pagamento/cadastrar', views.cadastrar_forma_pagamento, name='cadastrar-forma-pagamento'),
    path('editar/forma_pagamento/<int:id_forma_pagamento>', views.editar_forma_pagamento, name='editar-forma-pagamento'),
    path('remover/forma_pagamento/<int:id_forma_pagamento>', views.excluir_forma_pagamento, name='excluir-forma-pagamento'),
    path('pedidos/', views.listar_pedidos, name='pedidos'),
    path('pedidos/cadastrar', views.cadastrar_pedido, name='cadastrar-pedido'),
    path('pedidos/confirmar_itens_pedido/<int:id_pedido>', views.confirmar_itens_pedido, name='confirmar-itens-pedido'),
    path('editar/pedido/<int:id_pedido>', views.editar_pedido, name='editar-pedido'),
    path('cadastrar/itens_pedido/<int:id_pedido>', views.cadastrar_itens_pedido, name='cadastrar-itens-pedido'),
    path('pedidos/retorna_informacoes_itens_pedido/<int:id_pedido>', views.retorna_informacoes_itens_pedido, name='retorna-informacoes-itens-pedido'),
    path('editar/itens_pedido/<int:id_pedido>', views.editar_itens_pedido, name='editar-itens-pedido'),
    path('remover/pedido/<int:id_pedido>', views.excluir_pedido, name='excluir-pedido'),
    path('gerar-pdf/pedido/<int:id_pedido>', views.gerar_pdf_pedido, name='gerar-pdf-pedido'),
    path('tendencias', views.acompanhamentos, name='acompanhamentos'),
    path('tendencias/cadastrar', views.cadastrar_acompanhamento, name='cadastrar-acompanhamento'),
    path('editar/tendencia/<int:id_acompanhamento>', views.editar_acompanhamento, name='editar-acompanhamento'),
    path('excluir/tendencia/<int:id_acompanhamento>', views.excluir_acompanhamento, name='excluir-acompanhamento'),
    path('prospecoes-clientes', views.prospeccoes_clientes, name="prospeccoes-clientes"),
    path('clientes-sem-pedido', views.clientes_sem_pedido, name="clientes-sem-pedido"),
    path('cancelamentos-pedidos-por-cliente', views.cancelamento_pedidos_por_cliente, name="cancelamentos-pedidos-clientes"),
    path('tarefas', views.listar_tarefas, name='tarefas'),
    path('tarefas/cadastrar', views.cadastrar_tarefa, name='cadastrar-tarefa'),
    path('editar/tarefa/<int:id_tarefa>', views.editar_tarefa, name="editar-tarefa"),
    path('excluir/tarefa<int:id_tarefa>', views.excluir_tarefa, name="excluir-tarefa"),
    path('configuracoes/pedidos', views.configuracoes_pedidos, name="configuracoes-pedidos"),
    path('ofertas', views.criar_oferta, name='ofertas'),
    path('ofertas/retorna_informacoes_produtos_empresa', views.retorna_informacoes_produtos_empresa, name='retorna-informacoes-produtos-empresa')
]
