# coding=utf-8
import json
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System
from ExpertSystem.views_edit.utils import error_response
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_post_params
from ExpertSystem.utils.log_manager import log
from scripts.recreate import recreate


@login_required(login_url="/login/")
def create_db(request):
    recreate()
    return HttpResponse(content="OK")


@login_required(login_url="/login/")
def add_system(request, **kwargs):

    if "system_id" in kwargs:
        # Если выбрали редактирование конкретной системы
        system_id = kwargs["system_id"]
        try:
            system = System.objects.get(id=system_id, user_id=request.user.id, is_deleted=False)
            sessions.init_es_create_session(request, system.id)
            return render(request, "add_system/add_system.html", {"system": system})
        except System.DoesNotExist:
            return redirect("/", {'error': u'Вы не можете редактировать эту систему'})
        except Exception as e:
            log.exception(e)
            return redirect("/", {'error': u'Что-то пошло не так...'})
    else:
        sessions.clear_session(request)
        sessions.clear_es_create_session(request)
        return render(request, "add_system/add_system.html")


@login_required(login_url="/login/")
@require_http_methods(["POST"])
def insert_system(request):

    response = {
        "code": 0,
    }

    system_name = request.POST.get("system_name")
    system_about = request.POST.get("system_about")
    system_public = True if request.POST.get("system_public") else False
    system_open = True if request.POST.get("system_open") else False
    system_pic = request.FILES.get('system_pic')

    if not system_name:
        response = {
            'code': 1,
            'msg': u'Введите название системы'
        }
        return HttpResponse(json.dumps(response), content_type="application/json")

    if system_pic:
        try:
            trial_image = Image.open(system_pic)
            trial_image.verify()
        except IOError:
            response = {
                'code': 1,
                'msg': u'Загрузите корректную картинку.'
            }
            return HttpResponse(json.dumps(response), content_type="application/json")
        except Exception as e:
            log.exception(e)
            response = {
                'code': 1,
                'msg': u'Загрузите корректную картинку.'
            }
            return HttpResponse(json.dumps(response), content_type="application/json")

    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    if session:
        try:
            system = System.objects.get(id=session["system_id"], is_deleted=False)
        except System.DoesNotExist:
            log.error("System " + session["system_id"] + " doesn\'t exist.")
            response = {
                'code': 1,
                'msg': u'Системы не существует. Попробуйте заново создать систему.'
            }
            return HttpResponse(json.dumps(response), content_type="application/json")

        system.name = system_name
        system.about = system_about
        system.is_open_for_guests = system_open
        system.is_public = system_public
        if system_pic:
            system.photo = system_pic
        try:
            system.save()
        except Exception as e:
            log.exception(e)
            return error_response()

        response['system_id'] = system.id
        return HttpResponse(json.dumps(response), content_type="application/json")

    params = {
        "name": system_name,
        "user": request.user,
        "about": system_about,
        "is_open_for_guests": system_open,
        "is_public": system_public
    }
    if system_pic:
        params.update({"photo": system_pic})
    try:
        system = System.objects.create(**params)
        response['system_id'] = system.id
    except Exception as e:
        log.exception(e)
        return error_response()

    sessions.init_es_create_session(request, system.id)
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_http_methods(["GET"])
@login_required(login_url="/login/")
def delete_system(request, system_id=None):
    if system_id:
        try:
            system = System.objects.get(id=system_id, is_deleted=False)
            user_id = User.objects.get(id=system.user_id).id
        except System.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'System doesn\'t exist'}), content_type='application/json')
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'User doesn\'t exist'}), content_type='application/json')

        if request.user.id == user_id:
            if not request.user.is_superuser:
                system.is_deleted = True
                system.save()
            else:
                system.delete()
            return HttpResponse(json.dumps({'OK': 'Deleted'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'error': 'You can\'t delete this system'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error': 'No system id'}), content_type='application/json')
