#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django import http
from apphome.models import Image

from serializers import ImageSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import response


class ImageView(APIView):
    """列出所有镜像

    Info:
        GET /images/ HTTP/1.1
        Content-Type: application/json

    Example request:
        - GET /images/ HTTP/1.1
        - GET /images/?iid=0a8fb585b&repository=ubuntu&tag=12.04 ... HTTP/1.1

    Query Parameters:
        iid tag created repository virtual_size
        os_type os_version

    Status Codes:
        200 - no error
        404 - no such image
        500 - server error
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
    """创建一个镜像

    Info:
        POST /images/create HTTP/1.1
        Content-Type: application/json

    Example request:
        POST /images/create HTTP/1.1

    Json Parameters:
        iid tag created repository virtual_size
        os_type os_version
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
    """更新一个镜像

    Info:
        PUT /images/(pk)/update HTTP/1.1
        Content-Type: application/json

    Example request:
        PUT /images/2/update HTTP/1.1

    Json Parameters:
        iid tag created repository virtual_size
        os_type os_version
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
    """删除一个镜像

    Info:
        DELETE /images/(pk)/delete HTTP/1.1
        Content-Type: application/json

    Example request:
        DELETE /images/2/delete HTTP/1.1
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
    """根据 pk 获取镜像

    Info:
        GET /images/(pk)/ HTTP/1.1
        Content-Type: application/json

    Example request:
        GET /images/2/ HTTP/1.1
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
