from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blog_previews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
