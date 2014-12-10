#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

import pika
import uuid
import simplejson

from telegraph_pole.settings import RABBITMQ_HOST
from telegraph_pole.settings import RABBITMQ_PORT
from telegraph_pole.settings import RABBITMQ_USER
from telegraph_pole.settings import RABBITMQ_PASS


# class SingLeton(object):
#     """ 单例类，只初始化一次
#
#     获取 RabbitMQ 连接对象.
#     """
#
#     _instance = None
#     conn = None
#     channel = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(SingLeton, cls).__new__(
#                 cls, *args, **kwargs)
#
#             # Initialize RabbitMQ connection
#             credentials = pika.PlainCredentials(RABBITMQ_USER,
#                                                 RABBITMQ_PASS)
#             cls.conn = pika.BlockingConnection(pika.ConnectionParameters(
#                 host=RABBITMQ_HOST,
#                 port=int(RABBITMQ_PORT),
#                 credentials=credentials))
#             cls.channel = cls.conn.channel()
#
#         return (cls.channel, cls.conn)
#
#     def __del__(self):
#         del self._instance
#         del self.conn
#         del self.channel


class Call(object):
    """发送消息同时等待远程返回值"""

    def __init__(self):
        # Initialize RabbitMQ connection
        credentials = pika.PlainCredentials(RABBITMQ_USER,
                                            RABBITMQ_PASS)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=int(RABBITMQ_PORT),
            credentials=credentials))
        self.channel = self.conn.channel()
        # sing_leton = SingLeton()
        # self.channel = sing_leton[0]
        # self.connection = sing_leton[1]

        # 定义接收返回消息的队列(随机)
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        # 消费消息
        self.channel.basic_consume(self.on_response,
                                   no_ack=False,
                                   queue=self.callback_queue)

        # 返回的结果都会保存在该字典中
        self.response = {}

    def on_response(self, ch, method, props, body):
        """定义接收到返回消息的处理方法"""
        self.response[props.correlation_id] = body

    def request(self, message):
        corr_id = str(uuid.uuid4())
        self.response[corr_id] = None

        # 发送消息, 并设置返回队列和 crooelation_id
        self.channel.basic_publish(exchange='',
                                   routing_key='docker_scheduler',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=corr_id),
                                   body=message)

        # 接收返回的数据
        while self.response[corr_id] is None:
            self.conn.process_data_events()
        # 返回接收到的数据
        return self.response[corr_id]


def send_message(message):
    """发送消息"""
    call = Call()
    # 返回消息处理结果
    res = simplejson.loads(call.request(simplejson.dumps(message)))
    return (res[0], res[1], res[2])
