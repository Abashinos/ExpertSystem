# coding=utf-8
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System, Question, Parameter, Answer
from ExpertSystem.views_edit.utils import get_system, error_response
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session, require_post_params
from ExpertSystem.utils.log_manager import log


@login_required(login_url="/login/")
@require_creation_session()
def add_answers(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = get_system(session, request.user.id)
    if not system:
        return redirect("/reset/")
    questions = Question.objects.filter(system=system, type=Question.SELECT)
    return render(request, "add_system/add_answers.html", {
        "system": system,
        "questions": questions
    })


@login_required(login_url="/login/")
@require_http_methods(["POST"])
@require_post_params("form_data")
@require_creation_session()
@transaction.atomic
def insert_answers(request):
    """
    Добавление/редактирование ответов
    :param request:
    {
        "form_data": [
            {
                "id": id вопроса
                "answers": [
                    {
                        "id": id ответа, либо -1
                        "body": значение,
                        "parameter_value": значение параметра, устанавлимое этим ответом
                    }
                ]
            }
        ]
    }
    :return:
    """
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = get_system(session, request.user.id)
    if not system:
        return error_response()

    try:
        form_data = json.loads(request.POST.get("form_data"))
    except TypeError as e:
        log.exception(e)
        return error_response()

    for question_element in form_data:
        try:
            question = Question.objects.get(id=question_element['id'], system=system)
        except Question.DoesNotExist:
            log.error("Question #" + str(question_element["id"]) + " doesn\'t exist.")
            continue

        if len(question_element['answers']) > 0:
            for answer in question_element['answers']:
                a_id = answer['id']

                if not answer.get('body'):
                    response = {
                        "code": 1,
                        "msg": u"Заполните названия всех ответов, пожалуйста."
                    }

                    return HttpResponse(json.dumps(response), content_type="application/json")

                if a_id and int(a_id) != -1:
                    # Обновление вопроса
                    try:
                        answer_element = Answer.objects.get(id=a_id)
                    except Answer.DoesNotExist as e:
                        log.error("Answer #" + str(a_id) + " doesn\'t exist.")
                        continue
                    answer_element.body = answer['body']
                    answer_element.parameter_value = answer['parameter_value']
                    answer_element.save()
                else:
                    # Создание вопроса
                    answer_element = Answer(question=question, body=answer['body'], parameter_value=answer['parameter_value'])
                    answer_element.save()
                pass
        else:
            # удалить все ответы для этого вопроса
            Answer.objects.filter(question=question).delete()
    response = {
        "code": 0,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required(login_url="/login/")
@require_http_methods(["POST"])
@require_post_params("id")
@require_creation_session()
@transaction.atomic
def delete_answer(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    if not get_system(session, request.user.id):
        return error_response()

    a_id = request.POST.get("id")

    try:
        q_id = int(request.POST.get("id"))
        if q_id and q_id > 0:
            Answer.objects.get(id=q_id).delete()
    except Question.DoesNotExist:
        pass
    except ValueError as e:
        log.exception(e)
        return error_response()

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")