# coding: utf-8

import requests
import logging

from django.conf import settings
from .meta import Singleton

LOGGER = logging.getLogger(__name__)


class ErpApi(metaclass=Singleton):
    """
    Взаимодействие с ERP API
    """

    def __init__(self, erp_host, username=None, password=None):
        self.host = erp_host
        self.username = username
        self.password = password
        self.timeout = 10

    def __connect(self, url, payload):
        """
        Для соединения

        :param url: str
        :param payload: dict
        :return: None | dict
        """
        payload['j_username'] = self.username
        payload['j_password'] = self.password
        try:
            r = requests.get(url, params=payload, timeout=self.timeout)
        except (requests.RequestException, requests.Timeout) as e:
            LOGGER.warning('ERP API request failed: {}'.format(e))
            return None

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            LOGGER.warning('ERP API request failed: {}'.format(e))
            return None

        try:
            result = r.json()
        except ValueError as e:
            LOGGER.warning('ERP API request failed: {}'.format(e))
            return None

        if 'status' in result and result['status'] == 'ok':
            return result['data']
        else:
            LOGGER.warning('ERP API request failed: Unexpected response.')
            return None

erp_api = ErpApi(settings.ERP_HOST, settings.ERP_USER, settings.ERP_PASSWORD)
