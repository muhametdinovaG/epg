# coding: utf8
from django.contrib import admin
from modules.core.forms import *
from .models import *
from .tasks import provider_update


@admin.register(Channel)
class Channels(admin.ModelAdmin):
    form = ChannelForm
    list_display = ['id_channel', 'name', 'provider']
    search_fields = ['id_channel', 'name']


@admin.register(Provider)
class Provider(admin.ModelAdmin):
    form = ProviderForm
    list_display = ['name', 'login', 'password', 'main']
    actions = ['update_program']

    def update_program(self, request, providers):
        for provider in providers:
            provider_update.apply_async(args=(provider.pk,))
    update_program.short_description = 'Обновить программу'


@admin.register(DvbGenre)
class DvbGenre(admin.ModelAdmin):
    form = DvbGenreForm
    list_display = ['code', 'name']


@admin.register(Genre)
class Genre(admin.ModelAdmin):
    form = GenreForm


@admin.register(Category)
class Category(admin.ModelAdmin):
    form = CategoryForm


@admin.register(Program)
class Program(admin.ModelAdmin):
    form = ProgramForm
    list_display = ['broadcast_name', 'channel', 'broadcast_start', 'broadcast_end']
