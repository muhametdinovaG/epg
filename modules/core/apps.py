# coding: utf-8
from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'modules.core'
    verbose_name = 'Основное'

    def ready(self):
        super(CoreAppConfig, self).ready()
        from . import signal_receivers
