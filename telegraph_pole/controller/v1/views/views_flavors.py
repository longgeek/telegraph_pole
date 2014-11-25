#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django import http
from apphome.models import Flavor

from rest_framework.views import APIView
from rest_framework import response


class FlavorView(APIView):
    """列出所有 Flavor

    Info:
        GET /flavors/ HTTP/1.1
        Content-Type: application/json

    Example request:
        - GET /flavors/ HTTP/1.1

    Status Codes:
        200 - no error
        404 - no such flavor
        500 - server error
    """

    def get(self, request, format=None):
        # 如果有 url 参数
        if request.GET:
            raise http.Http404
        # 没有 url 参数，就返回所有的 Flavor
        else:
            return response.Response(Flavor)


class FlavorDetailView(APIView):
    """根据 id 获取 Flavor

    Info:
        GET /flavors/(id)/ HTTP/1.1
        Content-Type: application/json

    Example request:
        GET /flavors/2/ HTTP/1.1

    Status Codes:
        200 - no error
        404 - no such flavor
        500 - server error
    """

    def get_object(self, id):
        try:
            return Flavor[str(id)]
        except KeyError:
            raise http.Http404

    def get(self, request, id, format=None):
        flavor = self.get_object(id)
        return response.Response(flavor)
