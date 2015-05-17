# coding=utf-8
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.utils.log_manager import log

CHANGEABLE_FIELDS = ['last_name', 'first_name', 'email',]


@login_required
def view_profile(request):
    return render(request, "profile/view_profile.html")

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