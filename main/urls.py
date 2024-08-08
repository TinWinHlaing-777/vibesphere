from django.urls import path
from . import views


urlpatterns = [
    # welcome path
    path('', views.welcome_view, name='welcome'),
    # auth paths
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    # profile paths
    # path('profile/<int:user_id>/', views.showUserData, name='profile'),
]