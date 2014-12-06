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
        200 - Success, no error
        400 - Failure, bad request
        404 - Failure, no such container
        500 - Failure, server error

    Results: JSON
        Success:
            [
                {
                    "id": 14,
                    "cid": "390e90e34656806578a5a86bd12d5f1abc
                            59b58b8be2b65bcf48a410e5536b9b",
                    "size": "0",
                    "host": 1,
                    "name": "/determined_lalande",
                    "image": 1,
                    "ports": "",
                    "status": "Up 36 minutes",
                    "user_id": "2",
                    "command": "/bin/bash",
                    "created": "1417874473",
                    "hostname": "bda51967884c",
                    "flavor_id": "1"
                }
            ]
        Failure:
            {"detail": STRING}
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
        201 - Success, no error, created
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {
                "id": 14,
                "cid": "bda51967884c70b578a5a86bd12d5f1abc59b5
                        8b8be2b65bcf48a410e5536b9b",
                "size": "0",
                "host": 1,
                "name": "/determined_lalande",
                "image": 1,
                "ports": "",
                "status": "Up 41 minutes",
                "user_id": "2",
                "command": "/bin/bash",
                "created": "1417874473",
                "hostname": "bda51967884c",
                "flavor_id": "1"
            }

        Failure:
            {"detail": STRING}
    """

    def post(self, request, format=None):
        serializer = ContainerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.data['message_type'] = 'create_container'
            s, m, r = send_message(serializer.data)
            if s == 0:
                return Response(r, status=status.HTTP_201_CREATED)
            else:
                detail = {'detail': m}
                return Response(detail,
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
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error
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
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {"detail": STRING}
        Failure:
            {"detail": STRING}
    """

    def delete(self, request, id, format=None):
        msg = {'id': id, 'message_type': 'delete_container'}
        s, m, r = send_message(msg)
        if s == 0:
            detail = {'detail': 'Container %s has been deleted.' % r['cid']}
            return Response(detail, status=status.HTTP_200_OK)
        else:
            detail = {'detail': m}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)


class ContainerDetailView(APIView):
    """根据容器 id 获取数据库中容器信息

    Info:
        GET /containers/(id) HTTP/1.1
        Content-Type: application/json

    Example request:
        GET /containers/3 HTTP/1.1

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {
                "id": 14,
                "cid": "bda51967884c70b578a5a86bd12d5f1abc59b
                        58b8be2b65bcf48a410e5536b9b",
                "size": "0",
                "host": 1,
                "name": "/determined_lalande",
                "image": 1,
                "ports": "",
                "status": "Up 6 minutes",
                "user_id": "2",
                "command": "/bin/bash",
                "created": "1417874473",
                "hostname": "bda51967884c",
                "flavor_id": "1"
            }
        Failure:
            {"detail": STRING}
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
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {"detail": STRING}
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'stop_container'}
        s, m, r = send_message(msg)
        if s == 0:
            detail = {'detail': 'Container %s stop success.' % r['cid']}
            return Response(detail, status=status.HTTP_200_OK)
        else:
            detail = {'detail': m}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)


class ContainerStartView(APIView):
    """启动一个容器

    Info:
        POST /containers/(id)/start HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/start HTTP/1.1

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {"detail": STRING}
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'start_container'}
        s, m, r = send_message(msg)
        if s == 0:
            detail = {'detail': 'Container %s startup success.' % r['cid']}
            return Response(detail, status=status.HTTP_200_OK)
        else:
            detail = {'detail': m}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)


class ContainerReStartView(APIView):
    """重启一个容器

    Info:
        POST /containers/(id)/restart HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/restart HTTP/1.1

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {"detail": STRING}
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'restart_container'}
        s, m, r = send_message(msg)
        if s == 0:
            detail = {'detail': 'Container %s restart success.' % r['cid']}
            return Response(detail, status=status.HTTP_200_OK)
        else:
            detail = {'detail': m}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)


class ContainerExecView(APIView):
    """在容器中启动一个进程

    Info:
        POST /containers/(id)/exec HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/exec HTTP/1.1

        {
         "command":[
                     "date",
                     "date -s"
             ],
        }

    Jons Parameters:
        id: str
        command: list

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {"detail": STRING}
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        param = request.POST

        # 判断 post 的参数是否有 'id' ‘command'
        # 并且 value 不能为空
        if len(param) == 1 and 'command' in param.keys():
            if param['command']:
                msg = {'id': id, 'command': param['command'],
                       'message_type': 'exec_container'}
                s, m, r = send_message(msg)
                if s == 0:
                    detail = {'detail': 'Container %s command \
                                         executed successfully' % r['cid']}
                    return Response(detail, status=status.HTTP_200_OK)
                else:
                    detail = {'detail': m}
                    return Response(detail,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                detail = {'detail': 'Error: The wrong parameter!'}
                return Response(detail,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            detail = {'detail': 'Error: The wrong parameter!'}
            return Response(detail,
                            status=status.HTTP_400_BAD_REQUEST)


class ContainerPauseView(APIView):
    """暂停一个容器

    Info:
        POST /containers/(id)/pause HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/pause HTTP/1.1

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {"detail": STRING}
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'pause_container'}
        s, m, r = send_message(msg)
        if s == 0:
            detail = {'detail': 'Container %s suspend success.' % r['cid']}
            return Response(detail, status=status.HTTP_200_OK)
        else:
            detail = {'detail': m}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)


class ContainerUnPauseView(APIView):
    """恢复一个容器

    Info:
        POST /containers/(id)/unpause HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/unpause HTTP/1.1

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {"detail": STRING}
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        if request.POST:
            return Response('Error: Do not need any parameters!',
                            status=status.HTTP_400_BAD_REQUEST)
        msg = {'id': id, 'message_type': 'unpause_container'}
        s, m, r = send_message(msg)
        if s == 0:
            detail = {'detail': 'Container %s unpause success.' % r['cid']}
            return Response(detail, status=status.HTTP_200_OK)
        else:
            detail = {'detail': m}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)


class ContainerTopView(APIView):
    """列出容器中的所有进程

    Info:
        POST /containers/(id)/top HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/top HTTP/1.1

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
        {
             "cid": "bda51967884c70b578a5a86bd12d5f1abc59b58b
                     8be2b65bcf48a410e5536b9b",
             "titles":[
                     "USER",
                     "PID",
                     "%CPU",
                     "%MEM",
                     "VSZ",
                     "RSS",
                     "TTY",
                     "STAT",
                     "START",
                     "TIME",
                     "COMMAND"
                     ],
             "processes":[
                     ["root","20147","0.0","0.1","18060",
                      "1864","pts/4","S","10:06","0:00","bash"],
                     ["root","20271","0.0","0.0","4312",
                      "352","pts/4","S+","10:07","0:00","sleep","10"]
             ]
        }
        Failure:
            {"detail": STRING}
    """

    def get(self, request, id, format=None):
        msg = {'id': id, 'message_type': 'top_container'}
        s, m, r = send_message(msg)
        if s == 0:
            r.pop('id')
            r.pop('host')
            r.pop('port')
            r.pop('message_type')
            return Response(r, status=status.HTTP_200_OK)
        else:
            detail = {'detail': m}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)
