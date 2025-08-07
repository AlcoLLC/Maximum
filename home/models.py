from django.db import models
        
class HomeSwiper(models.Model):    
    image = models.ImageField(
        upload_to='home_swiper/',
        help_text="Image to be displayed in the home page swiper"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of the image in the swiper"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this image is active and should be displayed"
    )
    title = models.CharField(
        max_length=255,
        help_text="Title for the swiper image"
    )

    link = models.URLField(
        help_text="Link to navigate when the swiper button is clicked"
    )

    def __str__(self):
        return f"Swiper Image {self.order} - {'Active' if self.is_active else 'Inactive'}"

    class Meta:
        ordering = ['order']
        verbose_name = "Home Swiper Image"
        verbose_name_plural = "Home Swiper Images"

class PartnerLogo(models.Model):
    name = models.CharField(
        max_length=255, 
        null=True, blank=True,
        help_text="Partner name"
    )
    logo = models.ImageField(upload_to='partner_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CarLogo(models.Model):
    name = models.CharField(
        max_length=255, null=True, blank=True
    )
    logo = models.ImageField(upload_to='car_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
