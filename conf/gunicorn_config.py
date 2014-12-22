#!/usr/bin/env python
# encoding: utf-8

import multiprocessing

bind = "127.0.0.1:9003"
daemon = False
worker_class = "gevent"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "/var/log/telegraph-pole/access.log"
errorlog = "/var/log/telegraph-pole/error.log"
