#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django import http

from apphome.models import Host

from serializers import HostSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import response


class HostView(APIView):
    """列出所有的主机

    Info:
        GET /hosts/ HTTP/1.1
        Content-Type: application/json

    Example request:
        - GET /hosts/ HTTP/1.1
        - GET /hosts/?ip=192.168.8.1&port=2375& ...... HTTP/1.1

    Query Parameters:
        ip port image status total_cpu total_mem
        total_sys_disk total_volume total_bandwidth

    Status Codes:
        200 - no error
        404 - no such container
        500 - server error
    """

    def get(self, request, format=None):
        # 如果有 url 参数
        if request.GET:
            # 从数据库中过滤相应的对象
            hosts = Host.objects.all()
            kwargs = request.GET.dict()
            hosts = hosts.filter(**kwargs)

            # 如果没有过滤出，或者参数传递错误，返回 404
            if not hosts:
                raise http.Http404

        # 没有 url 参数，就返回所有的 host
        else:
            hosts = Host.objects.all()

        serializer = HostSerializer(hosts, many=True)
        return response.Response(serializer.data)


class HostCreateView(APIView):
    """创建一个主机

    Info:
        POST /hosts/create HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /hosts/create HTTP/1.1

    Json Parameters:
        ip port image status total_cpu total_mem
        total_sys_disk total_volume total_bandwidth
    """

    def post(self, request, format=None):
        serializer = HostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)


class HostUpdateView(APIView):
    """更新一个主机

    Info:
        PUT /hosts/(pk)/update HTTP/1.1
        Content-Type: application/json

    Example request:
        PUT /hosts/2/update HTTP/1.1

    Json Parameters:
        ip port image status total_cpu total_mem
        total_sys_disk total_volume total_bandwidth
    """

    def get_object(self, pk):
        try:
            return Host.objects.get(pk=pk)
        except Host.DoesNotExist:
            raise http.Http404

    def put(self, request, pk, format=None):
        host = self.get_object(pk)
        serializer = HostSerializer(host, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)


class HostDeleteView(APIView):
    """删除一个主机

    Info:
        DELETE /hosts/(pk)/delete HTTP/1.1
        Content-Type: application/json

    Example request:
        DELETE /host/2/delete HTTP/1.1
    """

    def get_object(self, pk):
        try:
            return Host.objects.get(pk=pk)
        except Host.DoesNotExist:
            raise http.Http404

    def delete(self, request, pk, format=None):
        host = self.get_object(pk)
        host.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class HostDetailView(APIView):
    """根据 pk 获取主机信息

    Info:
        GET /hosts/(id)/ HTTP/1.1
        Content-Type: application/json

    Example request:
        GET /hosts/2/ HTTP/1.1
    """

    def get_object(self, pk):
        try:
            return Host.objects.get(pk=pk)
        except Host.DoesNotExist:
            raise http.Http404

    def get(self, request, pk, format=None):
        host = self.get_object(pk)
        serializer = HostSerializer(host)
        return response.Response(serializer.data)
