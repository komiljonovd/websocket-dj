from django.db import models

# Create your models here.
class News(models.Model):
    title = models.TextField()
    short_description = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'News'   
        verbose_name = 'News'
        verbose_name_plural = 'News'