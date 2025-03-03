from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Article paths
    path('articles/by-page/<str:page_name>/', views.articles_by_page, name="articles_by_page"),
    path('article/new', views.create_update_article, name='create'),
    path('article/<str:article_title>/edit/', views.create_update_article, name='edit_article'),
    path('articles/<str:id>/', views.read_article, name="read_article"),
    path('articles/', views.show_all_articles, name="show_all_articles"),
    path('like/<str:article_title>/', views.like_article, name='like_article'),
    path('increment-share-count/<str:article_title>/', views.increment_share_count, name='increment_share_count'),

    
    # Page paths
    path('pages/', views.show_all_pages, name='pages'),
    path('page/new', views.create_update_blog_page, name="create_page"),
    path('page/manage/<int:user_id>/', views.manage_page, name="manage_page"),
    path('page/update/<str:title>/', views.create_update_blog_page, name="update_page"),
]