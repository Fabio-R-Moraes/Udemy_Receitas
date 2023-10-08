from django.urls import path
from . import views

app_name = 'autores'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/receita/<int:id>/edit/',
        views.DashboardReceitas.as_view(),
        name='dashboard_receita_edit'
    ),
    path(
        'dashboard/receita/nova/',
        views.DashboardReceitas.as_view(),
        name='dashboard_receita_nova'
    ),
    path(
        'dashboard/receita/delete/',
        views.DashboardReceitaDelete.as_view(),
        name='dashboard_receita_delete'
    ),
    path(
        'profile/<int:id>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
]
