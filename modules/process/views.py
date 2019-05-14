# coding: utf-8

from django.conf import settings
from django.views import generic as cbv
from modules.process.utils import WS
from django.http import JsonResponse


class OrderConnectView(cbv.View):
    """
    Создание процессов
    """

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        event_type = request.POST.get('event_type')
        filial = request.POST.get('filial')
        description = request.POST.get('description')
        start_of_work = request.POST.get('start_of_work')
        end_of_work = request.POST.get('end_of_work')

        data = {
            'id': id,
            'event_type': event_type,
            'filial': filial,
            'description': description,
            'start_of_work': start_of_work,
            'end_of_work': end_of_work,
        }

        result = None
        with WS(app_key=settings.API_APP_KEY, host=settings.API_HOST) as api:
            result = api.request(data, 'create_request')
        if not result:
            return JsonResponse(data={'status': 'error'}, status=400)

        if result['status'] == 200:
            return JsonResponse(data={'status': 'ok'})
        else:
            return JsonResponse(data={'status': 'error'}, status=result['status'])
