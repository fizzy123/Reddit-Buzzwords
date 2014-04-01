from django.conf.urls import patterns, url

from buzzwords import views

urlpatterns = patterns('buzzwords.views',
        url(r'^$', 'index', name='index'),
)
