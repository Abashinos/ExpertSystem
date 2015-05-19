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

    name = models.CharField(max_length=50, verbose_name=u'Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    about = models.TextField(max_length=1000, blank=True, null=True, default='', verbose_name=u'О системе')
    date_created = models.DateField(blank=True, null=True, default=timezone.now(), verbose_name=u'Дата создания')
    is_deleted = models.BooleanField(blank=True, default=False, verbose_name=u'Удалена')
    is_public = models.BooleanField(blank=True, default=True, verbose_name=u'Публична')
    is_open_for_guests = models.BooleanField(blank=True, default=True, verbose_name=u'Открыта для гостей')
    photo = models.ImageField(upload_to=photo_upload, default=default_photo(), null=True, blank=True, verbose_name=u'Картинка')
    pic_thumbnail = ImageSpecField([ResizeToFill(200, 200)], source='photo',
                                   format='JPEG', options={'quality': 90})

    class Meta:
        db_table = "system"
        verbose_name = u"Система"
        verbose_name_plural = u"Системы"

    def __unicode__(self):
        return self.name + u". Автор: " + self.user.username


class Attribute(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название')
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u'Система')

    class Meta:
        db_table = "attribute"
        verbose_name = u"Атрибут"
        verbose_name_plural = u"Атрибуты"

    def __unicode__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название')
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u'Система')

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
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name=u'Параметр')
    body = models.TextField(verbose_name=u'Текст')
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u'Система')
    type = models.IntegerField(choices=CHOICES, verbose_name=u'Тип')

    class Meta:
        db_table = "question"
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"

    def __unicode__(self):
        return u"Вопрос №" + unicode(self.id) + u" в системе " + self.system.name


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name=u'Вопрос')
    body = models.TextField(verbose_name=u'Текст')
    parameter_value = models.TextField(verbose_name=u'Значение параметра')

    class Meta:
        db_table = "answer"
        verbose_name = u"Ответ"
        verbose_name_plural = u"Ответы"

    def __unicode__(self):
        return u"Ответ №" + unicode(self.id) + u" на вопрос №" + unicode(self.question.id)


class AttributeValue(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u'Система')
    attr = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name=u'Атрибут')
    value = models.CharField(max_length=50, verbose_name=u'Значение')

    class Meta:
        db_table = "attribute_value"
        verbose_name = u"Значение атрибута"
        verbose_name_plural = u"Значения атрибутов"

    def __unicode__(self):
        return str(self.id) + ". " + self.attr.name + " : " + self.value


class SysObject(models.Model):
    name = models.TextField(verbose_name=u'Название')
    attributes = models.ManyToManyField(AttributeValue, null=True, blank=True, related_name='sys_objects', verbose_name=u'Атрибуты')
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u'Система')

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
    condition = models.TextField(verbose_name=u'Условие')
    result = models.TextField(verbose_name=u'Следствие')
    type = models.IntegerField(choices=CHOICES, verbose_name=u'Тип')
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u'Система')

    class Meta:
        db_table = "rule"
        verbose_name = u"Правило"
        verbose_name_plural = u"Правила"


class TestHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u'Система')
    hash = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Уникальный хэш')

    results = models.TextField(default="", verbose_name=u'Результаты')
    started = models.DateTimeField(null=True, blank=True, verbose_name=u'Начало прохождения')
    finished = models.DateTimeField(null=True, blank=True, verbose_name=u'Конец прохождения')
    questions = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=u'Количество отвеченных вопросов')

    class Meta:
        db_table = "test_history"
        verbose_name = u"История"
        verbose_name_plural = u"Истории"

    def __unicode__(self):
        return u"История прохождения пользователем " + self.user.username + u" тестирования в системе " + self.system.name