==============
TELEGRAPH_POLE
==============

Restful API

Getting Started
---------------

If you'd like to run from the master branch, you can clone the git repo:

    git clone git@git.pyindex.com:reviewdev/telegraph_pole.git

* Wiki: http://wiki.pyindex.com

AMQP Client - Python Pika
-------------
https://github.com/pika/pika

References
----------
* http://wiki.pyindex.com

We have integration with
------------------------
* git@git.pyindex.com:reviewdev/looker.git (online)
* git@git.pyindex.com:reviewdev/boss.git (online manager)
* git@git.pyindex.com:reviewdev/mountain_tai.git (scheduler)

How to use (For Ubuntu-14.04.1 Server)
--------------------------------------

If necessary, please update the system as well as the kernel:
    apt-get upgrade
    apt-get dist-upgrade

Dependent on the installation of the bat:
    git clone git@git.pyindex.com:reviewdev/telegraph_pole.git
    cd telegraph_pole
    pip install -r requirements.txt

The configuration file:
    mkdir /var/log/telegraph-pole
    chown :adm /var/log/telegraph-pole
    cp telegraph_pole/local/local_settings.py.example telegraph_pole/local/local_settings.py
    cp conf/telegraph-pole.conf /etc/init/
    cp conf/logrotate.d/telegraph-pole /etc/logrotate.d/
    logrotate -f /etc/logrotate.d/telegraph-pole
    service rsyslog restart

Modify the configuration file:
    vim telegraph_pole/local/local_settings.py
      e.g.:
      DATABASES
      RABBITMQ
      REDIS
      ....

    vim /etc/init/telegraph-pole.conf
      e.g.:
      chdir /opt/git/telegraph_pole  # the project dir path

    vim conf/gunicorn_config.py
      e.g.:
      bind = "127.0.0.1:9003"  # update this port number, Make sure and nginx proxy_pass

Databases:
    apt-get install mysql-server
    mysql -uroot -p
      create database telegraph_pole default character set utf8;
      grant all on telegraph_pole.* to 'root'@'%' identified by 'password'; 
    python manage.py syncdb

Use nginx proxy telegraph_pole:
    Copy the conf/nginx-telegraph-pole.conf content, Paste to nginx.conf!

Run it:
    service telegraph-pole restart

Log:
    tail -f /var/log/telegraph-pole/*.log
