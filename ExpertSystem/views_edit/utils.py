# coding=utf-8
import json
from django.http import HttpResponse
from ExpertSystem.models import System
from ExpertSystem.utils.log_manager import log


def get_system(session, user_id):
    try:
        system_id = session.get("system_id")
        if not system_id:
            log.warning("No system id in session.")
            return False

        system = System.objects.get(id=system_id, is_deleted=False, user_id=user_id)
    except System.DoesNotExist:
        log.warning("System doesn\'t exist or is deleted or VERBOTTEN")
        return False
    except Exception as e:
        log.exception(e)
        return False

    return system


def error_response():
    response = {
        "code": 1,
        "msg": u"Что-то пошло не так. Попробуйте обновить страницу."
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
