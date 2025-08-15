from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('brands/', views.brand_view, name='brands'),
    path('brands/<str:tab>/', views.brand_view, name='brands_tab'),

]

