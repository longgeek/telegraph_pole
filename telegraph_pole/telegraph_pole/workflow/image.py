#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from time import localtime
from time import strftime

from online.settings import DOCKER_SCHEDULER_CONN


def get_images(host_ip, host_port, user_id=None):
    """获取 Docker 主机上的镜像
    Params:
        host_ip:   str;  Docker Host IP 地址
        host_port: str;  Docker Host 开放的端口号

    Return:
        (status,
         msgs,
         results) # results: 返回经过处理的一台主机上所有镜像列表
    """

    images = DOCKER_SCHEDULER_CONN.images()
    results = []

    for image in images:
        # 转换为字符串时间格式
        created = image['Created']
        str_created = strftime('%Y-%m-%d %X', localtime(created))

        # 以 MB 为单位
        size = image['Size'] / 1048576.0
        virtual_size = image['VirtualSize'] / 1048576.0

        # 定义 image 的 id 长度为前 12 位
        image_id = image['Id'][:12]
        parent_id = image['ParentId']

        # 分割 api 中 'RepoTags' 字段
        repo_tags = image['RepoTags']
        for repotag in repo_tags:
            redefine_images = {}
            repo_tags_split = repotag.split(':')
            if len(repo_tags_split) == 2:
                repo = repo_tags_split[0]
                tags = repo_tags_split[1]
            else:
                repo = repo_tags_split[0] + ':' + repo_tags_split[1]
                tags = repo_tags_split[2]

            if repo and tags:
                redefine_images[u'Id'] = image_id
                redefine_images[u'Tag'] = tags
                redefine_images[u'Repo'] = repo
                redefine_images[u'Size'] = size
                redefine_images[u'Created'] = str_created
                redefine_images[u'ParentId'] = parent_id
                redefine_images[u'VirtualSize'] = virtual_size
                results.append(redefine_images)
            else:
                continue
    return (0, '', results)


def delete_images(host_ip, host_port, image, user_id=None):
    """删掉 Docker 主机上的镜像
    Params:
        host_ip:   str;  Docker Host IP 地址
        host_port: str;  Docker Host 开放的端口号
        image:     str;  Docker Image 的 id 或 repo+tag

    Return:
        (status,
         msgs,
         results)
    """

    try:
        DOCKER_SCHEDULER_CONN.remove_image(image)
        return (0, '', '%s has been deleted!')
    except Exception, msgs:
        return (1, msgs, '')
