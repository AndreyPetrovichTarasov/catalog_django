from django.urls import path
from catalog.apps import CatalogConfig
from . import views


app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
]
