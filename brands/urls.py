from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('brands/', views.brand_view, name='brands'),
]

