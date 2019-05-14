from configs import celery_app
from modules.core.models import Provider


@celery_app.task(name='core.update_program')
def provider_update(pk):
    """Перенос контента в ceph"""
    try:
        Provider.objects.get(pk=pk).update_program()
    except Provider.DoesNotExist:
        pass
