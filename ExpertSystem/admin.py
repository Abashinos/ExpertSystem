from django.contrib import admin
from django.db.models import get_models, get_model
from models import *


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'system')
    ordering = ('-system', 'name')


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'system')
    ordering = ('-system', 'name')


class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_deleted', 'is_public', 'is_open_for_guests')
    ordering = ('is_deleted', 'user', 'name')


class SysObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'system')
    ordering = ('-system', 'name')


class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'system')
    ordering = ('-system', '-id')

admin.site.register(System, SystemAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AttributeValue)
admin.site.register(SysObject, SysObjectAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(TestHistory)


