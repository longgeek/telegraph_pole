#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.conf.urls import patterns
from django.conf.urls import url

from views import views_flavors as views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.FlavorView.as_view()),
    url(r'^(?P<id>[0-9]+)$',
        views.FlavorDetailView.as_view()),
)
