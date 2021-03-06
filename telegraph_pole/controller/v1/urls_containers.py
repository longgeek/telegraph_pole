#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.conf.urls import patterns
from django.conf.urls import url

from views import views_containers as views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.ContainerView.as_view()),

    url(r'^create$',
        views.ContainerCreateView.as_view()),

    url(r'^(?P<id>[0-9]+)/$',
        views.ContainerDetailView.as_view()),

    url(r'^(?P<id>[0-9]+)/update$',
        views.ContainerUpdateView.as_view()),

    url(r'^(?P<id>[0-9]+)/delete$',
        views.ContainerDeleteView.as_view()),

    url(r'^(?P<id>[0-9]+)/inspect$',
        views.ContainerInspectView.as_view()),

    url(r'^(?P<id>[0-9]+)/stop$',
        views.ContainerStopView.as_view()),

    url(r'^(?P<id>[0-9]+)/start$',
        views.ContainerStartView.as_view()),

    url(r'^(?P<id>[0-9]+)/restart$',
        views.ContainerReStartView.as_view()),

    url(r'^(?P<id>[0-9]+)/exec$',
        views.ContainerExecView.as_view()),

    url(r'^(?P<id>[0-9]+)/pause$',
        views.ContainerPauseView.as_view()),

    url(r'^(?P<id>[0-9]+)/unpause$',
        views.ContainerUnPauseView.as_view()),

    url(r'^(?P<id>[0-9]+)/top$',
        views.ContainerTopView.as_view()),

    url(r'^(?P<id>[0-9]+)/console$',
        views.ContainerConsoleView.as_view()),

    url(r'^(?P<id>[0-9]+)/files/write$',
        views.ContainerFilesWriteView.as_view()),

    url(r'^(?P<id>[0-9]+)/files/list$',
        views.ContainerFilesListView.as_view()),

    url(r'^(?P<id>[0-9]+)/files/read$',
        views.ContainerFilesReadView.as_view()),

    url(r'^(?P<id>[0-9]+)/files/delete$',
        views.ContainerFilesDeleteView.as_view()),

    url(r'^(?P<id>[0-9]+)/console/url$',
        views.ContainerConsoleUrlView.as_view()),

    url(r'^(?P<id>[0-9]+)/dirs/create$',
        views.ContainerDirsCreateView.as_view()),

    url(r'^(?P<id>[0-9]+)/dirs/delete',
        views.ContainerDirsDeleteView.as_view()),

    url(r'^(?P<id>[0-9]+)/host/exec$',
        views.ContainerHostExecView.as_view()),

    url(r'^(?P<id>[0-9]+)/host/fdcheck$',
        views.ContainerHostFDCheckView.as_view()),
)
