from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'receitas'

urlpatterns = [
    path('', views.ReceitaListViewHome.as_view(), name='home'),
    path('receitas/categoria/<int:categoria_id>/', views.ReceitaListViewCategoria.as_view(), name='categoria'),
    path('receitas/<int:pk>/', views.ReceitaDetail.as_view(), name='receita'),
    path('receitas/pesquisa/', views.ReceitaListViewPesquisa.as_view(), name='pesquisa'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
