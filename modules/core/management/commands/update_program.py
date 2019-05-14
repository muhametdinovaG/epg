from django.core.management.base import BaseCommand
from modules.core.models import Provider
from modules.core.tasks import provider_update


class Command(BaseCommand):
    help = 'Update program'

    def handle(self, *args, **options):
        providers = Provider.objects.all()
        for provider in providers:
            provider_update(pk=provider.pk)
