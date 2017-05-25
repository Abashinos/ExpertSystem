# coding=utf-8
import hashlib
from django.shortcuts import render, redirect
from ExpertSystem.models import System, Parameter, Question, Answer, TestHistory
from ExpertSystem.queries import update_session_attributes
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_session, require_post_params
from ExpertSystem.utils.parser import get_parameters
from ExpertSystem.utils.parser import get_attributes

@require_session()
def next_question(request, final=False):
    session_dict = request.session.get(sessions.SESSION_KEY)
    system_id = session_dict["system_id"]
    selected_params = session_dict["selected_params"]
    asked_questions = session_dict["asked_questions"]

    system = System.objects.get(id=system_id)
    all_parameters = Parameter.objects.filter(system=system)

    if not final:
        # Берем все параметры
        for param in all_parameters:

            param_values = selected_params.get(str(param.id), None)

            # Находим, какие еще не выясняли
            if not param_values:

                questions = Question.objects.filter(parameter=param)

                # Проходим все вопросы у каждого параметра, смотрим какие еще не задавали и спрашиваем
                for question in questions:
                    if question.id not in asked_questions:
                        table = []
                        for elem in session_dict["objects"]:
                            if elem['weight'] > 0.01:
                                table.append(elem)

                        table = sorted(
                            table,
                            key=lambda k: float(k['weight']),
                            reverse=True
                        )

                        answers = Answer.objects.filter(question=question)
                        ctx = {
                            "question": question,
                            "answers": answers,
                            "table": table
                        }
                        return render(request, "question.html", ctx)

    sum_weights = sum(map(lambda obj: float(obj['weight']), session_dict['objects']))
    objects = [{'name': obj['name'], 'weight': round(100.0 * float(obj['weight']) / sum_weights, 2)}
               for obj in session_dict['objects']
               if obj['weight'] >= 0.01]

    session_dict['objects'] = sorted(
        objects,
        key=lambda k: float(k['weight']),
        reverse=True
    )

    try:
        history = session_dict['history']
        TestHistory.objects.get(hash=hashlib.md5(str(history['user_id'])+history['started']).hexdigest())
    except TestHistory.DoesNotExist:
        sessions.update_session_history(request, write_results=True, results=session_dict['objects'], finished=True)

    return render(request, "final.html", {"system_id": system.id, "table": session_dict["objects"]})


@require_session()
def final(request):
    return next_question(request, final=True)


@require_session()
@require_post_params("answer", "question_id")
def answer(request):
    answer_id = request.POST.get("answer")
    question_id = request.POST.get("question_id")

    session_dict = request.session.get(sessions.SESSION_KEY, None)
    selected_params = session_dict['selected_params']

    question = Question.objects.get(id=question_id)
    param_id = question.parameter.id
    param_values = selected_params.get(param_id, [])

    sessions.update_session_history(request, inc_questions=True)

    if question.type == 0:
        answer = Answer.objects.get(id=answer_id)
        if not answer.parameter_value or answer.parameter_value == "":
            return skip_question(request, question_id)
        param_values.append(answer.parameter_value)
    else:
        # Здесь answer_id - текст ответа
        param_values.append(answer_id)

    selected_params[param_id] = param_values

    applied_rules = session_dict['applied_rules']

    get_parameters(selected_params, session_dict["system_id"], applied_rules)

    attrs = get_attributes(selected_params, session_dict["system_id"], applied_rules)

    sessions.add_to_session(request, asked_questions=[int(question_id), ], selected_params=selected_params, applied_rules=applied_rules)

    request.session[sessions.SESSION_KEY] = update_session_attributes(
        request.session.get(sessions.SESSION_KEY), attrs
    )

    return redirect("/index")


@require_session()
def skip_question(request, question_id):
    try:
        sessions.add_to_session(request, asked_questions=[int(question_id)])
    except ValueError:
        pass
    return redirect("/index")