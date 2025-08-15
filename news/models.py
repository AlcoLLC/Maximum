from django.db import models
from django.utils.text import slugify



class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/')
    published_date = models.DateTimeField()
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False, verbose_name="Top of news page")
    in_home = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

class News_Content(models.Model):
    news = models.ForeignKey(
        News, related_name='contents', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)


    def __str__(self):
        return f"{self.news.title} Content"
