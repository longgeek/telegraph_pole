#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

import redis
import hashlib
import simplejson

from django.http import Http404
from apphome.models import Container
from serializers import ContainerSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from telegraph_pole.lib.mq import send_message

from telegraph_pole.settings import REDIS_DB
from telegraph_pole.settings import REDIS_HOST
from telegraph_pole.settings import REDIS_PORT
from telegraph_pole.settings import CONSOLE_DOMAIN


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
        user_id command created hostname flavor_id json_extra

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
                    "flavor_id": "1",
                    "json_extra": "",
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
        user_id command created hostname flavor_id json_extra

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
                "json_extra": "",
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
            return Response({'detail': str(serializer.errors)},
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
        user_id command created hostname flavor_id json_extra

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
        return Response({'detail': str(serializer.errors)},
                        status=status.HTTP_400_BAD_REQUEST)


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
                "flavor_id": "1",
                "json_extra": "",
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
        param = request.DATA

        # 判断 post 的参数是否有 'command'
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


class ContainerConsoleView(APIView):
    """容器启动 bash ipython vim Console.

    Info:
        POST /containers/(id)/console HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/console HTTP/1.1

        {
         "username":"longgeek",
         "command":[
                     "/bin/bash",
                     "vim /path/urls.py",
             ]
        }

    Jons Parameters:
        command: list
        username: str

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {
                "id": "10",
                "cid": "779bfb2bebb079ae80f7686c642cb83df9ae
                        b51b3cd139fc050860f362def2ed",
                "host": "192.168.8.8",
                "username": 'longgeek',
                "console": {
                    "/bin/bash": {
                        "private_port": 4301,
                        "public_port": 49187
                    }
                },
            }
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        param = request.DATA

        # 判断 post 的参数是否有 'command' ’username'
        # 并且 value 不能为空
        if len(param) == 2 and 'command' in param.keys() and \
                               'username' in param.keys():
            if param['command'] and param['username']:
                msg = {'id': id,
                       'command': param['command'],
                       'username': param['username'],
                       'message_type': 'console_container'}
                s, m, r = send_message(msg)
                if s == 0:
                    return Response(r, status=status.HTTP_200_OK)
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


class ContainerFilesWriteView(APIView):
    """为容器中的文件写入数据

    Info:
        POST /containers/(id)/files/write HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/files/write HTTP/1.1

        {
         "username":"longgeek",
         "files":{
            "/opt/python/django_project/urls.py": "file content",
            "/opt/python/django_project/views.py": "file content",
            }
        }

    Jons Parameters:
        files: dict
        username: str

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {
                "id": "10",
                "cid": "779bfb2bebb079ae80f7686c642cb83df9ae
                        b51b3cd139fc050860f362def2ed",
                "host": "192.168.8.8",
                "username": 'longgeek',
                "files":{
                   "/opt/python/django_project/urls.py": "file content",
                   "/opt/python/django_project/views.py": "file content",
                }
            }
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        param = request.DATA

        # 判断 post 的参数是否有 'files' 'username'
        # 并且 value 不能为空
        if len(param) == 2 and 'files' in param.keys() and \
                               'username' in param.keys():
            if param['files'] and param['username']:
                # for file_name in simplejson.loads(param['files']):
                #     if file_name[0] != '/':
                #         detail = {'detail': 'Error: The wrong parameter!'}
                #         return Response(detail,
                #                         status=status.HTTP_400_BAD_REQUEST)
                msg = {'id': id,
                       'files': param['files'],
                       'username': param['username'],
                       'message_type': 'files_write_container'}
                s, m, r = send_message(msg)
                if s == 0:
                    return Response(r, status=status.HTTP_200_OK)
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


class ContainerFilesReadView(APIView):
    """为容器中的文件写入数据

    Info:
        POST /containers/(id)/files/read HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/files/read HTTP/1.1

        {
         "files":[
                     "/path/urls.py",
                     "/path/views.py",
             ],
        }

    Jons Parameters:
        files: list
        username: str

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {
                "id": "10",
                "cid": "779bfb2bebb079ae80f7686c642cb83df9ae
                        b51b3cd139fc050860f362def2ed",
                "host": "192.168.8.8",
                "username": 'longgeek',
                "files": {
                    "/opt/python/django_project/urls.py": "file content",
                    "/opt/python/django_project/views.py": "file content",
                },
            }
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        param = request.DATA

        # 判断 post 的参数是否有 'files' ’username'
        # 并且 value 不能为空
        if len(param) == 2 and 'files' in param.keys() and \
                               'username' in param.keys():
            if param['files'] and param['username']:
                # for file_name in param['files']:
                #     if file_name[0] != '/':
                #         detail = {'detail': 'Error: The wrong parameter!'}
                #         return Response(detail,
                #                         status=status.HTTP_400_BAD_REQUEST)
                msg = {'id': id,
                       'files': param['files'],
                       'username': param['username'],
                       'message_type': 'files_read_container'}
                s, m, r = send_message(msg)
                if s == 0:
                    return Response(r, status=status.HTTP_200_OK)
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


class ContainerConsoleUrlView(APIView):
    """从 redis 中获取 bash ipython vim Console url.

    Info:
        POST /containers/(id)/console/url HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /containers/3/console/url HTTP/1.1

        {
         "username":"longgeek",
         "command":[
                     "/bin/bash",
                     "vim /path/urls.py",
             ]
        }

    Jons Parameters:
        command: list
        username: str

    Status Codes:
        200 - Success, no error
        400 - Failure, bad request
        500 - Failure, server error

    Results: JSON
        Success:
            {
                "/bin/bash": "51d962f4446e125073234337.console.coderpie.com"
                "vim /opt/views.py": "51d962f4446e125073234337\
                        .console.coderpie.com"
            }
        Failure:
            {"detail": STRING}
    """

    def post(self, request, id, format=None):
        param = request.DATA

        # 判断 post 的参数是否有 'command' ’username'
        # 并且 value 不能为空
        if len(param) == 2 and 'command' in param.keys() and \
                               'username' in param.keys():
            if not param['command'] or not param['username']:
                detail = {'detail': 'Error: The wrong parameter!'}
                return Response(detail,
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                # 根据 cid username command 生成 hash
                cid = Container.objects.get(id=id).cid
                username = param['username']
                command_list = simplejson.loads(param['command'])

                # 连接到 Redis 数据库
                conn = redis.Redis(REDIS_HOST, REDIS_PORT, REDIS_DB)

                # 定义返回数据
                results = {}

                # 遍历多条命令, 生成 hash
                for command in command_list:
                    hash_key = hashlib.md5(username +
                                           cid +
                                           command).hexdigest()
                    # 根据 hash 值从 Redis 获取 Value
                    full_hash_key = cid[:12] + hash_key[:12]
                    console_url = conn.get(full_hash_key)
                    if console_url:
                        console_url = full_hash_key + CONSOLE_DOMAIN

                    results[command] = console_url
                return Response(results, status=status.HTTP_200_OK)

            except Exception, e:
                return Response({'detail': str(e)},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            detail = {'detail': 'Error: The wrong parameter!'}
            return Response(detail,
                            status=status.HTTP_400_BAD_REQUEST)
