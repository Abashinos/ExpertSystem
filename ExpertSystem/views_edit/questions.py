# coding=utf-8
import json
from django import forms
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import Select
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System
from ExpertSystem.models import Parameter
from ExpertSystem.models import Question
from ExpertSystem.models import SysObject
from ExpertSystem.models import AttributeValue
from ExpertSystem.views_edit.utils import get_system, error_response
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session
from ExpertSystem.utils.decorators import require_post_params
from ExpertSystem.utils.log_manager import log


@login_required(login_url="/login/")
@require_creation_session()
def add_questions(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = get_system(session, request.user.id)
    if not system:
        return redirect("/reset/")
    all_parameters = Parameter.objects.filter(system=system)

    parameters = []

    for param in all_parameters:
        param_dict = {
            "id": param.id,
            "name": param.name,
            "questions": [],
        }
        param_questions = Question.objects.filter(parameter=param)
        for question in param_questions:
            param_dict["questions"].append(question)

        parameters.append(param_dict)

    return render(request, "add_system/questions_page/add_questions.html", {
        "parameters": parameters,
        "system": system
    })


@login_required(login_url="/login/")
@require_http_methods(["POST"])
@require_post_params("id")
@require_creation_session()
@transaction.atomic
def delete_question(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    if not get_system(session, request.user.id):
        return error_response()

    try:
        q_id = int(request.POST.get("id"))
        if q_id and q_id > 0:
            Question.objects.get(id=q_id).delete()
    except Question.DoesNotExist:
        pass
    except ValueError as e:
        log.exception(e)
        return error_response()

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required(login_url="/login/")
@require_http_methods(["POST"])
@require_post_params("form_data")
@require_creation_session()
@transaction.atomic
def insert_questions(request):
    """
    Добавляет объекты
    :param request: {
        "form_data": [
            {
                "id": id параметра,
                "questions": [
                    {
                        "id": id вопроса, либо -1, если вопрос новый
                        "type": тип вопроса (0 или 1),
                        "body": текст вопроса
                    }, ...
                ]
            }, ...
        ]
    }
    :return:
    """
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = get_system(session, request.user.id)
    if not system:
        return error_response()

    try:
        formdata = json.loads(request.POST.get('form_data'))
    except TypeError as e:
        log.exception(e)
        return error_response()

    for parameterJSON in formdata:
        try:
            parameter = Parameter.objects.get(id=parameterJSON["id"])
        except Parameter.DoesNotExist:
            log.error("Parameter #" + str(parameterJSON["id"]) + " doesn\'t exist.")
            continue

        for questionJSON in parameterJSON["questions"]:
            question_id = questionJSON["id"]
            if not questionJSON.get("body"):
                response = {
                    "code": 1,
                    "msg": u"Заполните все вопросы, пожалуйста."
                }

                return HttpResponse(json.dumps(response), content_type="application/json")
            if question_id and question_id != "-1":
                try:
                    question = Question.objects.get(id=question_id)
                except Question.DoesNotExist:
                    log.error("Question #" + str(question_id) + " doesn\'t exist.")
                    continue
            else:
                question = Question(system=system, parameter=parameter)
            question.type = questionJSON["type"]
            question.body = questionJSON["body"]
            question.save()

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")