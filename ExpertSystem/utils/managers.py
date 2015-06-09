# coding=utf-8
from __future__ import division
from django.db.models import get_model
from ExpertSystem.utils.ordereddict import OrderedDict


ACTIVITY_MODELS = {
    'ExpertSystem': ['system', 'testhistory'],
    'auth': ['user'],
}

SYSTEM_MODELS = {
    'ExpertSystem': ['sysobject', 'attribute', 'parameter', 'question', 'answer', 'rule'],
}

def get_statistics():

    statistics = []

    activity_data = []
    for app in ACTIVITY_MODELS:
        for model in ACTIVITY_MODELS[app]:
            model = get_model(app, model)
            if model:
                activity_data.append({
                    'point': model._meta.verbose_name_plural.title(),
                    'number': model.objects.count()
                })

    total_system_data = []
    for app in SYSTEM_MODELS:
        for model in SYSTEM_MODELS[app]:
            model = get_model(app, model)
            if model:
                total_system_data.append({
                    'point': model._meta.verbose_name_plural.title(),
                    'number': model.objects.count()
                })

    system_data = []
    systems_count = get_model('ExpertSystem', 'system').objects.count()
    for data in total_system_data:
        system_data.append({
            'point': data['point'],
            'number': round(data['number'] / systems_count, 2)
        })

    statistics.extend((
        {
            'name': u'Активность пользователей',
            'type': 'bar',
            'data': activity_data
        },
        {
            'name': u'Количество данных в экспертных системах',
            'type': 'bar',
            'data': total_system_data
        },
        {
            'name': u'Соотношение данных на одну экспертную систему',
            'type': 'pie',
            'data': system_data
        }
    ))

    return statistics
