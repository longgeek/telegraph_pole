#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

import simplejson

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
        400 - bad request
        404 - no such container
        500 - server error
    """

    def get(self, request, format=None):

        # 如果有 url 参数
        if request.GET:
            # 从数据库中过滤相应的对象
            containers = Container.objects.filter(create_status=True)
            kwargs = request.GET.dict()
            containers = containers.filter(**kwargs)

            # 如果没有过滤出，或者参数传递错误，返回 404
            if not containers:
                raise Http404

        # 没有 url 参数，就返回所有的 container
        else:
            containers = Container.objects.filter(create_status=True)

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

    Status Codes:
        200 - no error
        400 - bad request
        404 - no such container
        500 - server error
    """

    def post(self, request, format=None):
        serializer = ContainerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.data['message_type'] = 'create_container'
            msg_result = simplejson.loads(send_message(serializer.data))
            if msg_result[0] == 0:
                return Response(msg_result[2], status=status.HTTP_200_OK)
            else:
                return Response(msg_result[1],
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ContainerUpdateView(APIView):
    """更新一个容器

    Info:
        PUT /containers/(id)/update HTTP/1.1
        Content-Type: application/json

    Example request:
        PUT /containers/3/update HTTP/1.1

    Jons Parameters:
        cid name host size ports image status
        user_id command created hostname flavor_id

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
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
        DELETE /containers/3/delete HTTP/1.1

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
    """

    def delete(self, request, id, format=None):
        msg = {'id': id, 'message_type': 'delete_container'}
        msg_result = simplejson.loads(send_message(msg))
        if msg_result[0] == 0:
            return Response(msg_result[2], status=status.HTTP_200_OK)
        else:
            return Response(msg_result[1], status=status.HTTP_400_BAD_REQUEST)


class ContainerDetailView(APIView):
    """根据容器 id 获取数据库中容器信息

    Info:
        GET /containers/(id)/ HTTP/1.1
        Content-Type: application/json

    Example request:
        GET /containers/3 HTTP/1.1

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
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
        POST /containers/3/stop?t=5 HTTP/1.1

    Query Parameters:
        t – number of seconds to wait before killing the container

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'stop_container'}
        msg_result = simplejson.loads(send_message(msg))
        if msg_result[0] == 0:
            return Response(msg_result[2], status=status.HTTP_200_OK)
        else:
            return Response(msg_result[1], status=status.HTTP_400_BAD_REQUEST)


class ContainerStartView(APIView):
    """启动一个容器

    Info:
        POST /containers/(id)/start HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/start HTTP/1.1

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'start_container'}
        msg_result = simplejson.loads(send_message(msg))
        if msg_result[0] == 0:
            return Response(msg_result[2], status=status.HTTP_200_OK)
        else:
            return Response(msg_result[1], status=status.HTTP_400_BAD_REQUEST)


class ContainerReStartView(APIView):
    """重启一个容器

    Info:
        POST /containers/(id)/restart HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/restart HTTP/1.1

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'restart_container'}
        msg_result = simplejson.loads(send_message(msg))
        if msg_result[0] == 0:
            return Response(msg_result[2], status=status.HTTP_200_OK)
        else:
            return Response(msg_result[1], status=status.HTTP_400_BAD_REQUEST)


class ContainerExecView(APIView):
    """在容器中启动一个进程

    Info:
        POST /containers/exec HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/exec HTTP/1.1

        {
         "id": "2",
         "command":[
                     "date"
             ],
        }

    Jons Parameters:
        id: str
        command: list

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
    """

    def post(self, request, format=None):
        param = request.POST

        # 判断 post 的参数是否有 'id' ‘command'
        # 并且 value 不能为空
        if len(param) == 2 and 'id' in param.keys() and \
                               'command' in param.keys():
            if param['id'] and param['command']:
                msg = {'id': param['id'], 'command': param['command'],
                       'message_type': 'exec_container'}
                msg_result = simplejson.loads(send_message(msg))
                if msg_result[0] == 0:
                    return Response(msg_result[2], status=status.HTTP_200_OK)
                else:
                    return Response(msg_result[1],
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Error: The wrong parameter!',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Error: The wrong parameter!',
                            status=status.HTTP_400_BAD_REQUEST)


class ContainerPauseView(APIView):
    """暂停一个容器

    Info:
        POST /containers/(id)/pause HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/pause HTTP/1.1

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'pause_container'}
        msg_result = simplejson.loads(send_message(msg))
        if msg_result[0] == 0:
            return Response(msg_result[2], status=status.HTTP_200_OK)
        else:
            return Response(msg_result[1], status=status.HTTP_400_BAD_REQUEST)


class ContainerUnPauseView(APIView):
    """恢复一个容器

    Info:
        POST /containers/(id)/unpause HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/unpause HTTP/1.1

    Status Codes:
        200 - no error
        400 - bad request
        500 - server error
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'unpause_container'}
        msg_result = simplejson.loads(send_message(msg))
        if msg_result[0] == 0:
            return Response(msg_result[2], status=status.HTTP_200_OK)
        else:
            return Response(msg_result[1], status=status.HTTP_400_BAD_REQUEST)
