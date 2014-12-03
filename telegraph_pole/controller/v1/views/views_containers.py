#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.http import Http404

from apphome.models import Container

from serializers import ContainerSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from telegraph_pole.lib.mq import send_message


class ContainerView(APIView):
    """列出所有的容器

    Info:
        GET /containers/ HTTP/1.1
        Content-Type: application/json

    Example request:
        - GET /containers/ HTTP/1.1
        - GET /containers/?cid=390e90e34656806&host=192.168.8.1&... HTTP/1.1

    Query Parameters:

        cid name host size ports image status
        user_id command created hostname flavor_id

    Status Codes:
        200 - no error
        404 - no such container
        500 - server error
    """

    def get(self, request, format=None):

        # 如果有 url 参数
        if request.GET:
            # 从数据库中过滤相应的对象
            containers = Container.objects.all()
            kwargs = request.GET.dict()
            containers = containers.filter(**kwargs)

            # 如果没有过滤出，或者参数传递错误，返回 404
            if not containers:
                raise Http404

        # 没有 url 参数，就返回所有的 container
        else:
            containers = Container.objects.all()

        serializer = ContainerSerializer(containers, many=True)
        return Response(serializer.data)


class ContainerCreateView(APIView):
    """创建一个容器

    Info:
        POST /containers/create HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/create HTTP/1.1

    Json Parameters:
        cid name host size ports image status
        user_id command created hostname flavor_id
    """

    def post(self, request, format=None):
        serializer = ContainerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.data['message_type'] = 'create_container'
            send_message(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerUpdateView(APIView):
    """更新一个容器

    Info:
        PUT /containers/(id)/update HTTP/1.1
        Content-Type: application/json

    Example request:
        PUT /containers/390e90e34656806/update HTTP/1.1

    Jons Parameters:
        cid name host size ports image status
        user_id command created hostname flavor_id
    """

    def get_object(self, id):
        try:
            return Container.objects.get(id=id)
        except Container.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        container = self.get_object(id)
        serializer = ContainerSerializer(container, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerDeleteView(APIView):
    """删除一个容器

    Info:
        DELETE /containers/(id)/delete HTTP/1.1
        Content-Type: application/json

    Example request:
        DELETE /containers/390e90e34656806/delete HTTP/1.1
    """

    def get_object(self, id):
        try:
            return Container.objects.get(id=id)
        except Container.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        container = self.get_object(id)
        container['message_type'] = 'delete_container'
        send_message(container)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContainerDetailView(APIView):
    """根据容器 id 获取数据库中容器信息

    Info:
        GET /containers/(id)/ HTTP/1.1
        Content-Type: application/json

    Example request:
        GET /containers/390e90e34656806 HTTP/1.1
    """

    def get_object(self, id):
        try:
            return Container.objects.get(id=id)
        except Container.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        container = self.get_object(id)
        serializer = ContainerSerializer(container)
        return Response(serializer.data)


class ContainerStopView(APIView):
    """停止一个容器

    Info:
        POST /containers/(id)/stop HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/e90e34656806/stop?t=5 HTTP/1.1

    Query Parameters:
        t – number of seconds to wait before killing the container
    """

    def post(self, request, id, format=None):
        message = {'id': id, 'message_type': 'stop_container'}
        send_message(message)
        return Response(status=status.HTTP_304_NOT_MODIFIED)


class ContainerStartView(APIView):
    """启动一个容器

    Info:
        POST /containers/(id)/start HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/e90e34656806/start HTTP/1.1
    """

    def post(self, request, id, format=None):
        message = {'id': id, 'message_type': 'start_container'}
        send_message(message)
        return Response(status=status.HTTP_304_NOT_MODIFIED)


class ContainerReStartView(APIView):
    """重启一个容器

    Info:
        POST /containers/(id)/restart HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/e90e34656806/restart HTTP/1.1
    """

    def post(self, request, id, format=None):
        message = {'id': id, 'message_type': 'restart_container'}
        send_message(message)
        return Response(status=status.HTTP_304_NOT_MODIFIED)
