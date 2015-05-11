# coding=utf-8
from django.shortcuts import render, redirect
from ExpertSystem.models import System
from ExpertSystem.utils import sessions
from ExpertSystem.utils.sessions import clear_session
from ExpertSystem.views_common.testing import next_question


def index(request):
    admin = True if request.user.is_staff is True else False
    sessions.clear_es_create_session(request)
    if sessions.SESSION_KEY not in request.session:
        system_id = request.GET.get("system_id", None)

        if not system_id:
            if not request.user.is_authenticated():
                systems = System.objects.filter(is_deleted=False, is_public=True, is_open_for_guests=True)
                return render(request, "systems.html", {"systems": systems})

            if admin:
                systems = System.objects.all().order_by('is_deleted', '-id')
            else:
                systems = System.objects.filter(is_deleted=False, is_public=True) | System.objects.filter(is_deleted=False, user=request.user)
            return render(request, "systems.html", {"systems": systems, "user_id": request.user.id, "admin": admin})
        else:
            sessions.init_session(request, system_id)

    return next_question(request)


def reset(request):
    """
    Очищает сессию, стартует тестирование заново
    """
    system_id = request.GET.get('system_id')
    clear_session(request)
    redirect_url = "/index/"
    if system_id:
        redirect_url += '?system_id=' + system_id
    return redirect(redirect_url)


def main_menu(request):
    sessions.clear_session(request)
    return redirect('/index/')