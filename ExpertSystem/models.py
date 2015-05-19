# coding=utf-8
import hashlib
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from imagekit.models.fields import ImageSpecField
from pilkit.processors import ResizeToFill
import os
from django.utils.translation import ugettext_lazy as _

def default_photo():
    return os.path.join("images", "no_img.png")


class System(models.Model):
    def photo_upload(self, *args):
        return os.path.join("system", hashlib.md5(str(self.id)).hexdigest() + ".jpg")

    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=1000, blank=True, null=True, default='')
    date_created = models.DateField(blank=True, null=True, default=timezone.now())
    is_deleted = models.BooleanField(_(u'Удалена'), blank=True, default=False)
    is_public = models.BooleanField(_(u'Опубликована'), blank=True, default=True)
    is_open_for_guests = models.BooleanField(_(u'Открыта для гостей'), blank=True, default=True)
    photo = models.ImageField(upload_to=photo_upload, default=default_photo(), null=True, blank=True)
    pic_thumbnail = ImageSpecField([ResizeToFill(200, 200)], source='photo',
                                   format='JPEG', options={'quality': 90})

    class Meta:
        db_table = "system"
        verbose_name = u"Система"
        verbose_name_plural = u"Системы"

    def __unicode__(self):
        return self.name + " by " + self.user.username


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    class Meta:
        db_table = "attribute"
        verbose_name = u"Атрибут"
        verbose_name_plural = u"Атрибуты"

    def __unicode__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    class Meta:
        db_table = "parameter"
        verbose_name = u"Параметр"
        verbose_name_plural = u"Параметры"

    def __unicode__(self):
        return self.name


class Question(models.Model):
    SELECT = 0
    NUMBER = 1
    CHOICES = (
        (SELECT, "Выберите ответ"),
        (NUMBER, "Напишите число"),
    )
    # Параметр, к которому привязан вопрос
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    body = models.TextField()
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    type = models.IntegerField(choices=CHOICES)

    class Meta:
        db_table = "question"
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"

    def __unicode__(self):
        return "Question #" + str(self.id) + " in system: " + self.system.name


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    body = models.TextField()
    parameter_value = models.TextField()

    class Meta:
        db_table = "answer"
        verbose_name = u"Ответ"
        verbose_name_plural = u"Ответы"

    def __unicode__(self):
        return "Answer #" + str(self.id) + " to question #" + str(self.question.id)


class AttributeValue(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    attr = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    class Meta:
        db_table = "attribute_value"
        verbose_name = u"Значение атрибута"
        verbose_name_plural = u"Значения атрибутов"

    def __unicode__(self):
        return str(self.id) + ". " + self.attr.name + " : " + self.value


class SysObject(models.Model):
    name = models.TextField()
    #Список атрибутов и их значений у объекта
    attributes = models.ManyToManyField(AttributeValue, null=True, blank=True, related_name='sys_objects')
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    class Meta:
        db_table = "sys_object"
        verbose_name = u"Объект"
        verbose_name_plural = u"Объекты"

    def __unicode__(self):
        return self.name


class Rule(models.Model):
    PARAM_RULE = 0
    ATTR_RULE = 1
    CHOICES = (
        (PARAM_RULE, "Правило для параметра"),
        (ATTR_RULE, "Правило для атрибута"),
    )
    condition = models.TextField()
    result = models.TextField()
    type = models.IntegerField(choices=CHOICES)
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    class Meta:
        db_table = "rule"
        verbose_name = u"Правило"
        verbose_name_plural = u"Правила"


class TestHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    hash = models.CharField(max_length=100, null=True, blank=True)

    results = models.TextField(default="")
    started = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)
    questions = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = "test_history"
        verbose_name = u"История"
        verbose_name_plural = u"Истории"

    def __unicode__(self):
        return u"History for user " + self.user.username + u" for system " + self.system.name