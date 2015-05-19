# coding=utf-8
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import re
from ExpertSystem.models import System, Question, TestHistory
from ExpertSystem.utils.log_manager import log

CHANGEABLE_FIELDS = ['last_name', 'first_name', 'email', 'password']


def word_grammar(numeral):
    rem100 = numeral % 100
    if 4 < rem100 < 21:
        result = u'ов'
    else:
        rem10 = rem100 % 10
        if rem10 == 1:
            result = u''
        elif rem10 == 2 or rem10 == 3 or rem10 == 4:
            result = u'а'
        else:
            result = u'ов'
    return result

@login_required
def view_profile(request):
    obj_systems = request.user.system_set.filter(is_deleted=False)
    systems = []
    for obj_system in obj_systems:
        q_count = obj_system.question_set.count()
        o_count = obj_system.sysobject_set.all().count()
        systems.append({
            'id': obj_system.id,
            'name': obj_system.name,
            'is_public': obj_system.is_public,
            'photo': obj_system.photo.url,
            'question_count': q_count,
            'object_count': o_count,
            'question_ending': word_grammar(q_count),
            'object_ending': word_grammar(o_count)
        })

    obj_histories = request.user.testhistory_set.all().order_by('-started')
    histories = []
    for obj_history in obj_histories:
        histories.append({
            'id': obj_history.id,
            'system_id': obj_history.system.id,
            'system_name': obj_history.system.name,
            'started': obj_history.started,
            'finished': obj_history.finished,
            'questions_answered': obj_history.questions,
            'questions_ending': word_grammar(obj_history.questions),
            'total_questions': obj_history.system.question_set.count(),
            'results': json.loads(obj_history.results)
        })

    context = {
        'systems': systems,
        'histories': histories
    }
    return render(request, "profile/view_profile.html", context)

@login_required
@require_http_methods(['POST'])
def update_field(request):
    if request.is_ajax():
        field = request.POST.get('field')
        value = request.POST.get('value')

        if field and field in CHANGEABLE_FIELDS:
            try:
                if field == 'password':
                    value1 = request.POST.get('value1')
                    if not value:
                        return HttpResponse(json.dumps({'status': 'error', 'msg': u'Пароль не может быть пустым'}), content_type='application/json')
                    elif len(value) < 5:
                        return HttpResponse(json.dumps({'status': 'error', 'msg': u'Введите пароль не короче 5 символов'}), content_type='application/json')
                    elif value != value1:
                        return HttpResponse(json.dumps({'status': 'error', 'msg': u'Пароли не совпадают'}), content_type='application/json')
                    else:
                        request.user.set_password(value)
                elif field == 'email' and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    return HttpResponse(json.dumps({'status': 'error', 'msg': u'Введите корректный email'}), content_type='application/json')
                else:
                    setattr(request.user, field, value)
                request.user.save()
                return HttpResponse(json.dumps({'status': 'ok', 'result': getattr(request.user, field, value)}), content_type='application/json')
            except Exception as e:
                log.exception(e)
                return HttpResponse(json.dumps({'status': 'error', 'msg': u'Не получилось обновить данные'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'error', 'msg': u'Это поле нельзя изменить'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'error', 'msg': 'ajax required'}), content_type='application/json')


def delete_history(request, history_id=None):
    if history_id:
        try:
            history = TestHistory.objects.get(id=history_id)
        except TestHistory.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'History doesn\'t exist'}), content_type='application/json')

        if request.user.id == history.user_id:
            history.delete()
            return HttpResponse(json.dumps({'OK': 'Deleted'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'error': 'You can\'t delete this history'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error': 'No history id'}), content_type='application/json')