from django.urls import path
from .views import home_view, submit_review

app_name = "home"

urlpatterns = [
    path("", home_view, name="home"),
    path("submit-review/", submit_review, name="submit_review"),

]