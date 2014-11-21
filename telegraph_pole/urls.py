#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

from django.contrib import admin

from controller.v1 import urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('rest_framework_swagger.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^v1/', include(urls)),
)
