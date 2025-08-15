from django.urls import path
from .views import contact_view, contact_step_two_view, handle_contact_step_two_submission, validate_email_ajax

app_name = "contact"

urlpatterns = [
    path("contact/", contact_view, name="contact"),
    path('contact-step-2/', contact_step_two_view, name='contact_step_two'),
    path('contact-step-2/submit/', handle_contact_step_two_submission, name='contact_step_two_submit'),
    path('validate-email/', validate_email_ajax, name='validate_email'),
]