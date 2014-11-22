#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from kombu import Connection
from kombu import Exchange
from kombu import Queue

types = {
    'create_container': {
        'queue_name': 'create_container_queue',
        'router_key': 'create_container_router',
        'exchange_name': 'create_container_exchange',
    },
    'start_container': {
        'queue_name': 'start_container_queue',
        'router_key': 'start_container_router',
        'exchange_name': 'start_container_exchange',
    },
    'stop_container': {
        'queue_name': 'stop_container_queue',
        'router_key': 'stop_container_router',
        'exchange_name': 'stop_container_exchange',
    },
    'restart_container': {
        'queue_name': 'restart_container_queue',
        'router_key': 'restart_container_router',
        'exchange_name': 'restart_container_exchange',
    },
    'delete_container': {
        'queue_name': 'delete_container_queue',
        'router_key': 'delete_container_router',
        'exchange_name': 'delete_container_exchange',
    },
}


def send(type, messages):
    queue_name = types[type]['queue_name']
    router_key = types[type]['router_key']
    exchange_name = types[type]['exchange_name']

    exchange = Exchange(exchange_name,
                        'direct',
                        durable=True)
    queue = Queue(queue_name,
                  exchange=exchange,
                  routing_key=router_key)
    # connection
    with Connection('amqp://guest:guest@192.168.8.239:5672//') as conn:
        # produce
        producer = conn.Producer(serializer='json')
        producer.publish(messages,
                         exchange=exchange,
                         routing_key=router_key,
                         declare=[queue])

if __name__ == "__main__":
    send('create_container', 'testssssssssssssssss')
