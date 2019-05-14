# coding: utf-8
from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'modules.process'
    verbose_name = 'Процессы'

    def ready(self):
        super(CoreAppConfig, self).ready()
