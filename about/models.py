from django.db import models

# Create your models here.

class About(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class AboutContent(models.Model):
    about = models.ForeignKey(About, related_name='contents', on_delete=models.CASCADE)
    section_title = models.CharField(max_length=200)
    section_content = models.TextField()
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)

    def __str__(self):
        return self.section_title
    
class AboutSection(models.Model):
    about = models.ForeignKey(About, related_name='sections', on_delete=models.CASCADE)
    section_title = models.CharField(max_length=200)
    section_description = models.TextField()
    image = models.ImageField(upload_to='about_section_images/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.section_title
    
class GlobalPresence(models.Model):
    title = models.CharField(max_length=200)
    description_one = models.TextField()
    description_two = models.TextField()
    description_three = models.TextField()

    def __str__(self):
        return self.title
    
class Sustainability(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='sustainability_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class PartnershipContent(models.Model):
    title = models.CharField(max_length=200)
    title_content = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='partnership_images/', blank=True, null=True)

    def __str__(self):
        return self.title