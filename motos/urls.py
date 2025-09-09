from django.urls import path
from . import views

app_name = 'motos'

urlpatterns = [
    # Páginas principais
    path('', views.lista_motos, name='lista'),
    path('<int:moto_id>/', views.detalhe_moto, name='detalhe'),
    path('criar/', views.criar_moto, name='criar'),
    path('<int:moto_id>/editar/', views.editar_moto, name='editar'),
    path('<int:moto_id>/excluir/', views.excluir_moto, name='excluir'),

    # Perfil da moto
    path('<int:moto_id>/perfil/', views.perfil_moto, name='perfil'),

    # Rotas da moto
    path('<int:moto_id>/rotas/', views.rotas_moto, name='rotas'),

    # API
    path('api/', views.api_motos, name='api_lista'),
    path('api/<int:moto_id>/', views.api_moto_detalhes, name='api_detalhes'),
    path('api/<int:moto_id>/atualizar-km/', views.api_atualizar_km, name='api_atualizar_km'),
]
