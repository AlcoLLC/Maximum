from django.urls import path
from .views import contact_view, contact_step_two_view, validate_email_ajax

app_name = "contact"

urlpatterns = [
    path("contact/", contact_view, name="contact"),
    path('contact-step-2/', contact_step_two_view, name='contact_step_two'),
    path('validate-email/', validate_email_ajax, name='validate_email'),
]