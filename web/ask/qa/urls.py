from django.conf.urls import url

from . import views

app_name = 'qa'
urlpatterns = [
    url(r'^question/(?P<pk>[0-9]+)/$', views.question, name='question'),
    url(r'^$', views.new_questions, name='new_questions'),
    url(r'^popular/$', views.popular_questions, name='popular_questions'),
    url(r'^ask/$', views.question_add, name='question_add')

]
