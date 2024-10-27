from django.urls import path
from blog_post.apps import BlogPostConfig
from .views import ArticleDeleteView, ArticleUpdateView, ArticleCreateView, ArticleDetailView, ArticleListView


app_name = BlogPostConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('blog/articles/new/', ArticleCreateView.as_view(), name='article_create'),
    path('blog/article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('blog/update_article/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('blog/delete_article/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
]
