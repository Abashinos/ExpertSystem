# coding=utf-8
import datetime
import hashlib
import json
from time import strptime, strftime
from django.utils import timezone
from ExpertSystem.models import System, SysObject, TestHistory

SESSION_KEY = "ExpertSystem"
SESSION_ES_CREATE_KEY = "ExpertSystem_create"


def init_history(user_id, system_id):
    history = {
        'started': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'finished': None,
        'questions': 0,
        'results': None,
        'system_id': int(system_id),
        'user_id': user_id
    }
    history['hash'] = hashlib.md5(str(history['user_id'])+history['started']).hexdigest()
    return history


def init_session(request, system_id):
    system = System.objects.filter(id=system_id)
    sys_objects = SysObject.objects.filter(system=system)
    objects = []
    for object in sys_objects:
        objects.append({
            "name": object.name,
            "weight": 0,
        })
    session = {
        "system_id": system_id,
        "selected_params": {},
        "asked_questions": [],
        "applied_rules": [],
        "objects": objects,
        "history": init_history(request.user.id, system_id)
    }

    request.session[SESSION_KEY] = session


def add_to_session(request, asked_questions=None, selected_params=None, applied_rules=None):
    session = request.session.get(SESSION_KEY)

    if asked_questions:
        session["asked_questions"] += asked_questions

    if selected_params:
        session["selected_params"] = selected_params

    if applied_rules:
        session["applied_rules"] = applied_rules

    request.session[SESSION_KEY] = session


def clear_session(request):
    if SESSION_KEY in request.session:
        del request.session[SESSION_KEY]


def update_session_history(request, inc_questions=False, finished=False, write_results=False, results=""):
    if not request.user.is_authenticated():
        return
    if inc_questions:
        request.session[SESSION_KEY]['history']['questions'] += 1
    if write_results:
        request.session[SESSION_KEY]['history']['results'] = results
    if finished:
        request.session[SESSION_KEY]['history']['finished'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_history = request.session[SESSION_KEY]['history']
        if results and session_history['questions'] > 0:
            TestHistory.objects.create(
                user_id=session_history['user_id'],
                system_id=session_history['system_id'],
                questions=session_history['questions'],
                results=json.dumps(session_history['results']),
                started=session_history['started'],
                finished=session_history['finished'],
                hash=session_history['hash']
            )


def init_es_create_session(request, system_id):
    # Как только мы начали редактирование системы, или создали новую, мы записываем ее в сессию,
    # это значит, что мы в режиме редактирования и нужно не добавлять сущности, а изменять
    session = {
        "system_id": system_id,
    }

    request.session[SESSION_ES_CREATE_KEY] = session


def clear_es_create_session(request):
    if SESSION_ES_CREATE_KEY in request.session:
        del request.session[SESSION_ES_CREATE_KEY]