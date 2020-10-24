from .base import *

import sys

ALLOWED_HOSTS = []
DEBUG = True

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE
INSTALLED_APPS += ["debug_toolbar"]

INTERNAL_IPS = [
    "127.0.0.1",
]
