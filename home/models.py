from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
        
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


class Review(models.Model):    
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    surname = models.CharField(max_length=50, verbose_name="Surname")
    email_address = models.EmailField(verbose_name="Email Address")
    summary = models.CharField(max_length=200, verbose_name="Summary")
    review = models.TextField(verbose_name="Review")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    is_approved = models.BooleanField(default=False, verbose_name="Is Approved")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Approved At")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    
    def save(self, *args, **kwargs):
        if self.is_approved and not self.approved_at:
            self.approved_at = timezone.now()
        elif not self.is_approved:
            self.approved_at = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.rating}★"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.surname}"
    
    @property
    def star_display(self):
        """Star display for HTML usage"""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_approved', '-created_at']),
            models.Index(fields=['rating']),
        ]

class PageHeader(models.Model):
    slug = models.SlugField(
    unique=True,
    help_text="This must exactly match the <strong>name</strong> used in the URL pattern. For example: <code>about</code> "
    ) 
    image = models.ImageField(upload_to='page-headers/')

    def __str__(self):
        return self.slug
