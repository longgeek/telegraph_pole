#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from kombu import Connection
from kombu import Exchange

from telegraph_pole.settings import RABBITMQ_URLS

types = {
    'create_container': {
        'queue_name': 'create-container-queue',
        'router_key': 'create.container.router',
        'exchange_name': 'container',
    },
    'start_container': {
        'queue_name': 'start-container-queue',
        'router_key': 'start.container.router',
        'exchange_name': 'container',
    },
    'stop_container': {
        'queue_name': 'stop-container-queue',
        'router_key': 'stop.container.router',
        'exchange_name': 'container',
    },
    'restart_container': {
        'queue_name': 'restart-container-queue',
        'router_key': 'restart.container.router',
        'exchange_name': 'container',
    },
    'delete_container': {
        'queue_name': 'delete-container-queue',
        'router_key': 'delete.container.router',
        'exchange_name': 'container',
    },
}


def send(type, messages):
    router_key = types[type]['router_key']
    exchange_name = types[type]['exchange_name']

    exchange = Exchange(exchange_name,
                        type='topic',
                        durable=True)
    # connection
    with Connection(RABBITMQ_URLS) as conn:
        # produce
        producer = conn.Producer(serializer='json', exchange=exchange)
        producer.publish(messages,
                         exchange=exchange,
                         routing_key=router_key)
