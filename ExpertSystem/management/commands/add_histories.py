import json
from random import randrange
import string
from django.utils import timezone
import uuid
import datetime
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from ExpertSystem.models import System, TestHistory

import warnings
warnings.filterwarnings("ignore")

class Command(BaseCommand):

    def handle(self, *args, **options):
        arguments = {}
        for arg in args:
            try:
                key, value = string.split(arg, '=')
            except ValueError:
                continue
            arguments[key] = value

        number = int(arguments.get('n', 100))

        users = User.objects.all()
        systems = System.objects.all()

        for i in range(number):
            user = users[randrange(len(users))]
            system = systems[randrange(len(systems))]

            history = TestHistory.objects.create(
                user=user,
                system=system,
                hash=uuid.uuid4().hex,
                results=json.dumps([{"name": "test", "weight": 50.0}]),
                started=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                finished=timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            print(history.id)


