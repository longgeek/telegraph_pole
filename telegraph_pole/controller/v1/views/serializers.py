from apphome.models import Host
from apphome.models import Image
from apphome.models import Container
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id',
                  'iid',
                  'tag',
                  'created',
                  'os_type',
                  'os_version',
                  'repository',
                  'virtual_size',)


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ('id',
                  'ip',
                  'port',
                  'image',
                  'status',
                  'total_cpu',
                  'total_mem',
                  'total_volume',
                  'total_sys_disk',
                  'total_bandwidth',)


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ('id',
                  'cid',
                  'size',
                  'host',
                  'name',
                  'image',
                  'ports',
                  'status',
                  'user_id',
                  'command',
                  'created',
                  'hostname',
                  'flavor_id',
                  'json_extra')
