"""
WSGI config for TakeOutTogetherWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import sys
path = '/home/hupeng/py-web/StudentSign'
if path not in sys.path:
    sys.path.insert(0, '/home/hupeng/py-web/StudentSign')



from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudentSign.settings")

application = get_wsgi_application()
