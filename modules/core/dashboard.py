# coding^ utf-8
from admin_tools.dashboard import modules, Dashboard
from admin_tools.menu import items, Menu
from admin_tools.utils import get_admin_site_name
from django.urls import reverse


class CustomDashboard(Dashboard):
    """
    Рабочий стол для админки
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.LinkList(
            'Быстрые ссылки',
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [],
            ]
        ))

        self.children.append(modules.Group(
            title='Главное меню',
            display='tabs',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                modules.AppList(
                    title='Основные данные',
                    models=('modules.core.*',),
                ),
                modules.AppList(
                    title='Процессы',
                    models=('modules.process.*',),
                ),
            ]
        ))

        self.children.append(modules.RecentActions(
            title='Последние действия в системе',
            draggable=False,
            deletable=False,
            collapsible=False,
            limit=5
        ))


class CustomMenu(Menu):
    """
    Кастомное меню
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem('Dashboard', reverse('admin:index')),
            items.Bookmarks(),
            items.AppList(
                'Applications',
                exclude=('django.contrib.*', 'modules.core.models.User')
            ),
            items.ModelList(
                title='CELERY',
                models=(
                    'django_celery_results.models.*',
                    'django_celery_beat.models.*',
                )
            ),
            items.AppList(
                'Applications',
                exclude=('django.contrib.*', 'modules.core.models.User')
            ),
        ]
