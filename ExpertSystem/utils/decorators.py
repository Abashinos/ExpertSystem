from django.http import HttpResponseRedirect

from ExpertSystem.utils.sessions import SESSION_KEY
from ExpertSystem.utils.sessions import SESSION_ES_CREATE_KEY


def require_session():
    def decorator(func):
        def wrapped(request, *args, **kwargs):
            if request.session.get(SESSION_KEY):
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/index")
        return wrapped
    return decorator


def require_creation_session():
    def decorator(func):
        def wrapped(request, *args, **kwargs):
            if request.session.get(SESSION_ES_CREATE_KEY):
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/index")
        return wrapped
    return decorator


def require_post_params(*params):
    def decorator(func):
        def wrapped(request, *args, **kwargs):
            for param in params:
                if not request.POST.get(param):
                    return HttpResponseRedirect("/index")
            return func(request, *args, **kwargs)
        return wrapped
    return decorator