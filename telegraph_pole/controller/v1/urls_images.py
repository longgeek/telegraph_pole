#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.conf.urls import patterns
from django.conf.urls import url

from views import views_images as views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.ImageView.as_view()),

    url(r'^create$',
        views.ImageCreateView.as_view()),

    url(r'^(?P<pk>[0-9]+)$',
        views.ImageDetailView.as_view()),

    # url(r'^(?P<pk>[0-9]+)/update$',
    #     views.ImageUpdateView.as_view()),

    # url(r'^(?P<pk>[0-9]+)/delete$',
    #     views.ImageDeleteView.as_view()),
)
