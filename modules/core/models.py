# coding: utf-8
import gzip
import os
import wget
import shutil
import urllib
import xml.etree.ElementTree as ET
from urllib import request

from pytils import translit
from django.db import models
from django.conf import settings
from django.db import transaction
from django.utils import timezone

__all__ = ['Provider', 'Channel', 'Genre', 'Category', 'Program', 'DvbGenre']


class Provider(models.Model):
    """
    Поставщик
    """
    name = models.CharField('Поставщик', max_length=100, help_text='Максимальное кол-во символов: 100')
    main = models.BooleanField('Главный?', default=False)
    link = models.CharField('Ссылка', max_length=150, help_text='Максимальное кол-во символов: 150', blank=True, null=True)
    full_url_logo = models.BooleanField(default=False)
    login = models.CharField('Логин', max_length=100, null=True, blank=True, help_text='Максимальное кол-во символов: 100')
    password = models.CharField('Пароль', max_length=100, null=True, blank=True, help_text='Максимальное кол-во символов: 100')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name

    def update_program(self):

        if not self.link:
            return

        self.program.all().delete()

        url = self.link
        login = self.login
        password = self.password
        id_provider = self.id

        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, self.name)):
            os.mkdir(os.path.join(settings.MEDIA_ROOT, self.name))
            os.mkdir(os.path.join(settings.MEDIA_ROOT, self.name, 'icon'))

        if login is None:
            # Скачиваение архива
            filename = wget.download(url)
            dst_path = os.path.join(settings.MEDIA_ROOT, self.name, filename)
            os.rename(filename, dst_path)

            # Распаковка .gz
            output = "".join(dst_path.split('.')[0:-1])
            with gzip.open(dst_path, "rb") as f_in, open(output, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        else:
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, url, login, password)
            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            opener = urllib.request.build_opener(handler)
            opener.open(url)
            urllib.request.install_opener(opener)
            filename = wget.download(url)
            dst_path = os.path.join(settings.MEDIA_ROOT, self.name, filename)
            os.rename(filename, dst_path)
            output = dst_path
        tree = ET.parse(output)
        root = tree.getroot()

        """
        Получение каналов
        """
        for channel in root.findall('channel'):
            try:
                id_channel = channel.attrib['id']
                channel_name = channel.find('display-name').text
                icon = channel.find('icon').get('src')
                logo_url = icon if self.full_url_logo else "{0}{1}".format('http://', icon)
                filename_icon = wget.download(logo_url)
                dst_path = os.path.join(settings.MEDIA_ROOT, self.name, 'icon', filename_icon)

                os.rename(filename_icon, dst_path)
            except:
                continue

            with transaction.atomic():
                user_obj, _ = Channel.objects.get_or_create(id_channel=id_channel,
                                                            name=channel_name,
                                                            icon=dst_path,
                                                            provider_id=id_provider)

        for programme in root.findall('programme'):
            try:
                dvb = programme.find('dvbgenre').text
            except:
                dvb = None

            dvbgenres = DvbGenre.objects.all().filter(code=dvb)
            for dvbgenre in dvbgenres:
                dvbgenre_id = dvbgenre.id

            try:
                category_name = programme.find('category').text
            except:
                category_name = None

            with transaction.atomic():
                user_obj, _ = Category.objects.get_or_create(name=category_name)

            categoryes = Category.objects.all().filter(name=category_name)
            for category in categoryes:
                category_id = category.id

            try:
                genre = programme.find('genre').text
            except:
                genre = None

            with transaction.atomic():
                user_obj, _ = Genre.objects.get_or_create(name=genre)

            genres = Genre.objects.all().filter(name=genre)
            for genre in genres:
                genre_id = genre.id

            try:
                date = programme.find('date').text
            except:
                date = None

            try:
                broadcast_name = programme.find('title').text
            except:
                broadcast_name = None

            try:
                chnl_id = programme.attrib['channel']
            except:
                chnl_id = None

            chnls = Channel.objects.all().filter(id_channel=chnl_id)
            for chnl in chnls:
                ch_id = chnl.id

            try:
                description = programme.find('desc').text
            except:
                description = None

            try:
                broadcast_starts = programme.attrib['start'].split()
                broadcast_start = timezone.datetime.strptime(broadcast_starts[0], '%Y%m%d%H%M%S')
            except:
                broadcast_starts = programme.attrib['start']
                broadcast_start = timezone.datetime.strptime(broadcast_starts, '%Y%m%d%H%M%S')

            try:
                broadcast_ends = programme.attrib['stop'].split()
                broadcast_end = timezone.datetime.strptime(broadcast_ends[0], '%Y%m%d%H%M%S')
            except:
                broadcast_ends = programme.attrib['stop']
                broadcast_end = timezone.datetime.strptime(broadcast_ends, '%Y%m%d%H%M%S')

            with transaction.atomic():
                user_obj, _ = Program.objects.get_or_create(date=date,
                                                            broadcast_name=broadcast_name,
                                                            channel_id=ch_id,
                                                            category_id=category_id,
                                                            description=description,
                                                            broadcast_start=broadcast_start,
                                                            broadcast_end=broadcast_end,
                                                            genre_id=genre_id,
                                                            dvb_name_id=dvbgenre_id,
                                                            provider_id=id_provider)


class DvbGenre(models.Model):
    """
    Dvb жанр
    """
    code = models.CharField('Dvb код', max_length=5, help_text='Максимальное кол-во символов: 4')
    name = models.CharField('Название жанра', max_length=100, help_text='Максимальное кол-во символов: 100')

    class Meta:
        verbose_name = 'Dvb жанр'
        verbose_name_plural = 'Dvb жанры'

    def __str__(self):
        return str(self.name)


class Channel(models.Model):
    """
    Канал
    """

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["channel_icon/", translit.slugify(name), ".", extension])
        return path

    id_channel = models.PositiveIntegerField('ID канала')
    name = models.CharField('Название канала', max_length=250, help_text='Максимальное кол-во символов: 250')
    icon = models.ImageField('Логотип', upload_to=get_image_path, null=True, blank=True)
    provider = models.ForeignKey(Provider, verbose_name='Поставщик', related_name='channel', blank=True, null=True, on_delete=models.SET_NULL)
    main_channel = models.BooleanField('Главный?', default=False)
    display = models.BooleanField('Отображать?', default=False)

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанры
    """
    name = models.CharField('Название жанра', max_length=250, help_text='Максимальное кол-во символов: 250', null=True, blank=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    """
    Категория
    """
    name = models.CharField('Название категории', max_length=250, help_text='Максимальное кол-во символов: 250', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)


class Program(models.Model):
    """
    Программа
    """
    provider = models.ForeignKey(Provider, verbose_name='Поставщик', related_name='program', on_delete=models.CASCADE)
    broadcast_name = models.CharField('Название передачи', max_length=250, help_text='Максимальное кол-во символов: 250')
    date = models.DateField('Дата', null=True, blank=True)
    channel = models.ForeignKey(Channel, related_name='program', blank=True, null=True, on_delete=models.SET_NULL)
    broadcast_start = models.DateTimeField('Начало передачи')
    broadcast_end = models.DateTimeField('Конец передачи')
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', related_name='program', blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='program', blank=True, null=True, on_delete=models.SET_NULL)
    dvb_name = models.ForeignKey(DvbGenre, verbose_name='dvb жанр', related_name='program', blank=True, null=True, on_delete=models.SET_NULL)
    # country = models.CharField('Страна', max_length=100, help_text='Максимальное кол-во символов: 100', null=True)

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        return str(self.broadcast_name)
