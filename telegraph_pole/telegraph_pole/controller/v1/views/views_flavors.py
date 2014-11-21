#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django import http

from telegraph_pole.apphome.models import Image
from telegraph_pole.apphome.models import Host
from telegraph_pole.apphome.models import Container

from serializers import HostSerializer
from serializers import ImageSerializer
from serializers import ContainerSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import response


class ImageView(APIView):
    """列出所有镜像，或者根据 url 参数进行过滤,
       重新定义 get 请求

    路径:
       GET /images/ HTTP/1.1
       Content-Type: application/json
    """

    def get(self, request, format=None):

        # 如果有 url 参数
        if request.GET:
            # 从数据库中过滤相应的对象
            images = Image.objects.all()
            kwargs = request.GET.dict()
            images = images.filter(**kwargs)

            # 如果没有过滤出，或者参数传递错误，返回 404
            if not images:
                raise http.Http404

        # 没有 url 参数，就返回所有的 Image
        else:
            images = Image.objects.all()

        serializer = ImageSerializer(images, many=True)
        return response.Response(serializer.data)


class ImageCreateView(APIView):
    """创建一个镜像, 重新定义 post 请求

    路径:
       POST /images/create HTTP/1.1
       Content-Type: application/json
    """

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)


class ImageUpdateView(APIView):
    """更新一个镜像, 重新定义 put 请求

    路径:
       PUT /images/(pk)/update HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise http.Http404

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)


class ImageDeleteView(APIView):
    """删除一个镜像, 重新定义 delete 请求

    路径:
       DELETE /images/(pk)/delete HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise http.Http404

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetailView(APIView):
    """根据 pk 获取镜像, 重新定义 get 请求

    路径:
       get /images/(pk)/ HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise http.Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return response.Response(serializer.data)


class HostView(APIView):
    """列出所有的主机或, 根据 url 参数过滤出相应的主机;

    路径:
       GET /hosts/ HTTP/1.1
       Content-Type: application/json
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
    """创建一个主机, 重新定义 post 请求

    路径:
       POST /hosts/create HTTP/1.1
       Content-Type: application/json
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
    """更新一个主机, 重新定义 put 请求

    路径:
       PUT /hosts/(pk)/update HTTP/1.1
       Content-Type: application/json
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
    """删除一个主机, 重新定义 delete 请求

    路径:
       DELETE /hosts/(id)/delete HTTP/1.1
       Content-Type: application/json
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
    """根据 pk 获取主机信息, 重新定义 get 请求

    路径:
       GET /hosts/(id)/ HTTP/1.1
       Content-Type: application/json
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


class ContainerView(APIView):
    """列出所有的主机或, 根据 url 参数过滤出相应的主机;

    路径:
       GET /containers/ HTTP/1.1
       Content-Type: application/json
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
                raise http.Http404

        # 没有 url 参数，就返回所有的 container
        else:
            containers = Container.objects.all()

        serializer = ContainerSerializer(containers, many=True)
        return response.Response(serializer.data)


class ContainerCreateView(APIView):
    """创建一个容器, 重新定义 post 请求

    路径:
       POST /containers/create HTTP/1.1
       Content-Type: application/json
    """

    def post(self, request, format=None):
        serializer = ContainerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)


class ContainerUpdateView(APIView):
    """更新一个容器, 重新定义 put 请求

    路径:
       PUT /containers/(cid)/update HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Container.objects.get(pk=pk)
        except Container.DoesNotExist:
            raise http.Http404

    def put(self, request, pk, format=None):
        container = self.get_object(pk)
        serializer = ContainerSerializer(container, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)


class ContainerDeleteView(APIView):
    """删除一个容器, 重新定义 delete 请求

    路径:
       DELETE /containers/(cid)/delete HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Container.objects.get(pk=pk)
        except Container.DoesNotExist:
            raise http.Http404

    def delete(self, request, pk, format=None):
        container = self.get_object(pk)
        container.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ContainerDetailView(APIView):
    """根据 pk 获取主机信息, 重新定义 get 请求

    路径:
       get /containers/(pk)/ HTTP/1.1
       Content-Type: application/json
    """

    def get_object(self, pk):
        try:
            return Container.objects.get(pk=pk)
        except Container.DoesNotExist:
            raise http.Http404

    def get(self, request, pk, format=None):
        container = self.get_object(pk)
        serializer = ContainerSerializer(container)
        return response.Response(serializer.data)
