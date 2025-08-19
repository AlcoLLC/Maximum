from django.db import models

class BrandGuidelineDocument(models.Model):
    title = models.CharField(max_length=255)
    short_content = models.TextField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='brand_guidelines/documents/')
    preview_image = models.ImageField(upload_to='brand_guidelines/previews/')
    
    def __str__(self):
        return self.title


class PromoMaterialsLibrary(models.Model):
    short_content = models.TextField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.short_content[:50]
    

class PromoMaterial(models.Model):
    library = models.ForeignKey(
        PromoMaterialsLibrary,
        related_name='promo_materials',
        on_delete=models.CASCADE
    )
    
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='promo_materials/')
    preview_image = models.ImageField(upload_to='promo_materials/previews/')
    
    def __str__(self):
        return self.title

    
class BrandImageLibrary(models.Model):
    short_content = models.TextField(max_length=255)
    description = models.TextField() 
    
    def __str__(self):
        return self.short_content[:50]


class BrandImage(models.Model):
    library = models.ForeignKey(
        BrandImageLibrary,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='brand_images/previews/')
    
    def __str__(self):
        return f"Image for {self.library.short_content[:30]}"


class BrandVideoLibrary(models.Model):
    short_content = models.TextField(max_length=255)
    description = models.TextField() 
    
    def __str__(self):
        return self.short_content[:50]


class BrandVideo(models.Model):
    videos = models.ForeignKey(
        BrandVideoLibrary,
        related_name='videos',
        on_delete=models.CASCADE
    )
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='brand_videos/thumbnails/')
    
    def __str__(self):
        return f"Image for {self.videos.short_content[:30]}"
