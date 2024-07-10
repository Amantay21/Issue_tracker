from django.db import models


class Type(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название типа", unique=True)

    def __str__(self):
        return f'{self.title}'


class Status(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название статуса", unique=True)

    def __str__(self):
        return f'{self.title}'


class Issue(models.Model):
    summary = models.TextField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', on_delete=models.RESTRICT, verbose_name='Статус')
    types = models.ManyToManyField('webapp.Type', related_name='issues', verbose_name='Тип')
    created_date = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name='Время обновления', auto_now=True)

    def __str__(self):
        return f'{self.summary}'
