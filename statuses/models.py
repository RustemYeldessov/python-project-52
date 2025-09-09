from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name

