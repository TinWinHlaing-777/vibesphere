from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # profile paths
    # path('profile/<int:user_id>/', views.showUserData, name='profile'),

    # Article paths
    path('article/new', views.create_update_article, name='create'),
    path('article/<str:article_id>/edit/', views.create_update_article, name='edit_article'),
    path('pages/', views.show_all_pages, name='pages'),
    path('page/new', views.blog_page_create, name="create_page"),
    path('page/manage/<int:user_id>/', views.manage_page, name="manage_page"),
    path('page/update/<str:title>/', views.update_page, name="update_page"),
]