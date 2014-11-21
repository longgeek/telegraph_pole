#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from docker import Client
from online.apphome import models


def check_host(ip, port):
    """检测 Docker Host 是否开启
    Params:
        ip:   str;    Docker Host IP 地址
        port: str;  Docker Host 开放的端口号

    Return:
        (status,
         msgs,
         results)
    """
    conn = Client(base_url='tcp://%s:%s' % (ip, port),
                  timeout=5,
                  tls=False)
    try:
        return (0, '', (conn.info(), conn.version()))
    except Exception, msgs:
        return (1, msgs, '')


def scheduler_host():
    """Host 调度器
    Params:
        ip:   str;  Docker Host IP 地址
        port: str;  Docker Host 开放的端口号

    Return:
        (status,
         msgs,
         results)
    """
    # 过滤开启的主机列表
    up_host = models.db_HOST.object.filter(status=True)
    if up_host:
        for host in up_host:
            # 拿到主机总的配置情况
            # total_cpu = host.total_cpu
            # total_mem = host.total_mem
            # total_disk = host.total_disk
            # total_volume = host.total_volume
            # total_bandwidth = host.total_bandwidth

            # 计算出这台主机上运行 Docker 容器的所有配置总和
            containers = models.db_Container.object.filter(host_ip=host)
            if containers:
                for container in containers:
                    pass

            else:
                results = {}
                results['host_ip'] = host.ip
                results['host_port'] = host.port
                return (0, '', results)
    else:
        return (1, 'No valid host can schedule!', '')
