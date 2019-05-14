# coding: utf8
from django.contrib import admin
from modules.process.forms import *
from .models import *


@admin.register(Event)
class Events(admin.ModelAdmin):
    form = EventForm
    list_display = ['title']


@admin.register(Filial)
class Filials(admin.ModelAdmin):
    form = FilialForm
    list_display = ['erp_id', 'title']


@admin.register(ProcessQueue)
class ProcessQueues(admin.ModelAdmin):
    form = ProcessQueueForm
    list_display = ['filial', 'description', 'start_of_work', 'end_of_work', 'event_type', 'send']
    search_fields = ['filial', 'start_of_work']


@admin.register(Keywords)
class Keyword(admin.ModelAdmin):
    form = KeywordsForm
    list_display = ['genre', 'word']
    search_fields = ['genre', 'word']
