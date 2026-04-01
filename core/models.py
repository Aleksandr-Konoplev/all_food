from django.db import models


class ContentForSite(models.Model):
    """Контент сайта"""

    name_tag = models.CharField(max_length=30)

    title = models.CharField(max_length=100, blank=True, null=True)

    text = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to="media/image_for_site/", blank=True, null=True)

    def __str__(self):
        return f"{self.name_tag}"

    class Meta:
        verbose_name = "Блок контента для сайта"
        verbose_name_plural = "Блоки контента для вставки"


class Feedback(models.Model):
    """Обратная связь"""

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)

    user_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя")

    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")

    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    body = models.TextField()

    def __str__(self):
        return f"{self.owner if self.owner else self.user_name} - {self.body[:70]}"

    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
