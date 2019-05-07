from django.http import HttpRequest
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseNotFound
from functools import wraps
from .models import *

def allow_request(req: list):
    def __decorator(func):
        @wraps(func)
        def __wrapper(request: HttpRequest, *args, **kwargs):
            if request.method not in req:
                return HttpResponseNotAllowed(req)
            else:
                return func(request, *args, **kwargs)
        return __wrapper
    return __decorator

def check_authenticated(func):
    @wraps(func)
    def __wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            return func(request, *args, **kwargs)
    return __wrapper