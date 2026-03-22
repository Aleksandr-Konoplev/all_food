from django.db import models


class ContentForSite(models.Model):
    """ Контент сайта """

    name_content = models.CharField(max_length=30)

    text = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='media/image_for_site/', blank=True, null=True)

    def __str__(self):
        return f'{self.name_content}'

    class Meta:
        verbose_name = 'Контент для сайта'
        verbose_name_plural = 'Контенты для сайта'
