import logging
import websocket
import json

LOGGER = logging.getLogger(__name__)

__all__ = ['WS']


class WS(object):
    """
    Класс для общение с api.ufanet.ru
    """

    def __init__(self, app_key, host):
        self.app_key = app_key
        self.host = host
        self.ws = None

    def __enter__(self):
        try:
            self.ws = websocket.create_connection(self.host, timeout=5)
        except Exception as e:
            LOGGER.error('WS error: {0}'.format(e))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ws:
            self.ws.close()
        if exc_val:
            LOGGER.error('WS error: {0}'.format(exc_val))
        return True

    def fetch_data(self, data, method):
        result_data = {
            'app_key': self.app_key,
            'method': method,
            'data': data
        }
        return json.dumps(result_data)

    def request(self, data, method):
        if not self.ws:
            return None
        data = self.fetch_data(data, method)
        self.ws.send(data)
        response1 = self.ws.recv()
        response = self.ws.recv()

        try:
            response_data = json.loads(response)
        except:
            response_data = None
        return response_data
