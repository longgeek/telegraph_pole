#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from time import localtime
from time import strftime

from online.apphome import models
from host import scheduler_host
from online.settings import DOCKER_SCHEDULER_CONN


def get_containers(host_ip, host_port, size=False, quiet=False, all=False):
    """获取 Docker 主机上的镜像
    Params:
        host_ip:   str;  Docker Host IP 地址
        host_port: str;  Docker Host 开放的端口号
        quiet:     bool; 是否只显示容器 ID 号
        all:       bool; 是否显示所有的容器，包括stop
        size：     bool; 是否显示容器的大小

    Return:
        (status,
         msgs,
         results) # results: 返回一台 Docker 主机上所有的容器列表
    """
    containers = DOCKER_SCHEDULER_CONN.containers(all=all,
                                                  size=size,
                                                  quiet=quiet)
    return (0, '', containers)


def delete_containers(host_ip, host_port, status, container):
    """获取 Docker 主机上的镜像
    Params:
        host_ip:   str;  Docker Host IP 地址
        host_port: str;  Docker Host 开放的端口号

    Return:
        (status,
         msgs,
         results) # results: 返回一台 Docker 主机上所有的容器列表
    """
    if status:
        DOCKER_SCHEDULER_CONN.stop(container=container, timeout=10)
    try:
        DOCKER_SCHEDULER_CONN.remove_container(container=container, force=True)
        return (0, '', 'Container %s is deleted!' % container)
    except Exception, msgs:
        return (1, msgs, '')


def create_containers(user,
                      image,
                      flavor,
                      name=None,
                      ports=None,
                      host_ip=None,
                      command=None,
                      hostname=None):
    """获取 Docker 主机上的镜像
    Params:
        user:     str;
        image:    object;
        flavor:   object;
        name:     str;
        ports:    list;
        host_ip:  object;
        command:  str;
        hostname: str;

    Return:
        (status,
         msgs,
         results)
    """

    # 如果没有指定 Docker Host
    # 使用调度器 api 计算出有效的主机
    if not host_ip:
        results = scheduler_host()
        if results[0] == 0:
            host = scheduler_host[2]
            ip = host['ip']
            port = host['port']
        else:
            return (1, scheduler_host[1], '')
    else:
        ip = host_ip.ip
        port = host_ip.port

    if image.tag and image.repository:
        image_name = image.repository + ':' + image.tag
    else:
        image_name = image.iid

    if not command:
        command = '/bin/bash'
    container = DOCKER_SCHEDULER_CONN.create_container(name=name,
                                                       image=image_name,
                                                       ports=ports,
                                                       command=command,
                                                       hostname=hostname,
                                                       tty=True,
                                                       detach=True,
                                                       stdin_open=True)
    try:
        DOCKER_SCHEDULER_CONN.start(container=container['Id'])
    except Exception, msgs:
        return (1, msgs, '')
    else:
        container_info = get_containers(ip,
                                        port,
                                        quiet=False,
                                        size=True,
                                        all=True)
        if container_info[0] != 0:
            return (1, container_info[1], '')

        for info in container_info[2]:
            if info['Id'] == container['Id']:
                size = info['SizeRw']
                if size:
                    size /= 1048576.0
                status = info['Status']
                created = info['Created']
                str_created = strftime('%Y-%m-%d %X', localtime(created))

        if status[:2] == 'Up':
            status = True
        else:
            status = False

        # 保存到数据库中
        container_db = models.db_Container(cid=container['Id'][:12],
                                           flavor=flavor,
                                           image=image,
                                           user=user,
                                           host_ip=host_ip,
                                           name=name,
                                           ports=ports,
                                           hostname=hostname,
                                           created=str_created,
                                           status=status,
                                           command=command,
                                           size=size)
        container_db.save()
