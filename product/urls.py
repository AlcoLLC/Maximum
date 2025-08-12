from django.urls import path, re_path
from . import views

app_name = 'product'

urlpatterns = [
    path('products/', views.product_list, name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('ajax/product-properties/<int:product_id>/', views.product_properties_ajax, name='product_properties_ajax'),
]
