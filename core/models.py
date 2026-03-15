from django.db import models


class TextContent(models.Model):
    """ Текстовый контент сайта """

    name_content = models.CharField(max_length=20)

    content = models.TextField()

    def __str__(self):
        return f'{self.name_content} - {self.content}'

    class Meta:
        verbose_name = 'Текстовый контент'
        verbose_name_plural = 'Текстовые контенты'
