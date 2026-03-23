from django.db import models


class ContentForSite(models.Model):
    """ Контент сайта """

    name_tag = models.CharField(max_length=30)

    title = models.CharField(max_length=100, blank=True, null=True)

    text = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='media/image_for_site/', blank=True, null=True)

    def __str__(self):
        return f'{self.name_tag}'

    class Meta:
        verbose_name = 'Блок контента для сайта'
        verbose_name_plural = 'Блоки контента для вставки'
