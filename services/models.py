from django.core.exceptions import ValidationError
from django.db import models

class Services(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    in_home = models.BooleanField(default=False)
    in_service_page = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def clean(self):
        if not self.pk and Services.objects.count() >= 3:
            raise ValidationError("Only up to 3 services can be added.")

    def __str__(self):
        return f"{self.title}"


class Service_Content(models.Model):
    subtitle = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='service_content/')

    def __str__(self):
        return f"{self.title}"

