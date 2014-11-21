#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.conf.urls import patterns
from django.conf.urls import url

from views import views_flavors as views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.HostView.as_view()),
)
