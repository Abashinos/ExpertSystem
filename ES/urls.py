from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ES import settings
from ES.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from ExpertSystem.views_edit import answers, attributes, objects, parameters, questions, rules, system
from ExpertSystem.views_common import index, auth, testing

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ES.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/?$', include(admin.site.urls)),
    url(r'^reset/?$', index.reset, name="reset"),

    url(r'^/?$', index.index, name="index"),
    url(r'^index/?$', index.index, name="index"),
    url(r'^main/?$', index.main_menu, name="main_menu"),

    url(r'^skip/(?P<question_id>[0-9]+)/?$', testing.skip_question, name="skip_question"),
    url(r'^answer/?$', testing.answer, name="answer"),

    url(r'^login/?$', auth.login_view, name="login_view"),
    url(r'^registration/?$', auth.registration, name="registration"),
    url(r'^logout/?$', auth.logout_view, name="logout_view"),

    url(r'^add_system/(?P<system_id>[a-zA-Z0-9._-]+)/?$', system.add_system, name="add_system"),
    url(r'^add_system/?$', system.add_system, name="add_system"),
    url(r'^add_attributes/?$', attributes.add_attributes, name="add_attributes"),
    url(r'^add_parameters/?$', parameters.add_parameters, name="add_parameters"),
    url(r'^add_objects/?$', objects.add_objects, name="add_objects"),
    url(r'^add_answers/?$', answers.add_answers, name="add_answers"),
    url(r'^add_questions/?$', questions.add_questions, name="add_questions"),
    url(r'^add_rules/?$', rules.add_rules, name="add_rules"),

    url(r'^insert_system/?$', system.insert_system, name="insert_system"),
    url(r'^insert_attributes/?$', attributes.insert_attributes, name="insert_attributes"),
    url(r'^insert_parameters/?$', parameters.insert_parameters, name="insert_parameters"),
    url(r'^insert_objects/?$', objects.insert_objects, name="insert_objects"),
    url(r'^insert_answers/?$', answers.insert_answers, name="insert_answers"),
    url(r'^insert_questions/?$', questions.insert_questions, name="insert_questions"),
    url(r'^insert_rules/?$', rules.insert_rules, name="insert_rules"),

    url(r'^delete_attribute_value/?$', attributes.delete_attribute_value, name="delete_attribute_value"),
    url(r'^delete_attribute/?$', attributes.delete_attribute, name="delete_attribute"),
    url(r'^delete_parameter/?$', parameters.delete_parameter, name="delete_parameter"),
    url(r'^delete_answer/?$', answers.delete_answer, name="delete_answer"),
    url(r'^delete_question/?$', questions.delete_question, name="delete_question"),
    url(r'^delete_system/(?P<system_id>[a-zA-Z0-9._-]+)/?$', system.delete_system, name="delete_system")

)

if DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': MEDIA_ROOT}))

    urlpatterns += static(MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
