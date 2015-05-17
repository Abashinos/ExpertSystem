# coding=utf-8
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System, Question
from ExpertSystem.utils.log_manager import log

CHANGEABLE_FIELDS = ['last_name', 'first_name', 'email',]


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
    obj_systems = System.objects.filter(user=request.user, is_deleted=False)
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

    context = {
        'systems': systems
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