from django.urls import path
from .views import (listar_refeicoes, cadastrar_refeicao, editar_refeicao, excluir_refeicao, 
                    listar_refeicoes_dia, cadastrar_refeicao_dia, editar_refeicao_dia, excluir_refeicao_dia)

app_name = 'refeicoes'

urlpatterns = [
    path('', listar_refeicoes, name='listar_refeicoes'),
    path('cadastrar-refeicao/', cadastrar_refeicao, name='cadastrar_refeicao'),
    path('editar-refeicao/<int:id>/', editar_refeicao, name='editar_refeicao'),
    path('excluir-refeicao/<int:id>/', excluir_refeicao, name='excluir_refeicao'),

    path('listar-refeicoes-dia/', listar_refeicoes_dia, name='listar_refeicoes_dia'),
    path('cadastrar-refeicao-dia/', cadastrar_refeicao_dia, name='cadastrar_refeicao_dia'),
    path('editar-refeicao-dia/<int:id>/', editar_refeicao_dia, name='editar_refeicao_dia'),
    path('excluir-refeicao-dia/<int:id>/', excluir_refeicao_dia, name='excluir_refeicao_dia'),

]