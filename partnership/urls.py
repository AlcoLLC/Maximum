from django.urls import path
from . import views

app_name = 'partnership'

urlpatterns = [
    path('partnership/', views.service_view, name='partnership'),
]

