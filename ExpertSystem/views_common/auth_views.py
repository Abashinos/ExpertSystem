# coding=utf-8
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                return HttpResponse(json.dumps({"status": "ERROR", "error": u"Неправильные данные"}), content_type="application/json")
            else:
                login(request, user)
                return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "ERROR", "error": u"Мало данных"}), content_type="application/json")
    else:
        return render(request, "auth/login.html")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        if username and email and password:
            try:
                user = User.objects.get(username=username)
                if user:
                    return HttpResponse(json.dumps({"status": "ERROR", "error": u"Никнейм занят"}), content_type="application/json")
            except User.DoesNotExist:
                user = User.objects.create(email=email, username=username, last_name=last_name, first_name=first_name)
                user.set_password(request.POST["password"])
                user.save()

                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"status": "ERROR", "error": u"Ошибочка вышла"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "ERROR", "error": u"Мало данных"}, content_type="application/json"))
    else:
        return render(request, "auth/registration.html")


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("/")
