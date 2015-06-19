from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework import routers
from views import views_hosts as views

# from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
admin.autodiscover()


router = routers.DefaultRouter()

urlpatterns = patterns(
    '',

    url(r'^$',
        views.HostView.as_view()),

    url(r'^create$',
        views.HostCreateView.as_view()),

    url(r'^(?P<pk>[0-9]+)$',
        views.HostDetailView.as_view()),

    # url(r'^(?P<pk>[0-9]+)/update$',
    #     views.HostUpdateView.as_view()),

    # url(r'^(?P<pk>[0-9]+)/delete$',
    #     views.HostDeleteView.as_view()),
)

# urlpatterns = format_suffix_patterns(urlpatterns)
