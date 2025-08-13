from django.db import models

class Partnership_Content(models.Model):
    subtitle = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='partnership_content/')

    def __str__(self):
        return f"{self.title}"

