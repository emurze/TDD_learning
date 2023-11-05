import socket

from django.test import LiveServerTestCase


class MyLiveServerTestCase(LiveServerTestCase):
    host = socket.gethostbyname(socket.gethostname())
    live_server_url = f'http://{host}:8080'
