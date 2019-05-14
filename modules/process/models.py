# coding: utf-8
from django.db import models

__all__ = ['Event', 'Filial', 'ProcessQueue', 'Keywords']


class Event(models.Model):
    """
    Тип события в очереди
    """
    title = models.CharField('Тип события', max_length=20)

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'

    def __str__(self):
        return str(self.title)


class Filial(models.Model):
    """
    Филиалы в erp
    """
    erp_id = models.IntegerField('Идентификатор в erp')
    title = models.CharField('Название филиала', max_length=100)

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return str(self.title)


class ProcessQueue(models.Model):
    """
    Очередь процессов
    """
    event_type = models.ForeignKey(Event, related_name='processqueue', verbose_name='Тип события', blank=True, null=True, on_delete=models.SET_NULL)
    filial = models.ForeignKey(Filial, related_name='process_queue', verbose_name='Филиал', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField('Описание события', max_length=300, help_text='Максимальное кол-во символов: 300')
    start_of_work = models.DateTimeField('Начало работ')
    end_of_work = models.DateTimeField('Завершение работ')
    send = models.BooleanField('Отправить?', default=False)

    class Meta:
        verbose_name = 'Очередь процессов'
        verbose_name_plural = 'Очередь процессов'


class Keywords(models.Model):
    """
    Ключевые слова
    """
    genre = models.CharField('Жанр/Категория', max_length=250, help_text='Максимальное кол-во символов: 250')
    word = models.CharField('Слово', max_length=100, help_text='Максимальное кол-во символов: 150')

    class Meta:
        verbose_name = 'Ключевые слова'
        verbose_name_plural = 'Ключевые слова'
